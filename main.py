import os
import telebot
from flask import Flask, request

BOT_TOKEN = "8991039569:AAGACaer0mj5acvbiGVWfxdN01m9PBgi-1A"
CHAT_ID = "1377361873"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Қолданушы /start деп жазғанда жұмыс істейтін бөлік
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Сәлем! Kuanysh system жұмыс істеп тұр. Сізден сигналдарды күтудемін! 🚀")

# Сыртқы трейдинг сигналдарын қабылдайтын бөлік
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        signal = data.get('signal', 'Белгісіз сигнал')
        bot.send_message(CHAT_ID, f"📢 Сигнал: {signal}")
        return "OK", 200
    return "Error", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
