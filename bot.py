from pymongo import MongoClient
from crypto_utils import decrypt
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

client = MongoClient(os.getenv("MONGO_URL"))
db = client["hetbot"]
users = db["users"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой HET бот.")

async def get_credentials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user = users.find_one({"user_id": user_id})
    if not user:
        await update.message.reply_text("Нет сохранённых данных.")
        return
    login = decrypt(user["login"])
    password = decrypt(user["password"])
    await update.message.reply_text(f"Login: {login}\nPassword: {password}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("get", get_credentials))

app.run_polling()
