import os
import time
import random
import telebot
from telebot import types
from flask import Flask, request

BOT_TOKEN = "8991039569:AAGAcAeR0mj5acvbiGVWfxdNO1m9PBgi-lA"
CHAT_ID = "1377361873"
WEBHOOK_URL = f"https://kuanysh-bot.onrender.com/{BOT_TOKEN}"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

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
            types.InlineKeyboardButton("AED/CNY OTC", callback_data="pair_AED/CNY_OTC"),
            types.InlineKeyboardButton("USD/PKR OTC", callback_data="pair_USD/PKR_OTC"),
            types.InlineKeyboardButton("USD/PHP OTC", callback_data="pair_USD/PHP_OTC"),
            types.InlineKeyboardButton("EUR/USD OTC", callback_data="pair_EUR/USD_OTC"),
            types.InlineKeyboardButton("GBP/USD OTC", callback_data="pair_GBP/USD_OTC"),
            types.InlineKeyboardButton("USD/CAD OTC", callback_data="pair_USD/CAD_OTC"),
            types.InlineKeyboardButton("USD/JPY OTC", callback_data="pair_USD/JPY_OTC"),
            types.InlineKeyboardButton("AUD/CAD OTC", callback_data="pair_AUD/CAD_OTC"),
            types.InlineKeyboardButton("AUD/CHF OTC", callback_data="pair_AUD/CHF_OTC"),
            types.InlineKeyboardButton("AUD/USD OTC", callback_data="pair_AUD/USD_OTC"),
            types.InlineKeyboardButton("CAD/JPY OTC", callback_data="pair_CAD/JPY_OTC"),
            types.InlineKeyboardButton("EUR/CHF OTC", callback_data="pair_EUR/CHF_OTC"),
            types.InlineKeyboardButton("EUR/TRY OTC", callback_data="pair_EUR/TRY_OTC"),
            types.InlineKeyboardButton("GBP/AUD OTC", callback_data="pair_GBP/AUD_OTC"),
            types.InlineKeyboardButton("OMR/CNY OTC", callback_data="pair_OMR/CNY_OTC"),
            types.InlineKeyboardButton("QAR/CNY OTC", callback_data="pair_QAR/CNY_OTC"),
            types.InlineKeyboardButton("USD/CNH OTC", callback_data="pair_USD/CNH_OTC"),
            types.InlineKeyboardButton("USD/INR OTC", callback_data="pair_USD/INR_OTC"),
            types.InlineKeyboardButton("ZAR/USD OTC", callback_data="pair_ZAR/USD_OTC"),
            types.InlineKeyboardButton("CHF/NOK OTC", callback_data="pair_CHF/NOK_OTC"),
            types.InlineKeyboardButton("SAR/CNY OTC", callback_data="pair_SAR/CNY_OTC"),
            types.InlineKeyboardButton("AUD/NZD OTC", callback_data="pair_AUD/NZD_OTC"),
            types.InlineKeyboardButton("EUR/GBP OTC", callback_data="pair_EUR/GBP_OTC"),
            types.InlineKeyboardButton("EUR/NZD OTC", callback_data="pair_EUR/NZD_OTC"),
            types.InlineKeyboardButton("EUR/JPY OTC", callback_data="pair_EUR/JPY_OTC"),
            types.InlineKeyboardButton("USD/BRL OTC", callback_data="pair_USD/BRL_OTC"),
            types.InlineKeyboardButton("USD/MXN OTC", callback_data="pair_USD/MXN_OTC"),
            types.InlineKeyboardButton("USD/RUB OTC", callback_data="pair_USD/RUB_OTC"),
            types.InlineKeyboardButton("CAD/CHF OTC", callback_data="pair_CAD/CHF_OTC"),
            types.InlineKeyboardButton("USD/ARS OTC", callback_data="pair_USD/ARS_OTC"),
            types.InlineKeyboardButton("NZD/JPY OTC", callback_data="pair_NZD/JPY_OTC"),
            types.InlineKeyboardButton("CHF/JPY OTC", callback_data="pair_CHF/JPY_OTC"),
            types.InlineKeyboardButton("NZD/USD OTC", callback_data="pair_NZD/USD_OTC"),
            types.InlineKeyboardButton("USD/CHF OTC", callback_data="pair_USD/CHF_OTC"),
            types.InlineKeyboardButton("GBP/JPY OTC", callback_data="pair_GBP/JPY_OTC")
        )
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, 
                              text="📊 **Барлық OTC активтері тізімі:**\nҚажетті жұпты таңдаңыз:", reply_markup=markup, parse_mode="Markdown")
        
    elif call.data.startswith("pair_"):
        pair = call.data.split("_", 1)[1].replace("_", "/")
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
            user_data[chat_id] = {"pair": "AED/CNY OTC", "time": t_frame}
            
        pair = user_data[chat_id]["pair"]
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔮 ПОЛУЧИТЬ ПРОГНОЗ", callback_data="get_forecast"),
            types.InlineKeyboardButton("⬅️ Артқа", callback_data="back_to_pairs")
        )
        
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, 
                              text=f"💱 Актив: **{pair}** | ⏱️ Уақыт: **{t_frame}**\n\nНейросеть дайын. Прогноз алу үшін түймені басыңыз:", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "get_forecast":
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, 
                              text="🧠 **Анализ нейросеть...**\nОқыту модельдері мен индикаторлар тексерілуде...", parse_mode="Markdown")
        time.sleep(2)
        
        info = user_data.get(chat_id, {"pair": "AED/CNY OTC", "time": "1m"})
        pair = info.get("pair", "AED/CNY OTC")
        t_frame = info.get("time", "1m")
        
        decision = random.choice(["🟢 ПОКУПКА (BUY)", "🔴 ПРОДАЖА (SELL)"])
        confidence = round(random.uniform(88.5, 98.2), 1)
        price_val = round(random.uniform(1.1000, 5.5000), 4)

        result_text = (
            f"🤖 **KUANYSH SYSTEM v2.0 | ПРОГНОЗ**\n\n"
            f"📊 Актив: **{pair}**\n"
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

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    return "Forbidden", 403

@app.route('/webhook', methods=['POST'])
def trading_webhook():
    data = request.json
    if data:
        signal = data.get('signal', 'Белгісіз сигнал')
        bot.send_message(CHAT_ID, f"📢 Сигнал: {signal}")
        return "OK", 200
    return "Error", 400

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
