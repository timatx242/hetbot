# crypto_utils.py
from cryptography.fernet import Fernet
import os

SECRET_KEY = os.getenv("SECRET_KEY").encode()
cipher = Fernet(SECRET_KEY)

def encrypt(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt(data: str) -> str:
    return cipher.decrypt(data.encode()).decode()
