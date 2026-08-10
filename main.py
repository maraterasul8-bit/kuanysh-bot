import telebot
import yfinance as yf
import pandas as pd
from telebot import types

# Боттың токені
TOKEN = "8991039569:AAGAcAeR0mj5acvbiGVWfxdNO1m9PBgi-lA"
bot = telebot.TeleBot(TOKEN)

# /start командасы — барлық активтер тізімі
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Негізгі активтер тізімі
    assets = [
        ("📊 EUR/USD", "eurusd"),
        ("📊 GBP/USD", "gbpusd"),
        ("📊 USD/JPY", "usdjpy"),
        ("📊 AUD/USD", "audusd"),
        ("📊 USD/CAD", "usdcad"),
        ("📊 AED/CNY OTC", "aedcny"),
        ("📊 EUR/USD OTC", "eurusdotc"),
        ("📊 GBP/USD OTC", "gbpusdotc"),
        ("📊 GOLD", "gold"),
        ("📊 USD/BRL OTC", "usdbrlotc"),
        ("📊 USD/MXN OTC", "usdmxnotc"),
        ("📊 USD/JPY OTC", "usdjpyotc")
    ]
    
    buttons = [types.InlineKeyboardButton(text, callback_data=data) for text, data in assets]
    markup.add(*buttons)
    
    bot.send_message(
        message.chat.id, 
        "🚀 **KUANYSH TRADING SYSTEM**\n\nТөмендегі тізімнен анализ жасайтын активті таңдаңыз:", 
        reply_markup=markup, 
        parse_Mode="Markdown"
    )

# Батырмалар басқан кездегі әрекеттер
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    symbol_map = {
        "eurusd": ("EUR/USD", "EURUSD=X"),
        "gbpusd": ("GBP/USD", "GBPUSD=X"),
        "usdjpy": ("USD/JPY", "USDJPY=X"),
        "audusd": ("AUD/USD", "AUDUSD=X"),
        "usdcad": ("USD/CAD", "USDCAD=X"),
        "aedcny": ("AED/CNY OTC", "CNY=X"), # Символ баламасы
        "eurusdotc": ("EUR/USD OTC", "EURUSD=X"),
        "gbpusdotc": ("GBP/USD OTC", "GBPUSD=X"),
        "gold": ("GOLD", "GC=F"),
        "usdbrlotc": ("USD/BRL OTC", "BRL=X"),
        "usdmxnotc": ("USD/MXN OTC", "MXN=X"),
        "usdjpyotc": ("USD/JPY OTC", "USDJPY=X")
    }
    
    if call.data in symbol_map:
        name, ticker = symbol_map[call.data]
        bot.answer_callback_query(call.id, f"{name} таңдалды")
        bot.send_message(call.message.chat.id, f"⏳ {name} бойынша нарық деректері тексеріліп жатыр...")
        
        # Нарық анализін орындау
        analysis_result = analyze_market(ticker, name)
        bot.send_message(call.message.chat.id, analysis_result, parse_mode="Markdown")

# Нарықты талдау функциясы
def analyze_market(ticker, name):
    try:
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        if data.empty:
            return f"⚠️ {name} үшін нарық деректері табылмады."
        
        last_close = float(data['Close'].iloc[-1])
        prev_close = float(data['Close'].iloc[-2])
        
        if last_close > prev_close:
            signal = "🟢 ПОКУПКА (Өсу тренді)"
        else:
            signal = "🔴 ПРОДАЖА (Құлау тренді)"
            
        result = (
            f"📈 **Нарық анализі ({name}):**\n"
            f"💵 Соңғы баға: {last_close:.5f}\n"
            f"🎯 Сигнал: **{signal}**"
        )
        return result
    except Exception as e:
        return f"❌ Анализ жасау кезінде қате шықты: {str(e)}"

if __name__ == '__main__':
    bot.infinity_polling()
        
