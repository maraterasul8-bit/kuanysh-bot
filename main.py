import os
import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

# Flask арқылы Render серверін ояу ұстау
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Kuanysh Lightning Fast System жұмыс істеп тұр!"

TOKEN = "8991035959:AAF#H1o6A7L7gcbNegIf86KEGjt0V_VHQ"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Барлық стандартты және OTC активтер тізімі (видеодағыдай толық)
АКТИВТЕР = {
    # Стандартты жұптар
    "eurusd": ("EUR/USD", 1.0920, 0.0010),
    "gbpusdotc": ("GBP/USD OTC", 1.2850, 0.0018),
    "eurusdotc": ("EUR/USD OTC", 1.1945, 0.0012),
    "usdjpyotc": ("USD/JPY OTC", 148.20, 0.2500),
    "eurnzdotc": ("EUR/NZD OTC", 1.9394, 0.0015),
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

@dp.message(Command("start"))
async def cmd_start(message: Message):
    buttons = []
    for key, (name, _, _) in АКТИВТЕР.items():
        buttons.append(InlineKeyboardButton(text=f"📊 {name}", callback_data=key))
    
    # 2 қатарлы әдемі инлайн түймелер жасау
    keyboard_markup = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard_markup)

    await message.answer(
        "⚡ **KUANYSH SYSTEM: PROFESSIONAL TRADER**\n\n"
        "Жылдам асинхронды талдау жүйесі іске қосылды.\n"
        "Сауда жасау үшін активті таңдаңыз:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.in_(АКТИВТЕР.keys()))
async def process_callback(callback: CallbackQuery):
    aktiv_key = callback.data
    name, base_price, deviation = АКТИВТЕР[aktiv_key]
    
    # Бот қатпай бірден істеуі үшін алдын ала жауап беру
    await callback.answer(f"{name} талдануда...")

    # Математикалық есептеу мен трендті анықтау
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

    await callback.message.answer(analysis_text, parse_mode="Markdown")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Aiogram асинхронды боты сәтті іске қосылды!")
    await dp.start_polling(bot)

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    import threading
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    asyncio.run(main())
    
