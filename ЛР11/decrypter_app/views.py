from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from cryptography.fernet import Fernet
from django.views.decorators.csrf import csrf_exempt
import logging


logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'decrypter_app/index.html')

def login(request):
    return JsonResponse({"author": "1149288"})

def decrypt_message(key_file_content, encrypted_message):
    """Расшифровывает зашифрованное сообщение с использованием Fernet."""
    try:
        f = Fernet(key_file_content)
        decrypted_message = f.decrypt(encrypted_message)
        return decrypted_message.decode('utf-8')
    except Exception as e:
        logger.exception(f"Ошибка в decrypt_message: {e}")  
        return f"Ошибка расшифровки: {str(e)}"  

@csrf_exempt
def decypher(request):
    if request.method == 'POST':
        logger.debug(f"Received POST request to /decypher/")
        logger.debug(f"FILES: {request.FILES}")

        if 'key' not in request.FILES or 'secret' not in request.FILES:
            logger.error("Отсутствует ключ или зашифрованное сообщение")
            return JsonResponse({"error": "Отсутствует ключ или зашифрованное сообщение"}, status=400)

        key_file = request.FILES['key']
        secret_file = request.FILES['secret']

        if not key_file or not secret_file:
            logger.error("Не указан файл ключа или зашифрованное сообщение")
            return JsonResponse({"error": "Не указан файл ключа или зашифрованное сообщение"}, status=400)

        try:
            key_file_content = key_file.read()
            secret_file_content = secret_file.read()
            logger.debug(f"key_file_content (bytes): {key_file_content[:50]}...") 
            logger.debug(f"secret_file_content (bytes): {secret_file_content[:50]}...") 
        except Exception as e:
            logger.exception(f"Ошибка чтения файла: {e}")
            return JsonResponse({"error": f"Ошибка чтения файла: {str(e)}"}, status=500)

        try:
            decrypted_text = decrypt_message(key_file_content, secret_file_content)
            if "Ошибка" in decrypted_text:  
                return JsonResponse({"error": decrypted_text}, status=500)  
            logger.info(f"Расшифровано сообщение: {decrypted_text[:50]}...")  
            return HttpResponse(decrypted_text.encode('utf-8'), content_type="text/plain; charset=utf-8")  
        except Exception as e:
            logger.exception(f"Ошибка расшифровки: {e}")
            return JsonResponse({"error": f"Ошибка расшифровки: {str(e)}"}, status=500)
    else:
        logger.warning("Method not allowed")
        return JsonResponse({"error": "Method not allowed"}, status=405)