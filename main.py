import os
import telebot
from flask import Flask, request

BOT_TOKEN = "8991039569:AAGAcAeR0mj5acvbiGVWfxdNO1m9PBgi-lA"
CHAT_ID = "1377361873"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        signal = data.get('signal', 'Белгісіз сигнал')
        bot.send_message(CHAT_ID, f"📢 Сигнал: {signal}")
        return "OK", 200
    return "Error", 400

@app.route('/')
def index():
    return "Bot is running"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
