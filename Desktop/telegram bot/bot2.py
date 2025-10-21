import os
import sys
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Укажи свой токен, который выдал BotFather
BOT_TOKEN = "8239451221:AAE7TSB7rmvFPnaGDvpSHJnj6j8v4x3COK8"
# --- Пример данных: товары по категориям ---
ITEMS = {
    "до 1000": [
        "https://www.wildberries.ru/catalog/225408186/detail.aspx?size=357123357",

        "https://www.wildberries.ru/catalog/328964537/detail.aspx?size=493201983",

        "https://www.wildberries.ru/catalog/217906824/detail.aspx?size=347022681",

        "https://www.wildberries.ru/catalog/283817108/detail.aspx?size=434973489",

        "https://www.wildberries.ru/catalog/62001024/detail.aspx?size=109737005",
    ],

    "до 2000": [
        "https://www.wildberries.ru/catalog/265554868/detail.aspx",

        "https://www.wildberries.ru/catalog/281420466/detail.aspx?size=431839314",

        "https://www.wildberries.ru/catalog/336237564/detail.aspx?size=502000811",
    ],

    "до 4500": [
        "https://www.wildberries.ru/catalog/120302114/detail.aspx?size=212982677",
    ],

    "узнать размер одежды": [
        "Топ: 40–42",

        "Кофта: 42",
    ]
}


# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет! Это мой wishlist 👋\n\n"
        "Я бот, чтобы ты долго не парился с выбором подарка 🎁\n"
        "Здесь ты можешь выбрать цену, на которую рассчитываешь, "
        "а я пришлю тебе ссылки на товары с Wildberries 💜"
    )

    # создаём клавиатуру
    keyboard = [["до 1000"], ["до 2000"], ["до 4500"], ["узнать размер одежды"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text(text, reply_markup=reply_markup)


# --- Обработка нажатий кнопок ---
async def handle_price_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text.strip().lower()

    if choice in ITEMS:
        links = ITEMS[choice]

        # Если выбраны размеры — отправляем красиво оформленный текст
        if choice == "узнать размер одежды":
            message = "Твои примерные размеры:\n\n"
            for item in links:
                message += f"• {item}\n\n"
        else:
            message = f"Вот товары {choice} ₽:\n\n"
            for i, link in enumerate(links, start=1):
                message += f"{i}. {link}\n\n"  # <-- добавлен лишний абзац
        await update.message.reply_text(message, disable_web_page_preview=True)
    else:
        await update.message.reply_text("Выбери вариант с клавиатуры 🙂")


# --- Основной запуск ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_price_selection))

    print("✅ Бот запущен! Напиши /start в Telegram.")
    app.run_polling()
if __name__ == "__main__":
    main()