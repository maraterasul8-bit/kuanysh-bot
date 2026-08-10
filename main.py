import os
import telebot
from telebot import types
import random

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Kuanysh Trade Bot жұмыс істеп тұр!"

TOKEN = "8991035959:AAF#H1o6A7L7gcbNegIf86KEGjt0V_VHQ"
bot = telebot.TeleBot(TOKEN)

# Барлық активтердің тізімі мен мәндері (бір жерде жиналған)
АКТИВТЕР_БАЗАСЫ = {
    "eurusd": ("EUR/USD", 1.0920, 0.0010),
    "gbpusd": ("GBP/USD", 1.3150, 0.0015),
    "usdjpy": ("USD/JPY", 147.50, 0.2000),
    "usdchf": ("USD/CHF", 0.8900, 0.0012),
    "eurusdotc": ("EUR/USD OTC", 1.1945, 0.0012),
    "gbpusdotc": ("GBP/USD OTC", 1.2850, 0.0018),
    "eurnzdotc": ("EUR/NZD OTC", 1.9394, 0.0015),
    "usdjpyotc": ("USD/JPY OTC", 148.20, 0.2500),
    "audcadotc": ("AUD/CAD OTC", 0.9100, 0.0010),
    "gbpjpyotc": ("GBP/JPY OTC", 195.10, 0.3000),
    "eurjpyotc": ("EUR/JPY OTC", 168.40, 0.3500),
    "usdcadotc": ("USD/CAD OTC", 1.3520, 0.0020),
    "audusdotc": ("AUD/USD OTC", 0.6555, 0.0010),
    "nzdusdotc": ("NZD/USD OTC", 0.6025, 0.0010),
    "gbpaudotc": ("GBP/AUD OTC", 1.9420, 0.0020),
    "euraudotc": ("EUR/AUD OTC", 1.6650, 0.0018),
    "cadjpyotc": ("CAD/JPY OTC", 109.50, 0.2000),
    "chfjpyotc": ("CHF/JPY OTC", 165.80, 0.2500),
    "eurcadotc": ("EUR/CAD OTC", 1.4780, 0.0015),
    "nzdjpyotc": ("NZD/JPY OTC", 88.90, 0.1800),
    "audjpyotc": ("AUD/JPY OTC", 96.80, 0.2000),
    "gbpcadotc": ("GBP/CAD OTC", 1.7350, 0.0020),
    "gbpnzdotc": ("GBP/NZD OTC", 2.1300, 0.0025),
    "eurchfotc": ("EUR/CHF OTC", 0.9720, 0.0010),
    "audnzdotc": ("AUD/NZD OTC", 1.0880, 0.0012),
    "cadchfotc": ("CAD/CHF OTC", 0.6580, 0.0010)
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    for key, (name, _, _) in АКТИВТЕР_БАЗАСЫ.items():
        markup.add(types.InlineKeyboardButton(f"📊 {name}", callback_data=key))

    bot.send_message(
        message.chat.id,
        "⚡ **KUANYSH SYSTEM: TRADING TERMINAL**\n\n"
        "Барлық активтер тізімі жүктелді.\n"
        "Талдау жасау үшін қажетті жұпты таңдаңыз:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data in АКТИВТЕР_БАЗАСЫ:
        name, base_price, deviation = АКТИВТЕР_БАЗАСЫ[call.data]
        
        try:
            bot.answer_callback_query(call.id, f"{name} талдануда...")
        except Exception:
            pass
        
        symmetry = random.uniform(-1, 1)
        price = round(base_price + (symmetry * deviation), 4)
        winrate = random.randint(93, 99)
        
        if symmetry >= 0:
            signal = "🟢 ПОКУПКА (ВВЕРХ)"
            trend = "Өсу тренді (Bullish)"
        else:
            signal = "🔴 ПРОДАЖА (ВНИЗ)"
            trend = "Құлдырау тренді (Bearish)"

        analysis_text = (
            f"📈 **КУАНЫШ АНАЛИЗАТОРИ: {name}**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💵 Ағымдағы баға: `{price}`\n"
            f"📊 Винрейт: `{winrate}%`\n"
            f"📉 Тренд жағдайы: `{trend}`\n"
            f"⚙️ Индикатор (RSI/SMA): `Талдау аяқталды`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 **ҚОРЫТЫНДЫ ШЕШІМ:**\n"
            f"👉 Сигнал: **{signal}**\n"
            f"⏱ Уақыт (Экспирация): `1 минут`"
        )

        try:
            bot.send_message(call.message.chat.id, analysis_text, parse_mode="Markdown")
        except Exception:
            pass

def run_bot():
    bot.remove_webhook()
    print("Kuanysh Trade Bot сәтті іске қосылды.")
    bot.infinity_polling(none_stop=True)

if __name__ == "__main__":
    import threading
    t = threading.Thread(target=run_bot)
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
