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

(
    LANGUAGE, NAME, SURNAME, AGE, POSITION, LOCATION, PHONE,
    PREV_JOB, PREV_SALARY, EXPECTED_SALARY, HARDWORK, MATH,
    MOTIVATION, START_DATE
) = range(14)

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
        await update.message.reply_text("👋 Assalomu alaykum!\nIsmingizni kiriting:")
    else:
        context.user_data["lang"] = "kr"
        await update.message.reply_text("👋 Ассалому алайкум!\nИсмингизни киритинг:")
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    lang = context.user_data["lang"]
    text = "Familyangizni kiriting:" if lang == "uz" else "Фамилиянгизни киритинг:"
    await update.message.reply_text(text)
    return SURNAME


async def get_surname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["surname"] = update.message.text
    lang = context.user_data["lang"]
    text = "Yoshingiz nechida?" if lang == "uz" else "Ёшингиз нечада?"
    await update.message.reply_text(text)
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    lang = context.user_data["lang"]
    keyboard = [[KeyboardButton("Usta"), KeyboardButton("O‘rganuvchi")]] if lang == "uz" else [[KeyboardButton("Уста"), KeyboardButton("Ўрганувчи")]]
    text = "Lavozimingizni tanlang:" if lang == "uz" else "Лавозимингизни танланг:"
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
    return POSITION


async def get_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["position"] = update.message.text
    lang = context.user_data["lang"]
    text = "Manzilingizni yozing (Viloyat, shahar yoki tuman):" if lang == "uz" else "Манзилингизни ёзинг (Вилоят, шаҳар ёки туман):"
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
    text = "Oldin qayerda ishlagansiz? (Bo‘lmasa 'yo‘q' deb yozing)" if lang == "uz" else "Олдин қаерда ишлагансиз? (Бўлмаса 'йўқ' деб ёзинг)"
    await update.message.reply_text(text)
    return PREV_JOB


async def get_prev_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["prev_job"] = update.message.text
    lang = context.user_data["lang"]
    text = "Oldingi ish joyingizdagi oyligingiz qancha edi?" if lang == "uz" else "Олдинги иш жойингиздаги ойлигингиз қанча эди?"
    await update.message.reply_text(text)
    return PREV_SALARY


async def get_prev_salary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["prev_salary"] = update.message.text
    lang = context.user_data["lang"]
    text = "Hozir o‘ylayotgan oyligingiz qancha?" if lang == "uz" else "Ҳозир ўйлаётган ойлигингиз қанча?"
    await update.message.reply_text(text)
    return EXPECTED_SALARY


async def get_expected_salary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["expected_salary"] = update.message.text
    lang = context.user_data["lang"]
    text = "Og‘ir ishlarga tayyormisiz? (Ha/Yo‘q)" if lang == "uz" else "Оғир ишларга тайёрмисиз? (Ҳа/Йўқ)"
    await update.message.reply_text(text)
    return HARDWORK


async def get_hardwork(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["hardwork"] = update.message.text
    lang = context.user_data["lang"]
    text = "Matematikani (qo‘shish, ayrish, ko‘paytirish, bo‘lish) bilasizmi?" if lang == "uz" else "Математикани (қўшиш, айриш, кўпайтириш, бўлиш) биласизми?"
    await update.message.reply_text(text)
    return MATH


async def get_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["math"] = update.message.text
    lang = context.user_data["lang"]
    text = "Nima uchun hunar o‘rganmoqchisiz?" if lang == "uz" else "Нима учун ҳунар ўрганмоқчисиз?"
    await update.message.reply_text(text)
    return MOTIVATION


async def get_motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["motivation"] = update.message.text
    lang = context.user_data["lang"]
    text = "Qachondan ish boshlay olasiz?" if lang == "uz" else "Қачондан иш бошлай оласиз?"
    await update.message.reply_text(text)
    return START_DATE


async def get_start_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["start_date"] = update.message.text
    data = context.user_data

    # Ma'lumotlarni Google Sheets'ga yuborish
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
            SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_surname)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_position)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            PREV_JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_prev_job)],
            PREV_SALARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_prev_salary)],
            EXPECTED_SALARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_expected_salary)],
            HARDWORK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_hardwork)],
            MATH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_math)],
            MOTIVATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_motivation)],
            START_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_start_date)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
