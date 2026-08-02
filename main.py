import os
import json
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


ADMIN_ID = 486401273


with open("data.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)


def save_data():
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(DATA, f, ensure_ascii=False, indent=2)


MENU = [
    ["💰 Розцінки", "📸 Приклади робіт"],
    ["📅 Вільні дати", "📞 Контакти"],
    ["📝 Залишити заявку"]
]


async def post_init(app):
    await app.bot.set_my_commands([
        ("start", "Запуск бота"),
        ("phone", "Змінити телефон"),
        ("dates", "Змінити вільні дати"),
        ("price", "Змінити розцінки"),
        ("works", "Змінити приклади робіт"),
    ])


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вітаємо у FlatUp Львів!",
        reply_markup=ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    )


async def msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    r = {
        "💰 Розцінки": DATA["price"],
        "📸 Приклади робіт": DATA["works"],
        "📅 Вільні дати": DATA["dates"],
        "📞 Контакти": DATA["phone"],
        "📝 Залишити заявку": "Напишіть ім'я, телефон і що потрібно зробити."
    }

    await update.message.reply_text(
        r.get(t, "Оберіть пункт меню.")
    )


async def phone(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    DATA["phone"] = " ".join(ctx.args)
    save_data()

    await update.message.reply_text("✅ Телефон змінено")


async def dates(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    DATA["dates"] = " ".join(ctx.args)
    save_data()

    await update.message.reply_text("✅ Дати змінено")


async def price(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    DATA["price"] = " ".join(ctx.args)
    save_data()

    await update.message.reply_text("✅ Розцінки змінено")


async def works(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    DATA["works"] = " ".join(ctx.args)
    save_data()

    await update.message.reply_text("✅ Роботи змінено")


app = Application.builder().token(os.environ["BOT_TOKEN"]).post_init(post_init).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("phone", phone))
app.add_handler(CommandHandler("dates", dates))
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("works", works))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))


app.run_polling()
