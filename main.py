#!/usr/bin/env python
# coding: utf-8

import telebot
from telebot import types
from aliexpress_api import AliexpressApi, models
import re, requests, json, traceback, os
from urllib.parse import quote
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask
import threading

# --- Load Environment Variables ---
load_dotenv()

# --- Configuration Settings ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
ALIEXPRESS_APP_KEY = os.getenv("ALIEXPRESS_APP_KEY")
ALIEXPRESS_APP_SECRET = os.getenv("ALIEXPRESS_APP_SECRET")
CURRENCY_CODE = os.getenv("CURRENCY_CODE", "USD")
SHIP_TO_COUNTRY = os.getenv("SHIP_TO_COUNTRY", "CA")

# --- Bot Initialization ---
if not BOT_TOKEN:
    print("!!! خطأ فادح: لم يتم العثور على BOT_TOKEN. يرجى إعداده في ملف .env")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)
aliexpress = AliexpressApi(
    ALIEXPRESS_APP_KEY,
    ALIEXPRESS_APP_SECRET,
    models.Language.AR,
    CURRENCY_CODE,
    'default',
    ship_to_country=SHIP_TO_COUNTRY
)

# --- Flask Server for Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram Bot is running on Render!"

def run_web():
    port = int(os.environ.get("PORT", 5000))  # Render يعطي PORT تلقائيا
    app.run(host="0.0.0.0", port=port)

def run_bot():
    print(f"🤖 Bot starting... [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
    bot.infinity_polling(timeout=20)

# --- Threads: bot + flask ---
if __name__ == '__main__':
    if not all([BOT_TOKEN, ALIEXPRESS_APP_KEY, ALIEXPRESS_APP_SECRET]):
        print("!!! خطأ: يرجى إعداد متغيرات البيئة (BOT_TOKEN, ALIEXPRESS_APP_KEY, ALIEXPRESS_APP_SECRET)")
    else:
        threading.Thread(target=run_bot).start()
        run_web()
