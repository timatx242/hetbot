from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB
client = MongoClient("mongodb+srv://timatx360:JxhBu8lFpkYInaN0@cluster0.babxayx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["hetbot"]
users = db["users"]

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

    users.update_one({"user_id": user_id}, {"$set": {"login": login, "password": password}}, upsert=True)
    return jsonify({"status": "saved"}), 200

@app.route("/get/<user_id>")
def get(user_id):
    user = users.find_one({"user_id": user_id}, {"_id": 0})
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
