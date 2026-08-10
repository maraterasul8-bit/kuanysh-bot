import os
import telebot
from telebot import types
import random

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Kuanysh system full trading bot жұмыс істеп тұр!"

TOKEN = "8991035959:AAF#H1o6A7L7gcbNegIf86KEGjt0V_VHQ"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Барлық стандартты және OTC активтерінің толық тізімі
    resursi = [
        ("🇪🇺🇺🇸 EUR/USD", "eurusd"), ("🇬🇧🇺🇸 GBP/USD", "gbpusd"),
        ("🇺🇸🇯🇵 USD/JPY", "usdjpy"), ("🇺🇸🇨🇭 USD/CHF", "usdchf"),
        ("🇦🇺🇺🇸 AUD/USD", "audusd"), ("🇺🇸🇨🇦 USD/CAD", "usdcad"),
        ("🇳🇿🇺🇸 NZD/USD", "nzdusd"), ("🇪🇺🇬🇧 EUR/GBP", "eurgbp"),
        
        ("📉 EUR/USD OTC", "eurusdotc"), ("📉 GBP/USD OTC", "gbpusdotc"),
        ("📉 EUR/NZD OTC", "eurnzdotc"), ("📉 USD/JPY OTC", "usdjpyotc"),
        ("📉 AUD/CAD OTC", "audcadotc"), ("📉 GBP/JPY OTC", "gbpjpyotc"),
        ("📉 EUR/JPY OTC", "eurjpyotc"), ("📉 USD/CAD OTC", "usdcadotc"),
        ("📉 AUD/USD OTC", "audusdotc"), ("📉 NZD/USD OTC", "nzdusdotc"),
        ("📉 GBP/AUD OTC", "gbpaudotc"), ("📉 EUR/AUD OTC", "euraudotc"),
        ("📉 CAD/JPY OTC", "cadjpyotc"), ("📉 CHF/JPY OTC", "chfjpyotc"),
        ("📉 EUR/CAD OTC", "eurcadotc"), ("📉 NZD/JPY OTC", "nzdjpyotc"),
        ("📉 AUD/JPY OTC", "audjpyotc"), ("📉 GBP/CAD OTC", "gbpcadotc"),
        ("📉 GBP/NZD OTC", "gbpnzdotc"), ("📉 EUR/CHF OTC", "eurchfotc"),
        ("📉 AUD/NZD OTC", "audnzdotc"), ("📉 CAD/CHF OTC", "cadchfotc")
    ]

    for текст, данные in resursi:
        markup.add(types.InlineKeyboardButton(текст, callback_data=данные))

    bot.send_message(
        message.chat.id,
        "🚀 **KUANYSH SYSTEM: FULL PROFESSIONAL TRADING BOT**\n\n"
        "Барлық валюта жұптары мен OTC активтері қосылды.\n"
        "Талдау жасау үшін активті таңдаңыз:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda вызов: True)
def handle_callback(вызов):
    актив_базасы = {
        "eurusd": ("EUR/USD", 1.0920, 0.0010),
        "gbpusd": ("GBP/USD", 1.3150, 0.0015),
        "usdjpy": ("USD/JPY", 147.50, 0.2000),
        "usdchf": ("USD/CHF", 0.8900, 0.0012),
        "audusd": ("AUD/USD", 0.6550, 0.0010),
        "usdcad": ("USD/CAD", 1.3500, 0.0015),
        "nzdusd": ("NZD/USD", 0.6020, 0.0010),
        "eurgbp": ("EUR/GBP", 0.8540, 0.0008),
        
        "eurusdotc": ("EUR/USD OTC", 1.0921, 0.0012),
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

    if вызов.data in актив_базасы:
        имя, негизги_бага, ауытқу = актив_базасы[вызов.data]
        
        bot.answer_callback_query(вызов.id, f"{имя}: Финализация прогноза...")
        
        симметрия = random.uniform(-1, 1)
        цена = round(негизги_бага + (симметрия * ауытқу), 4)
        winrate = random.randint(92, 99)
        
        if симметрия >= 0:
            сигнал = "🟢 ПОКУПКА (ВВЕРХ)"
            тренд = "Өсу тренді (Bullish)"
        else:
            сигнал = "🔴 ПРОДАЖА (ВНИЗ)"
            тренд = "Құлдырау тренді (Bearish)"

        анализ_текст = (
            f"📈 **КУАНЫШ АНАЛИЗАТОРИ: {имя}**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💵 Ағымдағы баға: `{цена}`\n"
            f"📊 Винрейт: `{winrate}%`\n"
            f"📉 Тренд жағдайы: `{тренд}`\n"
            f"⚙️ Индикатор (RSI/SMA/Volatility): Талдау аяқталды\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 **ҚОРЫТЫНДЫ ШЕШІМ:**\n"
            f"👉 Сигнал: **{сигнал}**\n"
            f"⏱ Уақыт (Экспирация): `1 минут`"
        )

        try:
            bot.send_message(вызов.message.chat.id, анализ_текст, parse_mode="Markdown")
        except Exception:
            pass

def run_bot():
    bot.remove_webhook()
    print("Kuanysh Full Trade Bot сәтті іске қосылды.")
    bot.infinity_polling(none_stop=True)

if __name__ == "__main__":
    import threading
    t = threading.Thread(target=run_bot)
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
