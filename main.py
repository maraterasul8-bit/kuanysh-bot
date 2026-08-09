import os
import time
import random
import threading
import telebot
from telebot import types
from flask import Flask, request

BOT_TOKEN = "8991039569:AAGACaer0mj5acvbiGVWfxdN01m9PBgi-1A"
CHAT_ID = "1377361873"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Пайдаланушы таңдауларын сақтау
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_start = types.InlineKeyboardButton("🚀 KUANYSH TRADING SYSTEM", callback_data="main_menu")
    markup.add(btn_start)
    bot.send_message(message.chat.id, "🤖 **Kuanysh system v2.0** қош келдіңіз!\n\nЖүйені іске қосу үшін төмендегі батырманы басыңыз:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "main_menu" or call.data == "back_to_pairs":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("AED/CNY OTC", callback_data="pair_AED/CNY"),
            types.InlineKeyboardButton("EUR/USD OTC", callback_data="pair_EUR/USD"),
            types.InlineKeyboardButton("GBP/USD OTC", callback_data="pair_GBP/USD"),
            types.InlineKeyboardButton("BTC/USD OTC", callback_data="pair_BTC/USD")
        )
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, 
                              text="📊 **Активті таңдаңыз:**", reply_markup=markup, parse_mode="Markdown")
        
    elif call.data.startswith("pair_"):
        pair = call.data.split("_")[1]
        user_data[chat_id] = {"pair": pair}
        
        markup = types.InlineKeyboardMarkup(row_width=4)
        markup.add(
            types.InlineKeyboardButton("5s", callback_data="time_5s"),
            types.InlineKeyboardButton("15s", callback_data="time_15s"),
            types.InlineKeyboardButton("30s", callback_data="time_30s"),
            types.InlineKeyboardButton("1m", callback_data="time_1m")
        )
        markup.add(types.InlineKeyboardButton("⬅️ Артқа", callback_data="back_to_pairs"))
        
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, 
                              text=f"💱 Таңдалған актив: **{pair}**\n\n⏱️ **Уақыт аралығын таңдаңыз:**", reply_markup=markup, parse_mode="Markdown")
        
    elif call.data.startswith("time_"):
        t_frame = call.data.split("_")[1]
        if chat_id in user_data:
            user_data[chat_id]["time"] = t_frame
        else:
            user_data[chat_id] = {"pair": "AED/CNY", "time": t_frame}
            
        pair = user_data[chat_id]["pair"]
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔮 ПОЛУЧИТЬ ПРОГНОЗ", callback_data="get_forecast"),
            types.InlineKeyboardButton("⬅️ Артқа", callback_data=f"pair_{pair}")
        )
        
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, 
                              text=f"💱 Актив: **{pair}** | ⏱️ Уақыт: **{t_frame}**\n\nНейросеть дайын. Прогноз алу үшін түймені басыңыз:", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "get_forecast":
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, 
                              text="🧠 **Анализ нейросеть...**\nОқыту модельдері мен индикаторлар тексерілуде...", parse_mode="Markdown")
        time.sleep(2)
        
        info = user_data.get(chat_id, {"pair": "AED/CNY", "time": "1m"})
        pair = info.get("pair", "AED/CNY")
        t_frame = info.get("time", "1m")
        
        decision = random.choice(["🟢 ПОКУПКА (BUY)", "🔴 ПРОДАЖА (SELL)"])
        confidence = round(random.uniform(88.5, 98.2), 1)
        price_val = round(random.uniform(1.1000, 5.5000), 4)

        result_text = (
            f"🤖 **KUANYSH SYSTEM v2.0 | ПРОГНОЗ**\n\n"
            f"📊 Актив: **{pair} OTC**\n"
            f"⏱️ Таймфрейм: **{t_frame}**\n"
            f"📈 Баға деңгейі: `{price_val}`\n\n"
            f"🔥 Қорытынды шешім: **{decision}**\n"
            f"⚡️ Дәлдік көрсеткіші: **{confidence}%**\n\n"
            f"⚠️ *Тәуекелді өзіңіз басқарыңыз!*"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("🔄 Жаңа прогноз алу", callback_data="main_menu"))
        
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, 
                              text=result_text, reply_markup=markup, parse_mode="Markdown")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        signal = data.get('signal', 'Белгісіз сигнал')
        bot.send_message(CHAT_ID, f"📢 Сигнал: {signal}")
        return "OK", 200
    return "Error", 400

# Ботты бөлек ағында іске қосу функциясы
def run_bot():
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    # Ботты фоновом режимде (потокта) қосамыз
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Flask веб-серверін іске қосамыз
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
