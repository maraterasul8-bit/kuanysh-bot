import telebot
import yfinance as yf
import pandas as pd
from telebot import types

# Сіздің Telegram бот токеніңіз
TOKEN = "8991039569:AAGAcAeR0mj5acvbiGVWfxdNO1m9PBgi-lA"
bot = telebot.TeleBot(TOKEN)

# /start командасы — барлық активтер тізімі және ескі пернетақтаны өшіру
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Ескі астыңғы батырмаларды тазалау
    remove_markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "⏳ Жүйе іске қосылуда...", reply_markup=remove_markup)

    # Inline батырмалар (барлық қосылған активтер)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    assets = [
        ("📊 EUR/USD", "eurusd"),
        ("📊 GBP/USD", "gbpusd"),
        ("📊 USD/JPY", "usdjpy"),
        ("📊 AUD/USD", "audusd"),
        ("📊 USD/CAD", "usdcad"),
        ("📊 USD/CHF", "usdchf"),
        ("📊 EUR/JPY", "eurjpy"),
        ("📊 GBP/JPY", "gbpjpy"),
        ("📊 AUD/JPY", "audjpy"),
        ("📊 CAD/JPY", "cadjpy"),
        ("📊 EUR/CHF", "eurchf"),
        ("📊 EUR/GBP", "eurgbp"),
        ("📊 GBP/CAD", "gbpcad"),
        ("📊 GBP/CHF", "gbpchf"),
        ("📊 AUD/CAD", "audcad"),
        ("📊 AUD/CHF", "audchf"),
        ("📊 EUR/AUD", "euraud"),
        ("📊 GBP/AUD", "gbpaud"),
        ("📊 CAD/CHF", "cadchf"),
        ("📊 CHF/JPY", "chfjpy"),
        ("📊 NZD/USD", "nzdusd"),
        ("📊 NZD/JPY", "nzdjpy"),
        ("📊 AUD/NZD", "audnzd"),
        ("📊 EUR/NZD", "eurnzd"),
        # OTC активтері
        ("📊 EUR/USD OTC", "eurusdotc"),
        ("📊 GBP/USD OTC", "gbpusdotc"),
        ("📊 USD/JPY OTC", "usdjpyotc"),
        ("📊 USD/CAD OTC", "usdcadotc"),
        ("📊 USD/CHF OTC", "usdchfotc"),
        ("📊 EUR/RUB OTC", "eurbro"),
        ("📊 USD/RUB OTC", "usdrubotc"),
        ("📊 USD/BRL OTC", "usdbrlotc"),
        ("📊 USD/MXN OTC", "usdmxnotc"),
        ("📊 AED/CNY OTC", "aedcnyotc"),
        ("📊 USD/INR OTC", "usdinrotc"),
        ("📊 USD/PKR OTC", "usdpkrotc"),
        ("📊 USD/PHP OTC", "usdphpotc"),
        ("📊 CHF/NOK OTC", "chfnokotc"),
        ("📊 SAR/CNY OTC", "sarcnyotc"),
        ("📊 AUD/NZD OTC", "audnzdotc"),
        ("📊 USD/MYR OTC", "usdmyrotc"),
        ("📊 EUR/GBP OTC", "eurgbpotc"),
        ("📊 EUR/JPY OTC", "eurjpyotc"),
        ("📊 USD/CNH OTC", "usdcnhotc"),
        ("📊 USD/ARS OTC", "usdarsotc"),
        ("📊 CHF/JPY OTC", "chfjpyotc"),
        ("📊 GOLD", "gold")
    ]
    
    buttons = [types.InlineKeyboardButton(text, callback_data=data) for text, data in assets]
    markup.add(*buttons)
    
    bot.send_message(
        message.chat.id, 
        "🚀 **KUANYSH TRADING SYSTEM**\n\nТөмендегі тізімнен анализ жасайтын активті таңдаңыз:", 
        reply_markup=markup, 
        parse_mode="Markdown"
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
        "usdchf": ("USD/CHF", "USDCHF=X"),
        "eurjpy": ("EUR/JPY", "EURJPY=X"),
        "gbpjpy": ("GBP/JPY", "GBPJPY=X"),
        "audjpy": ("AUD/JPY", "AUDJPY=X"),
        "cadjpy": ("CAD/JPY", "CADJPY=X"),
        "eurchf": ("EUR/CHF", "EURCHF=X"),
        "eurgbp": ("EUR/GBP", "EURGBP=X"),
        "gbpcad": ("GBP/CAD", "GBPCAD=X"),
        "gbpchf": ("GBP/CHF", "GBPCHF=X"),
        "audcad": ("AUD/CAD", "AUDCAD=X"),
        "audchf": ("AUD/CHF", "AUDCHF=X"),
        "euraud": ("EUR/AUD", "EURAUD=X"),
        "gbpaud": ("GBP/AUD", "GBPAUD=X"),
        "cadchf": ("CAD/CHF", "CADCHF=X"),
        "chfjpy": ("CHF/JPY", "CHFJPY=X"),
        "nzdusd": ("NZD/USD", "NZDUSD=X"),
        "nzdjpy": ("NZD/JPY", "NZDJPY=X"),
        "audnzd": ("AUD/NZD", "AUDNZD=X"),
        "eurnzd": ("EUR/NZD", "EURNZD=X"),
        # OTC карталары
        "eurusdotc": ("EUR/USD OTC", "EURUSD=X"),
        "gbpusdotc": ("GBP/USD OTC", "GBPUSD=X"),
        "usdjpyotc": ("USD/JPY OTC", "USDJPY=X"),
        "usdcadotc": ("USD/CAD OTC", "USDCAD=X"),
        "usdchfotc": ("USD/CHF OTC", "USDCHF=X"),
        "eurbro": ("EUR/RUB OTC", "EURRUB=X"),
        "usdrubotc": ("USD/RUB OTC", "USDRUB=X"),
        "usdbrlotc": ("USD/BRL OTC", "BRL=X"),
        "usdmxnotc": ("USD/MXN OTC", "MXN=X"),
        "aedcnyotc": ("AED/CNY OTC", "CNY=X"),
        "usdinrotc": ("USD/INR OTC", "USDINR=X"),
        "usdpkrotc": ("USD/PKR OTC", "USDPKR=X"),
        "usdphpotc": ("USD/PHP OTC", "USDPHP=X"),
        "chfnokotc": ("CHF/NOK OTC", "CHFNOK=X"),
        "sarcnyotc": ("SAR/CNY OTC", "SAR=X"),
        "audnzdotc": ("AUD/NZD OTC", "AUDNZD=X"),
        "usdmyrotc": ("USD/MYR OTC", "USDMYR=X"),
        "eurgbpotc": ("EUR/GBP OTC", "EURGBP=X"),
        "eurjpyotc": ("EUR/JPY OTC", "EURJPY=X"),
        "usdcnhotc": ("USD/CNH OTC", "USDCNH=X"),
        "usdarsotc": ("USD/ARS OTC", "USDARS=X"),
        "chfjpyotc": ("CHF/JPY OTC", "CHFJPY=X"),
        "gold": ("GOLD", "GC=F")
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
    try:
        bot.remove_webhook()
    except:
        pass
    bot.infinity_polling()
    
