from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(f"Сгенерированный ключ: {key}")  

f = Fernet(key)
message = b"This is a secret message! Hello!"
encrypted_data = f.encrypt(message)
print(f"Зашифрованное сообщение: {encrypted_data}")

with open("key.txt", "wb") as f:
    f.write(key)
with open("secret.txt", "wb") as f:
    f.write(encrypted_data)