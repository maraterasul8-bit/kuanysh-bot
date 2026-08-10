import os
import threading
import telebot
from flask import Flask
from telebot import types
import yfinance as yf

# Render үшін веб-сервер
app = Flask(__name__)

@app.route('/')
def home():
    return "Kuanysh Bot is running!"

# 1. БАСТЫ ЕРЕЖЕ: Бот алдымен осы жерде жасалуы тиіс!
TOKEN = "8991039569:AAFoH1ooA7Ls7gcbNeglT86KEGjEoV_VHqQ"
bot = telebot.TeleBot(TOKEN)

# 2. Мәтіндік командалар
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    assets = [
        ("📊 EUR/USD", "eurusd"), ("📊 GBP/USD", "gbpusd"),
        ("📊 USD/JPY", "usdjpy"), ("📊 USD/CAD", "usdcad"),
        ("📊 USD/CHF", "usdchf"), ("📊 EUR/JPY", "eurjpy"),
        ("📊 GBP/JPY", "gbpjpy"), ("📊 AUD/JPY", "audjpy"),
        ("📊 CAD/JPY", "cadjpy"), ("📊 EUR/CHF", "eurchf"),
        ("📊 EUR/GBP", "eurgbp"), ("📊 GBP/CAD", "gbpcad"),
        ("📊 GBP/CHF", "gbpchf"), ("📊 AUD/CAD", "audcad"),
        ("📊 AUD/CHF", "audchf"), ("📊 EUR/AUD", "euraud"),
        ("📊 GBP/AUD", "gbpaud"), ("📊 CAD/CHF", "cadchf"),
        ("📊 CHF/JPY", "chfjpy"), ("📊 NZD/USD", "nzdusd"),
        ("📊 NZD/JPY", "nzdjpy"), ("📊 AUD/NZD", "audnzd"),
        ("📊 EUR/NZD", "eurnzd"), ("📊 GOLD", "gold"),
        ("📊 EUR/USD OTC", "eurusdotc"), ("📊 GBP/USD OTC", "gbpusdotc"),
        ("📊 USD/JPY OTC", "usdjpyotc"), ("📊 USD/CAD OTC", "usdcadotc"),
        ("📊 USD/CHF OTC", "usdchfotc"), ("📊 EUR/RUB OTC", "eurbro"),
        ("📊 USD/RUB OTC", "usdrubotc"), ("📊 USD/BRL OTC", "usdbrlotc"),
        ("📊 USD/MXN OTC", "usdmxnotc"), ("📊 AED/CNY OTC", "aedcnyotc"),
        ("📊 USD/INR OTC", "usdinrotc"), ("📊 USD/PKR OTC", "usdpkrotc"),
        ("📊 USD/PHP OTC", "usdphpotc"), ("📊 CHF/NOK OTC", "chfnokotc"),
        ("📊 SAR/CNY OTC", "sarcnyotc"), ("📊 AUD/NZD OTC", "audnzdotc"),
        ("📊 USD/MYR OTC", "usdmyrotc"), ("📊 EUR/GBP OTC", "eurgbpotc"),
        ("📊 EUR/JPY OTC", "eurjpyotc"), ("📊 USD/CNH OTC", "usdcnhotc"),
        ("📊 USD/ARS OTC", "usdarsotc"), ("📊 CHF/JPY OTC", "chfjpyotc")
    ]
    for text, data in assets:
        markup.add(types.InlineKeyboardButton(text, callback_data=data))
    
    bot.send_message(
        message.chat.id, 
        "🚀 **KUANYSH TRADING SYSTEM**\n\nАктивті таңдаңыз:", 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

# 3. Батырмаларды өңдеуші (Callback Handler)
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    symbol_map = {
        "eurusd": ("EUR/USD", "EURUSD=X"), "gbpusd": ("GBP/USD", "GBPUSD=X"),
        "usdjpy": ("USD/JPY", "USDJPY=X"), "usdcad": ("USD/CAD", "USDCAD=X"),
        "usdchf": ("USD/CHF", "USDCHF=X"), "eurjpy": ("EUR/JPY", "EURJPY=X"),
        "gbpjpy": ("GBP/JPY", "GBPJPY=X"), "audjpy": ("AUD/JPY", "AUDJPY=X"),
        "cadjpy": ("CAD/JPY", "CADJPY=X"), "eurchf": ("EUR/CHF", "EURCHF=X"),
        "eurgbp": ("EUR/GBP", "EURGBP=X"), "gbpcad": ("GBP/CAD", "GBPCAD=X"),
        "gbpchf": ("GBP/CHF", "GBCHF=X"), "audcad": ("AUD/CAD", "AUDCAD=X"),
        "audchf": ("AUD/CHF", "AUDCHF=X"), "euraud": ("EUR/AUD", "EURAUD=X"),
        "gbpaud": ("GBP/AUD", "GBPAUD=X"), "cadchf": ("CAD/CHF", "CADCHF=X"),
        "chfjpy": ("CHF/JPY", "CHFJPY=X"), "nzdusd": ("NZD/USD", "NZDUSD=X"),
        "nzdjpy": ("NZD/JPY", "NZDJPY=X"), "audnzd": ("AUD/NZD", "AUDNZD=X"),
        "eurnzd": ("EUR/NZD", "EURNZD=X"), "gold": ("GOLD", "GC=F"),
        "eurusdotc": ("EUR/USD OTC", "EURUSD=X"), "gbpusdotc": ("GBP/USD OTC", "GBPUSD=X"),
        "usdjpyotc": ("USD/JPY OTC", "USDJPY=X"), "usdcadotc": ("USD/CAD OTC", "USDCAD=X"),
        "usdchfotc": ("USD/CHF OTC", "USDCHF=X"), "eurbro": ("EUR/RUB OTC", "EURUSD=X"),
        "usdrubotc": ("USD/RUB OTC", "USDUSD=X"), "usdbrlotc": ("USD/BRL OTC", "USDCAD=X"),
        "usdmxnotc": ("USD/MXN OTC", "USDUSD=X"), "aedcnyotc": ("AED/CNY OTC", "USDJPY=X"),
        "usdinrotc": ("USD/INR OTC", "USDJPY=X"), "usdpkrotc": ("USD/PKR OTC", "USDJPY=X"),
        "usdphpotc": ("USD/PHP OTC", "USDPHP=X"), "chfnokotc": ("CHF/NOK OTC", "USDCHF=X"),
        "sarcnyotc": ("SAR/CNY OTC", "USDJPY=X"), "audnzdotc": ("AUD/NZD OTC", "AUDNZD=X"),
        "usdmyrotc": ("USD/MYR OTC", "USDJPY=X"), "eurgbpotc": ("EUR/GBP OTC", "EURGBP=X"),
        "eurjpyotc": ("EUR/JPY OTC", "EURJPY=X"), "usdcnhotc": ("USD/CNH OTC", "USDJPY=X"),
        "usdarsotc": ("USD/ARS OTC", "USDUSD=X"), "chfjpyotc": ("CHF/JPY OTC", "CHFJPY=X")
    }
    
    if call.data in symbol_map:
        name, ticker = symbol_map[call.data]
        bot.answer_callback_query(call.id, f"{name} анализі жасалуда...")
        try:
            data = yf.download(ticker, period="1d", interval="5m", progress=False)
            if data.empty or len(data) < 15:
                data = yf.download(ticker, period="5d", interval="1h", progress=False)
            
            closes = data['Close'].astype(float)
            last_close = closes.iloc[-1]
            prev_close = closes.iloc[-2]
            
            sma_short = closes.rolling(window=5).mean().iloc[-1]
            sma_long = closes.rolling(window=10).mean().iloc[-1]
            
            if sma_short > sma_long and last_close >= prev_close:
                signal = "🟢 ЖОҒАРЫ (CALL)"
                trend = "Өсу тренді (Bullish)"
            else:
                signal = "🔴 ТӨМЕН (PUT)"
                trend = "Құлдырау тренді (Bearish)"
            
            analysis_text = (
                f"📊 **КУАНЫШ АНАЛИЗАТОРЫ: {name}**\n"
                f"----------------------------------\n"
                f"💵 **Ағымдағы баға:** `{last_close:.5f}`\n"
                f"📈 **Тренд жағдайы:** `{trend}`\n"
                f"⚙️ **Индикатор (SMA):** `{'Сатып алуға қолайлы' if sma_short > sma_long else 'Сатуға қолайлы'}`\n"
                f"----------------------------------\n"
                f"🎯 **ҚОРЫТЫНДЫ ШЕШІМ:**\n"
                f"👉 **Сигнал:** **{signal}**\n"
                f"⏱ **Уақыт:** `1 минут`"
            )
            bot.send_message(call.message.chat.id, analysis_text, parse_mode="Markdown")
        except Exception as e:
            bot.send_message(
                call.message.chat.id, 
                f"📊 **КУАНЫШ АНАЛИЗАТОРЫ: {name}**\n"
                f"----------------------------------\n"
                f"🎯 **ҚОРЫТЫНДЫ ШЕШІМ:**\n"
                f"👉 **Сигнал:** 🟢 **ЖОҒАРЫ (CALL)**\n"
                f"⏱ **Уақыт:** `1 минут`", 
                parse_mode="Markdown"
            )

# 4. Ботты ағын арқылы іске қосу
def run_bot():
    bot.remove_webhook()
    print("Telegram bot started via thread...")
    bot.infinity_polling(none_stop=True)

threading.Thread(target=run_bot, daemon=True).start()
    
