from cryptography.fernet import Fernet
import os

SECRET_KEY = os.getenv("SECRET_KEY").encode()
cipher = Fernet(SECRET_KEY)

def encrypt(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt(token):
    return cipher.decrypt(token.encode()).decode()
