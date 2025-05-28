from flask import Flask, request, jsonify
from pymongo import MongoClient
from cryptography.fernet import Fernet
import os

app = Flask(__name__)

# MongoDB URI и ключ шифрования из переменных окружения
MONGO_URI = os.environ.get("MONGO_URI")
ENC_KEY = os.environ.get("ENC_KEY")

if not MONGO_URI or not ENC_KEY:
    raise RuntimeError("Missing environment variables: MONGO_URI or ENC_KEY")

client = MongoClient(MONGO_URI)
db = client["hetbot"]
users = db["users"]

# Настройка шифратора
f = Fernet(ENC_KEY)

@app.route("/")
def home():
    return "HET bot is working"

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    user_id = data.get("user_id")
    login = data.get("login")
    password = data.get("password")

    if not user_id or not login or not password:
        return jsonify({"error": "Missing fields"}), 400

    encrypted_login = f.encrypt(login.encode()).decode()
    encrypted_password = f.encrypt(password.encode()).decode()

    users.update_one(
        {"user_id": user_id},
        {"$set": {"login": encrypted_login, "password": encrypted_password}},
        upsert=True
    )
    return jsonify({"status": "saved"}), 200

@app.route("/get/<user_id>")
def get(user_id):
    user = users.find_one({"user_id": user_id}, {"_id": 0})
    if user:
        try:
            user["login"] = f.decrypt(user["login"].encode()).decode()
            user["password"] = f.decrypt(user["password"].encode()).decode()
        except Exception as e:
            return jsonify({"error": "Decryption failed"}), 500
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
