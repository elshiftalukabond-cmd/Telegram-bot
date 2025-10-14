import os
import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHEET_URL = os.getenv("SHEET_URL")

LANGUAGE, NAME, AGE, LOCATION, PHONE, EXPERIENCE, MOTIVATION = range(7)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🇺🇿 O‘zbek (Lotin)"), KeyboardButton("🇺🇿 Ўзбек (Кирил)")],
    ]
    await update.message.reply_text(
        "Tilni tanlang / Выберите язык:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return LANGUAGE

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.message.text
    if "Lotin" in lang:
        context.user_data["lang"] = "uz"
        await update.message.reply_text("Assalomu alaykum! 👷‍♂️\nIsmingizni kiriting:")
    else:
        context.user_data["lang"] = "kr"
        await update.message.reply_text("Ассалому алайкум! 👷‍♂️\nИсмингизни киритинг:")
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    lang = context.user_data["lang"]
    text = "Yoshingiz nechida?" if lang == "uz" else "Ёшингиз нечада?"
    await update.message.reply_text(text)
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    lang = context.user_data["lang"]
    text = "Qayerda yashaysiz?" if lang == "uz" else "Қаерда яшайсиз?"
    await update.message.reply_text(text)
    return LOCATION


async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["location"] = update.message.text
    lang = context.user_data["lang"]
    text = "Telefon raqamingizni yozing:" if lang == "uz" else "Телефон рақамингизни ёзинг:"
    await update.message.reply_text(text)
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    lang = context.user_data["lang"]
    text = "Ish tajribangiz bormi? (Ha/Yo‘q)" if lang == "uz" else "Иш тажрибангиз борми? (Ҳа/Йўқ)"
    await update.message.reply_text(text)
    return EXPERIENCE


async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["experience"] = update.message.text
    lang = context.user_data["lang"]
    text = "Nima uchun ustachilikni o‘rganmoqchisiz?" if lang == "uz" else "Нима учун устачиликни ўрганмоқчисиз?"
    await update.message.reply_text(text)
    return MOTIVATION


async def get_motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["motivation"] = update.message.text
    data = context.user_data

    requests.post(SHEET_URL, json=data)
    lang = context.user_data["lang"]
    text = "✅ Rahmat! Arizangiz qabul qilindi." if lang == "uz" else "✅ Рахмат! Аризангиз қабул қилинди."
    await update.message.reply_text(text)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ariza bekor qilindi.")
    return ConversationHandler.END


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_experience)],
            MOTIVATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_motivation)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
