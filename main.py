from flask import Flask, request, jsonify
from pymongo import MongoClient
from crypto_utils import encrypt, decrypt
import os

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URL"))
db = client["hetbot"]
users = db["users"]

@app.route("/")
def home():
    return "HET API is working"

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    user_id = data.get("user_id")
    login = data.get("login")
    password = data.get("password")

    if not user_id or not login or not password:
        return jsonify({"error": "Missing fields"}), 400

    encrypted_login = encrypt(login)
    encrypted_password = encrypt(password)

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
        user["login"] = decrypt(user["login"])
        user["password"] = decrypt(user["password"])
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
