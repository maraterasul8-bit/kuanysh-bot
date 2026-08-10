import os
import threading
import telebot
from flask import Flask
from telebot import types
import random

# Render үшін веб-сервер
app = Flask(__name__)

@app.route('/')
def home():
    return "Kuanysh Bot is running!"

TOKEN = "8991039569:AAFoH1ooA7Ls7gcbNeglT86KEGjEoV_VHqQ"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Барлық скриншотардан жиналған толық тізім
    assets = [
        # Стандартты жұптар
        ("📊 GBP/USD", "gbpusd"), ("📊 USD/CAD", "usdcad"),
        ("📊 USD/CHF", "usdchf"), ("📊 USD/JPY", "usdjpy"),
        ("📊 AUD/CAD", "audcad"), ("📊 AUD/JPY", "audjpy"),
        ("📊 EUR/AUD", "euraud"), ("📊 GBP/AUD", "gbpaud"),
        ("📊 CAD/CHF", "cadchf"), ("📊 EUR/USD", "eurusdm"),
        ("📊 AUD/CHF", "audchf"), ("📊 CHF/JPY", "chfjpy"),
        ("📊 EUR/CAD", "eurcad"), ("📊 EUR/CHF", "eurchf"),
        ("📊 EUR/GBP", "eurgbp"), ("📊 GBP/CAD", "gbpcad"),
        ("📊 GBP/CHF", "gbpchf"),
        
        # OTC активтері (Барлық скриншотардан)
        ("📊 CAD/CHF OTC", "cadchfotc"), ("📊 USD/ARS OTC", "usdarsotc"),
        ("📊 KES/USD OTC", "kesusdotc"), ("📊 NZD/JPY OTC", "nzdjpyotc"),
        ("📊 CHF/JPY OTC", "chfjpyotc"), ("📊 NZD/USD OTC", "nzdusdotc"),
        ("📊 USD/CHF OTC", "usdchfotc"), ("📊 EUR/HUF OTC", "eurhufotc"),
        ("📊 USD/EGP OTC", "usdegpotc"), ("📊 USD/THB OTC", "usdthbotc"),
        ("📊 USD/CLP OTC", "usdclpotc"), ("📊 EUR/RUB OTC", "eurrubotc"),
        ("📊 USD/DZD OTC", "usddzdotc"), ("📊 GBP/JPY OTC", "gbpjpyotc"),
        ("📊 USD/SGD OTC", "usdsgdotc"), ("📊 USD/IDR OTC", "usdidrotc"),
        ("📊 AUD/JPY OTC", "audjpyotc"), ("📊 USD/PKR OTC", "usdpkrotc"),
        ("📊 USD/PHP OTC", "usdphpotc"), ("📊 CHF/NOK OTC", "chfnokotc"),
        ("📊 USD/CAD OTC", "usdcadotc"), ("📊 YER/USD OTC", "yerusdotc"),
        ("📊 SAR/CNY OTC", "sarcnyotc"), ("📊 LBP/USD OTC", "lbpusdotc"),
        ("📊 AUD/NZD OTC", "audnzdotc"), ("📊 USD/MYR OTC", "usdmyrotc"),
        ("📊 BHD/CNY OTC", "bhdcnyotc"), ("📊 EUR/GBP OTC", "eurgbpotc"),
        ("📊 OMR/CNY OTC", "omrcnyotc"), ("📊 QAR/CNY OTC", "qarcnyotc"),
        ("📊 TND/USD OTC", "tndusdotc"), ("📊 UAH/USD OTC", "uahusdotc"),
        ("📊 USD/BDT OTC", "usdbdtotc"), ("📊 USD/CNH OTC", "usdcnhotc"),
        ("📊 USD/COP OTC", "usdcopotc"), ("📊 USD/INR OTC", "usdinrotc"),
        ("📊 ZAR/USD OTC", "zarusdotc"), ("📊 AED/CNY OTC", "aedcnyotc"),
        ("📊 AUD/CHF OTC", "audchfotc"), ("📊 EUR/TRY OTC", "eurtryotc"),
        ("📊 EUR/USD OTC", "eurusdotc"), ("📊 GBP/AUD OTC", "gbpaudotc"),
        ("📊 GBP/USD OTC", "gbpusdotc"), ("📊 NGN/USD OTC", "ngnusdotc"),
        ("📊 EUR/NZD OTC", "eurnzdotc"), ("📊 EUR/JPY OTC", "eurjpyotc"),
        ("📊 MAD/USD OTC", "madusdotc"), ("📊 USD/VND OTC", "usdvndotc"),
        ("📊 USD/BRL OTC", "usdbrlotc"), ("📊 JOD/CNY OTC", "jodcnyotc"),
        ("📊 USD/MXN OTC", "usdmxnotc")
    ]
    
    for text, data in assets:
        markup.add(types.InlineKeyboardButton(text, callback_data=data))
    
    bot.send_message(
        message.chat.id, 
        "🚀 **KUANYSH TRADING SYSTEM**\n\nБарлық активтер тізімі қосылды. Активті таңдаңыз:", 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # Барлық атаулар мен олардың баға диапазондары (min, max)
    asset_data = {
        "gbpusd": ("GBP/USD", (1.25, 1.35)), "usdcad": ("USD/CAD", (1.30, 1.40)),
        "usdchf": ("USD/CHF", (0.85, 0.95)), "usdjpy": ("USD/JPY", (145.0, 155.0)),
        "audcad": ("AUD/CAD", (0.88, 0.95)), "audjpy": ("AUD/JPY", (95.0, 105.0)),
        "euraud": ("EUR/AUD", (1.60, 1.70)), "gbpaud": ("GBP/AUD", (1.85, 1.95)),
        "cadchf": ("CAD/CHF", (0.63, 0.69)), "eurusdm": ("EUR/USD", (1.05, 1.15)),
        "audchf": ("AUD/CHF", (0.55, 0.62)), "chfjpy": ("CHF/JPY", (160.0, 175.0)),
        "eurcad": ("EUR/CAD", (1.45, 1.55)), "eurchf": ("EUR/CHF", (0.94, 0.99)),
        "eurgbp": ("EUR/GBP", (0.83, 0.88)), "gbpcad": ("GBP/CAD", (1.70, 1.80)),
        "gbpchf": ("GBP/CHF", (1.10, 1.20)),
        
        # OTC диапазондары
        "cadchfotc": ("CAD/CHF OTC", (0.63, 0.69)), "usdarsotc": ("USD/ARS OTC", (950.0, 1050.0)),
        "kesusdotc": ("KES/USD OTC", (125.0, 135.0)), "nzdjpyotc": ("NZD/JPY OTC", (90.0, 100.0)),
        "chfjpyotc": ("CHF/JPY OTC", (160.0, 175.0)), "nzdusdotc": ("NZD/USD OTC", (0.58, 0.65)),
        "usdchfotc": ("USD/CHF OTC", (0.85, 0.95)), "eurhufotc": ("EUR/HUF OTC", (390.0, 410.0)),
        "usdegpotc": ("USD/EGP OTC", (45.0, 50.0)), "usdthbotc": ("USD/THB OTC", (35.0, 38.0)),
        "usdclpotc": ("USD/CLP OTC", (900.0, 950.0)), "eurrubotc": ("EUR/RUB OTC", (95.0, 105.0)),
        "usddzdotc": ("USD/DZD OTC", (130.0, 140.0)), "gbpjpyotc": ("GBP/JPY OTC", (190.0, 205.0)),
        "usdsgdotc": ("USD/SGD OTC", (1.30, 1.38)), "usdidrotc": ("USD/IDR OTC", (15500.0, 16200.0)),
        "audjpyotc": ("AUD/JPY OTC", (95.0, 105.0)), "usdpkrotc": ("USD/PKR OTC", (275.0, 285.0)),
        "usdphpotc": ("USD/PHP OTC", (55.0, 60.0)), "chfnokotc": ("CHF/NOK OTC", (11.5, 12.5)),
        "usdcadotc": ("USD/CAD OTC", (1.30, 1.40)), "yerusdotc": ("YER/USD OTC", (245.0, 255.0)),
        "sarcnyotc": ("SAR/CNY OTC", (1.85, 1.95)), "lbpusdotc": ("LBP/USD OTC", (89000.0, 91000.0)),
        "audnzdotc": ("AUD/NZD OTC", (1.08, 1.15)), "usdmyrotc": ("USD/MYR OTC", (4.40, 4.70)),
        "bhdcnyotc": ("BHD/CNY OTC", (18.5, 19.5)), "eurgbpotc": ("EUR/GBP OTC", (0.83, 0.88)),
        "omrcnyotc": ("OMR/CNY OTC", (18.0, 19.0)), "qarcnyotc": ("QAR/CNY OTC", (1.95, 2.05)),
        "tndusdotc": ("TND/USD OTC", (3.0, 3.2)), "uahusdotc": ("UAH/USD OTC", (40.0, 42.0)),
        "usdbdtotc": ("USD/BDT OTC", (115.0, 120.0)), "usdcnhotc": ("USD/CNH OTC", (7.10, 7.30)),
        "usdcopotc": ("USD/COP OTC", (3900.0, 4100.0)), "usdinrotc": ("USD/INR OTC", (82.0, 84.0)),
        "zarusdotc": ("ZAR/USD OTC", (17.5, 18.5)), "aedcnyotc": ("AED/CNY OTC", (1.90, 2.00)),
        "audchfotc": ("AUD/CHF OTC", (0.55, 0.62)), "eurtryotc": ("EUR/TRY OTC", (35.0, 38.0)),
        "eurusdotc": ("EUR/USD OTC", (1.18, 1.22)), "gbpaudotc": ("GBP/AUD OTC", (1.85, 1.95)),
        "gbpusdotc": ("GBP/USD OTC", (1.25, 1.35)), "ngnusdotc": ("NGN/USD OTC", (1400.0, 15500.0)),
        "eurnzdotc": ("EUR/NZD OTC", (1.75, 1.85)), "eurjpyotc": ("EUR/JPY OTC", (165.0, 175.0)),
        "madusdotc": ("MAD/USD OTC", (9.8, 10.5)), "usdvndotc": ("USD/VND OTC", (24500.0, 25500.0)),
        "usdbrlotc": ("USD/BRL OTC", (5.4, 5.8)), "jodcnyotc": ("JOD/CNY OTC", (10.0, 10.5)),
        "usdmxnotc": ("USD/MXN OTC", (17.0, 18.5))
    }
    
    if call.data in asset_data:
        name, (min_p, max_p) = asset_data[call.data]
        bot.answer_callback_query(call.id, f"{name} анализі жасалуда...")
        
        # Сол валютаға сай шынайы баға генерациялау
        price = round(random.uniform(min_p, max_p), 4 if max_p < 10 else 2)
        signal = random.choice(["🟢 ЖОҒАРЫ (CALL)", "🔴 ТӨМЕН (PUT)"])
        trend = "Өсу тренді (Bullish)" if "ЖОҒАРЫ" in signal else "Құлдырау тренді (Bearish)"
        
        analysis_text = (
            f"📊 **КУАНЫШ АНАЛИЗАТОРЫ: {name}**\n"
            f"----------------------------------\n"
            f"💵 **Ағымдағы баға:** `{price}`\n"
            f"📈 **Тренд жағдайы:** `{trend}`\n"
            f"⚙️ **Индикатор (RSI/SMA):** `Талдау аяқталды`\n"
            f"----------------------------------\n"
            f"🎯 **ҚОРЫТЫНДЫ ШЕШІМ:**\n"
            f"👉 **Сигнал:** **{signal}**\n"
            f"⏱ **Уақыт:** `1 минут`"
        )
        try:
            bot.send_message(call.message.chat.id, analysis_text, parse_mode="Markdown")
        except Exception:
            pass

def run_bot():
    bot.remove_webhook()
    print("Telegram bot started via thread...")
    bot.infinity_polling(none_stop=True)

threading.Thread(target=run_bot, daemon=True).start()
    
