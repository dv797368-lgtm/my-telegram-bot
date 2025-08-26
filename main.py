import os
from flask import Flask
import threading
from telegram.ext import Updater, CommandHandler

# ⚠️ ضع التوكن تاع البوت هنا
TOKEN = "7473686932:AAEmpKvL4rJyC2aEzyJ3be65eCF2FFdwc6A"

# ----------------------
# بوت تيليغرام
# ----------------------
def start(update, context):
    update.message.reply_text("✅ البوت شغال على Render!")

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

# ----------------------
# سيرفر ويب صغير
# ----------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running on Render!"

def run_web():
    port = int(os.environ.get("PORT", 5000))  # Render يفرض PORT خاص
    app.run(host="0.0.0.0", port=port)

# ----------------------
# تشغيل الاثنين
# ----------------------
threading.Thread(target=run_bot).start()
run_web()
