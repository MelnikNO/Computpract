from flask import Flask, render_template, request, send_file, jsonify
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64
import os

app = Flask(__name__)

# Создание папки (если используется альтернативный вариант)
UPLOAD_FOLDER = 'static/images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

LOGIN = "1149288"

@app.route('/login')
def login():
    return jsonify({"author": LOGIN})

@app.route('/', methods=['GET'])
def index():
    return render_template('makeimage.html', message=None)

@app.route('/makeimage', methods=['POST'])
def make_image():
    if request.method == 'POST':
        try:
            width = int(request.form['width'])
            height = int(request.form['height'])
            text = request.form['text']

            if width <= 0 or height <= 0:
                return render_template('makeimage.html', message="Invalid image size")

            img = Image.new('RGB', (width, height), color='white')
            d = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("arial.ttf", size=min(width//len(text) , height//2))
            except IOError as e:
                font = ImageFont.load_default()


            bbox = d.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            x = (width - text_width) / 2
            y = (height - text_height) / 2

            d.text((x, y), text, fill=(0, 0, 0), font=font)

            img_io = BytesIO()
            img.save(img_io, 'JPEG', quality=70)
            img_io.seek(0)

            # Вариант 1: Base64 кодирование
            img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
            return render_template('makeimage.html', message=None, image=img_base64)

            # # Вариант 2: Сохранение на сервере и отдача URL
            # image_filename = f"image_{width}x{height}.jpg"
            # img_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            # img.save(img_path, 'JPEG')
            # image_url = os.path.join(app.config['UPLOAD_FOLDER'], image_filename) #os.path.join(app.config['UPLOAD_FOLDER'], image_filename) #url_for('static', filename=os.path.join('images', image_filename))
            #
            # return render_template('makeimage.html', message=None, image_url=image_url)

        except ValueError as e:
            return render_template('makeimage.html', message="Invalid image size")
        except Exception as e:
            return render_template('makeimage.html', message="An internal error occurred")

    else:
        return "Method Not Allowed", 405

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)