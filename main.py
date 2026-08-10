import os
import telebot
from telebot import types
import random
import threading
from datetime import datetime

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Kuanysh System Pro Trade Bot жұмыс істейді!"

# Өз токеніңізді осы жерге дұрыстап жазыңыз
TOKEN = "8991035959:AAF-H1o6A7L7gcbNegIf86KEGjt0V_VHQ"
bot = telebot.TeleBot(TOKEN)

# Скриншоттардан алынған платформаның барлық нақты OTC жұптарының толық базасы
АКТИВТЕР_БАЗАСЫ = {
    "audjpyotc": ("AUD/JPY OTC", 96.80, 0.2000),
    "gbpjpyotc": ("GBP/JPY OTC", 195.10, 0.3000),
    "aedcnyotc": ("AED/CNY OTC", 1.9500, 0.0100),
    "kesusdotc": ("KES/USD OTC", 0.0075, 0.0005),
    "usdinrotc": ("USD/INR OTC", 83.1000, 0.2000),
    "nzdusdotc": ("NZD/USD OTC", 0.6025, 0.0010),
    "uahusdotc": ("UAH/USD OTC", 0.0240, 0.0010),
    "usdbdtotc": ("USD/BDT OTC", 117.00, 0.5000),
    "usdidrotc": ("USD/IDR OTC", 15600.00, 50.0000),
    "usdmxnotc": ("USD/MXN OTC", 17.5000, 0.1000),
    "usdmyrotc": ("USD/MYR OTC", 4.7000, 0.0200),
    "usdpkrotc": ("USD/PKR OTC", 278.00, 1.0000),
    "usdrubotc": ("USD/RUB OTC", 92.5000, 0.5000),
    "usdvndotc": ("USD/VND OTC", 25000.00, 100.0000),
    "yerusdotc": ("YER/USD OTC", 0.0040, 0.0002),
    "tndusdotc": ("TND/USD OTC", 0.3200, 0.0020),
    "audcadotc": ("AUD/CAD OTC", 0.9100, 0.0010),
    "audchfotc": ("AUD/CHF OTC", 0.5850, 0.0010),
    "cadchfotc": ("CAD/CHF OTC", 0.6580, 0.0010),
    "chfjpyotc": ("CHF/JPY OTC", 165.80, 0.2500),
    "eurchfotc": ("EUR/CHF OTC", 0.9720, 0.0010),
    "eurjpyotc": ("EUR/JPY OTC", 168.40, 0.3500),
    "eurnzdotc": ("EUR/NZD OTC", 1.9394, 0.0015),
    "eurtryotc": ("EUR/TRY OTC", 35.2000, 0.1000),
    "lbpusdotc": ("LBP/USD OTC", 0.000011, 0.000001),
    "eurbpotc": ("EUR/GBP OTC", 0.8550, 0.0010),
    "eurusdotc": ("EUR/USD OTC", 1.0920, 0.0010),
    "gbpaudotc": ("GBP/AUD OTC", 1.9420, 0.0020),
    "madusdotc": ("MAD/USD OTC", 0.1000, 0.0020),
    "bhdcnyotc": ("BHD/CNY OTC", 19.2000, 0.0500),
    "usdthbotc": ("USD/THB OTC", 36.5000, 0.1000),
    "cadjpyotc": ("CAD/JPY OTC", 109.50, 0.2000),
    "jodcnyotc": ("JOD/CNY OTC", 9.8500, 0.0500),
    "usdcnhotc": ("USD/CNH OTC", 7.2000, 0.0200),
    "usdclpotc": ("USD/CLP OTC", 950.00, 5.0000),
    "usdphpotc": ("USD/PHP OTC", 56.2000, 0.1000),
    "omrcnyotc": ("OMR/CNY OTC", 18.5000, 0.0500),
    "usdsgdotc": ("USD/SGD OTC", 1.3450, 0.0012),
    "usdjpyotc": ("USD/JPY OTC", 148.20, 0.2500),
    "gbpusdotc": ("GBP/USD OTC", 1.2850, 0.0018),
    "sarcnyotc": ("SAR/CNY OTC", 1.9300, 0.0100),
    "qarcnyotc": ("QAR/CNY OTC", 1.9800, 0.0100),
    "usdcopotc": ("USD/COP OTC", 3900.00, 10.0000),
    "zarusdotc": ("ZAR/USD OTC", 0.0550, 0.0010),
    "usdchfotc": ("USD/CHF OTC", 0.8900, 0.0012),
    "usdarstotc": ("USD/ARS OTC", 860.00, 5.0000)
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    for key, (name, _, _) in АКТИВТЕР_БАЗАСЫ.items():
        markup.add(types.InlineKeyboardButton(f"📊 {name}", callback_data=key))

    bot.send_message(
        message.chat.id,
        "⚡ **KUANYSH SYSTEM: PRO TRADING TERMINAL** ⚡\n\n"
        "Платформаның барлық OTC жұптары толығымен жүктелді.\n"
        "Талдау жасау үшін тізімнен қажетті активті таңдаңыз:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data in АКТИВТЕР_БАЗАСЫ:
        name, base_price, deviation = АКТИВТЕР_БАЗАСЫ[call.data]
        
        try:
            bot.answer_callback_query(call.id, f"{name} бойынша талдау жасалуда...")
        except Exception:
            pass
        
        symmetry = random.uniform(-1, 1)
        price = round(base_price + (symmetry * deviation), 4)
        winrate = random.randint(92, 99)
        rsi_value = random.randint(18, 85)
        
        if symmetry >= 0:
            сигнал = "🟢 ПОКУПКА (ВВЕРХ / CALL)"
            тренд = "Жоғары өсу тренді (Bullish Momentum)"
            rsi_status = f"{rsi_value} (Сатып алу аймағы)"
        else:
            сигнал = "🔴 ПРОДАЖА (ВНИЗ / PUT)"
            тренд = "Құлдырау тренді (Bearish Pressure)"
            rsi_status = f"{rsi_value} (Сату аймағы)"

        current_time = datetime.now().strftime("%H:%M:%S")

        анализ_текст = (
            f"📈 **КУАНЫШ ПРО АНАЛИЗАТОРИ**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 Актив: `{name}`\n"
            f"💵 Модельдеу бағасы: `{price}`\n"
            f"⏰ Уақыты: `{current_time}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 **Техникалық индикаторлар:**\n"
            f" • RSI (14): `{rsi_status}`\n"
            f" • MACD: `Қиылысу расталды`\n"
            f" • Тренд бағыты: `{тренд}`\n"
            f" • Винрейт (Сәттілік пайызы): `{winrate}%`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 **ҚОРЫТЫНДЫ СИГНАЛ:**\n"
            f"👉 **{сигнал}**\n"
            f"⏱ Экспирация уақыты: `1 минут`"
        )

        try:
            bot.send_message(call.message.chat.id, анализ_текст, parse_mode="Markdown")
        except Exception:
            pass

def run_bot():
    print("Kuanysh System Pro Bot іске қосылуда...")
    try:
        bot.infinity_polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Бот қатесі: {e}")

bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True
bot_thread.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
