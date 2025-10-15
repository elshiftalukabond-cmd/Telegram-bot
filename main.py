import os
import re
import requests
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
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

LANG, NAME, SURNAME, AGE, POSITION, REGION, CITY, PHONE, PREV_WORK, PREV_PHONE, WORK_YEARS, PREV_SALARY, DESIRED_SALARY, HEAVY, MATH, REASON, START, COMMENT = range(18)

regions = {
    "Farg‘ona": ["Farg‘ona shahri", "Marg‘ilon", "Qo‘qon", "Toshloq", "Oltiariq", "Qo‘shtepa", "Beshariq", "Rishton", "Yozyovon", "Dang‘ara", "Furqat", "So‘x", "Uchko‘prik", "O‘zbekiston tumani", "Farg‘ona tumani"],
    "Namangan": ["Namangan shahri", "Chortoq", "Chust", "Kosonsoy", "Mingbuloq", "Norin", "Pop", "To‘raqo‘rg‘on", "Uchqo‘rg‘on", "Yangiqo‘rg‘on"],
    "Andijon": ["Andijon shahri", "Asaka", "Baliqchi", "Bo‘z", "Buloqboshi", "Izboskan", "Jalaquduq", "Marhamat", "Oltinko‘l", "Paxtaobod", "Shahrixon", "Ulug‘nor", "Xo‘jaobod", "Andijon tumani"]
}

def is_valid_phone(number: str) -> bool:
    pattern = re.compile(r'^\+998\d{9}$')
    return bool(pattern.match(number))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Assalomu alaykum! ELSHIFT — qurilish, montaj va interyer sohasida faoliyat yurituvchi kompaniya.\n\n"
        "Biz tez o‘rganadigan, mas’uliyatli yoshlarni o‘z jamoamizga taklif qilamiz!\n\n"
        "Quyidagi tillardan birini tanlang 👇"
    )
    keyboard = [
        [KeyboardButton("🇺🇿 O‘zbek (Lotin)"), KeyboardButton("🇺🇿 Ўзбек (Кирил)")],
    ]
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
    return LANG

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.message.text
    if "Lotin" in lang:
        context.user_data["lang"] = "uz"
        await update.message.reply_text("Ismingizni kiriting:")
    else:
        context.user_data["lang"] = "kr"
        await update.message.reply_text("Исмингизни киритинг:")
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
    keyboard = [[KeyboardButton("Usta")], [KeyboardButton("O‘rganuvchi")]]
    await update.message.reply_text("Lavozimni tanlang:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return POSITION

async def get_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["position"] = update.message.text
    keyboard = [[KeyboardButton(v)] for v in regions.keys()]
    await update.message.reply_text("Viloyatingizni tanlang:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return REGION

async def get_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    region = update.message.text
    context.user_data["region"] = region
    cities = regions.get(region, [])
    keyboard = [[KeyboardButton(c)] for c in cities]
    await update.message.reply_text(f"{region}dagi shahar/tumaningizni tanlang:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return CITY

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    contact_button = KeyboardButton("📱 Raqamni ulashish", request_contact=True)
    await update.message.reply_text("Telefon raqamingizni yuboring yoki yozing (+998 bilan):",
                                    reply_markup=ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True, one_time_keyboard=True))
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.contact.phone_number if update.message.contact else update.message.text
    if not is_valid_phone(phone):
        await update.message.reply_text("Telefon raqam noto‘g‘ri. Iltimos, +998 bilan yozing.")
        return PHONE
    context.user_data["phone"] = phone
    await update.message.reply_text("Oldin qayerda ishlagansiz?")
    return PREV_WORK

async def get_prev_work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["previous_work"] = update.message.text
    await update.message.reply_text("Oldingi ish joyingizning telefon raqamini yozing:")
    return PREV_PHONE

async def get_prev_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["previous_phone"] = update.message.text
    await update.message.reply_text("Necha yil davomida ishlagansiz?")
    return WORK_YEARS

async def get_work_years(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["work_years"] = update.message.text
    await update.message.reply_text("Oldingi ish joyingizda oyligingiz qancha edi?")
    return PREV_SALARY

async def get_prev_salary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["previous_salary"] = update.message.text
    keyboard = [
        [KeyboardButton("1 000 000 so‘m"), KeyboardButton("2 000 000 so‘m")],
        [KeyboardButton("3 000 000 so‘m"), KeyboardButton("4 000 000 so‘m")],
        [KeyboardButton("5 000 000 so‘m dan ko‘p")]
    ]
    await update.message.reply_text("Qancha oylik xohlaysiz?", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return DESIRED_SALARY

async def get_desired_salary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["desired_salary"] = update.message.text
    keyboard = [[KeyboardButton("Ha")], [KeyboardButton("Yo‘q")]]
    await update.message.reply_text("Og‘ir ishlarga tayyormisiz?", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return HEAVY

async def get_heavy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["heavy_ready"] = update.message.text
    keyboard = [[KeyboardButton("Ha")], [KeyboardButton("Yo‘q")]]
    await update.message.reply_text("Matematikani (qo‘shish, ayrish, ko‘paytirish, bo‘lish) bilasizmi?", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return MATH

async def get_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["math"] = update.message.text
    await update.message.reply_text("Nima uchun hunar o‘rganmoqchisiz?")
    return REASON

async def get_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["reason"] = update.message.text
    await update.message.reply_text("Qachondan ish boshlay olasiz?")
    return START

async def get_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["start_date"] = update.message.text
    await update.message.reply_text("Qo‘shimcha izoh yoki fikrlaringizni yozing (ixtiyoriy):")
    return COMMENT

async def get_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["comment"] = update.message.text
    data = context.user_data
    requests.post(SHEET_URL, json=data)
    await update.message.reply_text("✅ Rahmat! Arizangiz qabul qilindi.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_surname)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_position)],
            REGION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_region)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
            PHONE: [
                MessageHandler(filters.CONTACT, get_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)
            ],
            PREV_WORK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_prev_work)],
            PREV_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_prev_phone)],
            WORK_YEARS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_work_years)],
            PREV_SALARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_prev_salary)],
            DESIRED_SALARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_desired_salary)],
            HEAVY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_heavy)],
            MATH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_math)],
            REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reason)],
            START: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_start)],
            COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_comment)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
