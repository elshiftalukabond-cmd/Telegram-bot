import os
import requests
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ConversationHandler, ContextTypes
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHEET_URL = os.getenv("SHEET_URL")

(
    LANGUAGE,
    NAME, SURNAME, AGE,
    POSITION, LOCATION, PHONE,
    PREV_JOB, PREV_SALARY, EXPECTED_SALARY,
    HARDWORK, MATH, MOTIVATION,
    START_DATE
) = range(14)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("O‘zbek (Lotin)"), KeyboardButton("Ўзбек (Кирил)")]
    ]
    # Dastlabki xabar — Elshift haqida ma’lumot
    text = (
        "Elshift – binolaringiz uchun zamonaviy yechim! Uy, ofis va binolar uchun Alucabond xizmati.\n"
        "12 yillik tajriba, 20 dan ortiq mutaxassislar.\n\n"
        "Tilni tanlang / Тилни танланг:"
    )
    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return LANGUAGE


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sel = update.message.text.strip()
    if sel == "O‘zbek (Lotin)":
        context.user_data["lang"] = "uz"
        await update.message.reply_text(
            "👋 Assalomu alaykum! Siz **ELSHIFT** jamoasiga murojaat qilyapsiz.\n"
            "Ismingizni kiriting:", reply_markup=ReplyKeyboardRemove()
        )
    else:
        context.user_data["lang"] = "kr"
        await update.message.reply_text(
            "👋 Ассалому алайкум! Сиз **ELSHIFT** жамоасига мурожаат қиляпсиз.\n"
            "Исмингизни киритинг:", reply_markup=ReplyKeyboardRemove()
        )
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text.strip()
    lang = context.user_data["lang"]
    text = "Familyangizni kiriting:" if lang == "uz" else "Фамилиянгизни киритинг:"
    await update.message.reply_text(text)
    return SURNAME


async def get_surname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["surname"] = update.message.text.strip()
    lang = context.user_data["lang"]
    text = "Yoshingiz nechida?" if lang == "uz" else "Ёшингиз нечада?"
    await update.message.reply_text(text)
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text.strip()
    lang = context.user_data["lang"]
    if lang == "uz":
        keyboard = [[KeyboardButton("Usta"), KeyboardButton("O‘rganuvchi")]]
        text = "Lavozimingizni tanlang:"
    else:
        keyboard = [[KeyboardButton("Уста"), KeyboardButton("Ўрганувчи")]]
        text = "Лавозимингизни танланг:"
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
    return POSITION


async def get_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["position"] = update.message.text.strip()
    lang = context.user_data["lang"]
    if lang == "uz":
        viloyatlar = ["Farg‘ona", "Andijon", "Namangan"]
        text = "Qaysi viloyatda yashaysiz?"
    else:
        viloyatlar = ["Фарғона", "Андижон", "Наманган"]
        text = "Қайси вилоятда яшайсиз?"
    keyboard = [[v] for v in viloyatlar]
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
    return LOCATION


async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["viloyat"] = update.message.text.strip()
    lang = context.user_data["lang"]
    # misol tumanlar
    if lang == "uz":
        tumanlar = {
            "farg‘ona": ["Farg‘ona shahar", "Marg‘ilon", "Qo‘qon", "Oltiariq", "Rishton"],
            "andijon": ["Andijon shahar", "Asaka", "Shahrixon", "Xo‘jaobod"],
            "namangan": ["Namangan shahar", "Chortoq", "Chust", "Uchqo‘rg‘on"]
        }
        text = "Shahar yoki tumanningizni tanlang:"
    else:
        tumanlar = {
            "фарғона": ["Фарғона шаҳар", "Марғилон", "Қўқон", "Олтиариқ", "Риштон"],
            "андижон": ["Андижон шаҳар", "Асака", "Шаҳрихон", "Хўжаобод"],
            "наманган": ["Наманган шаҳар", "Чортоқ", "Чуст", "Учқўрғон"]
        }
        text = "Шаҳар ёки туманингизни танланг:"
    key = context.user_data["viloyat"].lower()
    keyboard = [[t] for t in tumanlar.get(key, [])]
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["tuman"] = update.message.text.strip()
    lang = context.user_data["lang"]
    text = "Telefon raqamingizni yuboring yoki yozing:" if lang == "uz" else "Телефон рақамингизни юборинг ёки ёзинг:"
    kb = [[KeyboardButton("📱 Raqamni yuborish", request_contact=True)]]
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True))
    return PREV_JOB


async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.contact.phone_number
    lang = context.user_data["lang"]
    text = "Oldin qayerda ishlagansiz? (Bo‘lmasa 'yo‘q' deb yozing)" if lang == "uz" else "Олдин қаерда ишлагансиз? (Бўлмаса 'йўқ' деб ёзинг)"
    await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    return PREV_JOB


async def get_prev_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["prev_job"] = update.message.text.strip()
    lang = context.user_data["lang"]
    text = "Oldingi ish joyingizdagi oyligingiz qancha edi?" if lang == "uz" else "Олдинги иш жойингиздаги ойлигингиз қанча эди?"
    await update.message.reply_text(text)
    return PREV_SALARY


async def get_prev_salary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["prev_salary"] = update.message.text.strip()
    lang = context.user_data["lang"]
    # oylik tanlov tugmalari
    oylik_opts = [
        ["1,000,000 so‘m", "1,500,000 so‘m"],
        ["2,000,000 so‘m", "2,500,000 so‘m"],
        ["3,000,000 so‘m", "3,500,000 so‘m"]
    ]
    text = "Hozir o‘ylayotgan oyligingiz qancha?" if lang == "uz" else "Ҳозир ўйлаётган ойлигингиз қанча?"
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(oylik_opts, one_time_keyboard=True, resize_keyboard=True))
    return EXPECTED_SALARY


async def get_expected_salary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["expected_salary"] = update.message.text.strip()
    lang = context.user_data["lang"]
    if lang == "uz":
        kb = [[KeyboardButton("Ha"), KeyboardButton("Yo‘q")]]
        text = "Og‘ir ishlarga tayyormisiz?"
    else:
        kb = [[KeyboardButton("Ҳа"), KeyboardButton("Йўқ")]]
        text = "Оғир ишларга тайёрмисиз?"
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True))
    return HARDWORK


async def get_hardwork(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["hardwork"] = update.message.text.strip()
    lang = context.user_data["lang"]
    if lang == "uz":
        kb = [[KeyboardButton("Ha"), KeyboardButton("Yo‘q")]]
        text = "Matematikani bilasizmi? (qo‘shish, ayrish, ko‘paytirish, bo‘lish)"
    else:
        kb = [[KeyboardButton("Ҳа"), KeyboardButton("Йўқ")]]
        text = "Математикани биласизми? (қўшиш, айриш, кўпайтириш, бўлиш)"
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True))
    return MOTIVATION


async def get_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["math"] = update.message.text.strip()
    lang = context.user_data["lang"]
    text = "Nima uchun hunar o‘rganmoqchisiz?" if lang == "uz" else "Нима учун ҳунар ўрганмоқчисиз?"
    await update.message.reply_text(text)
    return START_DATE


async def get_motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["motivation"] = update.message.text.strip()
    lang = context.user_data["lang"]
    text = "Qachondan ish boshlay olasiz?" if lang == "uz" else "Қачондан иш бошлай оласиз?"
    await update.message.reply_text(text)
    return START_DATE


async def get_start_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["start_date"] = update.message.text.strip()
    data = context.user_data
    requests.post(SHEET_URL, json=data)
    lang = context.user_data["lang"]
    text = "✅ Rahmat! Arizangiz qabul qilindi." if lang == "uz" else "✅ Рахмат! Аризангиз қабул қилинди."
    await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ariza bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_surname)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_position)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            PHONE: [
                MessageHandler(filters.CONTACT, get_contact),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)
            ],
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

    app.add_handler(conv)
    app.run_polling()


if __name__ == "__main__":
    main()
