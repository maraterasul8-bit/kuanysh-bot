import telebot
import yfinance as yf
from telebot import types

# Жаңа бот токені
TOKEN = "8991039569:AAFoH1ooA7Ls7gcbNeglT86KEGjEoV_VHqQ"
bot = telebot.TeleBot(TOKEN)

# Start командасы
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    assets = [
        ("📊 EUR/USD", "eurusd"), ("📊 GBP/USD", "gbpusd"), ("📊 USD/JPY", "usdjpy"),
        ("📊 USD/CAD", "usdcad"), ("📊 USD/CHF", "usdchf"), ("📊 EUR/JPY", "eurjpy"),
        ("📊 GBP/JPY", "gbpjpy"), ("📊 AUD/JPY", "audjpy"), ("📊 CAD/JPY", "cadjpy"),
        ("📊 EUR/CHF", "eurchf"), ("📊 EUR/GBP", "eurgbp"), ("📊 GBP/CAD", "gbpcad"),
        ("📊 GBP/CHF", "gbpchf"), ("📊 AUD/CAD", "audcad"), ("📊 AUD/CHF", "audchf"),
        ("📊 EUR/AUD", "euraud"), ("📊 GBP/AUD", "gbpaud"), ("📊 CAD/CHF", "cadchf"),
        ("📊 CHF/JPY", "chfjpy"), ("📊 NZD/USD", "nzdusd"), ("📊 NZD/JPY", "nzdjpy"),
        ("📊 AUD/NZD", "audnzd"), ("📊 EUR/NZD", "eurnzd"), ("📊 GOLD", "gold"),
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
    
    bot.send_message(message.chat.id, "🚀 **KUANYSH TRADING SYSTEM**\n\nАктивті таңдаңыз:", 
                     reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    symbol_map = {
        "eurusd": ("EUR/USD", "EURUSD=X"), "gbpusd": ("GBP/USD", "GBPUSD=X"),
        "usdjpy": ("USD/JPY", "USDJPY=X"), "usdcad": ("USD/CAD", "USDCAD=X"),
        "usdchf": ("USD/CHF", "USDCHF=X"), "eurjpy": ("EUR/JPY", "EURJPY=X"),
        "gbpjpy": ("GBP/JPY", "GBPJPY=X"), "audjpy": ("AUD/JPY", "AUDJPY=X"),
        "cadjpy": ("CAD/JPY", "CADJPY=X"), "eurchf": ("EUR/CHF", "EURCHF=X"),
        "eurgbp": ("EUR/GBP", "EURGBP=X"), "gbpcad": ("GBP/CAD", "GBPCAD=X"),
        "gbpchf": ("GBP/CHF", "GBPCHF=X"), "audcad": ("AUD/CAD", "AUDCAD=X"),
        "audchf": ("AUD/CHF", "AUDCHF=X"), "euraud": ("EUR/AUD", "EURAUD=X"),
        "gbpaud": ("GBP/AUD", "GBPAUD=X"), "cadchf": ("CAD/CHF", "CADCHF=X"),
        "chfjpy": ("CHF/JPY", "CHFJPY=X"), "nzdusd": ("NZD/USD", "NZDUSD=X"),
        "nzdjpy": ("NZD/JPY", "NZDJPY=X"), "audnzd": ("AUD/NZD", "AUDNZD=X"),
        "eurnzd": ("EUR/NZD", "EURNZD=X"), "gold": ("GOLD", "GC=F"),
        "eurusdotc": ("EUR/USD OTC", "EURUSD=X"), "gbpusdotc": ("GBP/USD OTC", "GBPUSD=X"),
        "usdjpyotc": ("USD/JPY OTC", "USDJPY=X"), "usdcadotc": ("USD/CAD OTC", "USDCAD=X"),
        "usdchfotc": ("USD/CHF OTC", "USDCHF=X"), "eurbro": ("EUR/RUB OTC", "EURRUB=X"),
        "usdrubotc": ("USD/RUB OTC", "USDRUB=X"), "usdbrlotc": ("USD/BRL OTC", "BRL=X"),
        "usdmxnotc": ("USD/MXN OTC", "MXN=X"), "aedcnyotc": ("AED/CNY OTC", "CNY=X"),
        "usdinrotc": ("USD/INR OTC", "USDINR=X"), "usdpkrotc": ("USD/PKR OTC", "USDPKR=X"),
        "usdphpotc": ("USD/PHP OTC", "USDPHP=X"), "chfnokotc": ("CHF/NOK OTC", "CHFNOK=X"),
        "sarcnyotc": ("SAR/CNY OTC", "SAR=X"), "audnzdotc": ("AUD/NZD OTC", "AUDNZD=X"),
        "usdmyrotc": ("USD/MYR OTC", "USDMYR=X"), "eurgbpotc": ("EUR/GBP OTC", "EURGBP=X"),
        "eurjpyotc": ("EUR/JPY OTC", "EURJPY=X"), "usdcnhotc": ("USD/CNH OTC", "USDCNH=X"),
        "usdarsotc": ("USD/ARS OTC", "USDARS=X"), "chfjpyotc": ("CHF/JPY OTC", "CHFJPY=X")
    }
    
    if call.data in symbol_map:
        name, ticker = symbol_map[call.data]
        bot.answer_callback_query(call.id, f"{name} таңдалды")
        try:
            data = yf.download(ticker, period="1d", interval="1m", progress=False)
            last_close = float(data['Close'].iloc[-1])
            prev_close = float(data['Close'].iloc[-2])
            signal = "🟢 ПОКУПКА" if last_close > prev_close else "🔴 ПРОДАЖА"
            bot.send_message(call.message.chat.id, f"📈 **{name}**\n💵 Баға: {last_close:.5f}\n🎯 Сигнал: **{signal}**", parse_mode="Markdown")
        except:
            bot.send_message(call.message.chat.id, "❌ Деректерді алу мүмкін болмады.")

if __name__ == '__main__':
    bot.remove_webhook()
    print("Bot is running...")
    bot.infinity_polling(none_stop=True)
        
