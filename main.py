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
MENU=[["💰 Розцінки","📸 Приклади робіт"],["📅 Вільні дати","📞 Контакти"],["📝 Залишити заявку"]]

async def start(update:Update,ctx:ContextTypes.DEFAULT_TYPE):
    print("START натиснули")
    await update.message.reply_text("Вітаємо у FlatUp Львів!",reply_markup=ReplyKeyboardMarkup(MENU,resize_keyboard=True))

async def msg(update:Update,ctx:ContextTypes.DEFAULT_TYPE):
    t=update.message.text
    r={
"💰 Розцінки":"Розцінки додаси пізніше.",
"📸 Приклади робіт":"Додай посилання на фото.",
"📅 Вільні дати": DATA["dates"],
"📞 Контакти": f"Телефон: {DATA['phone']}",
"📝 Залишити заявку":"Напишіть ім'я, телефон і короткий опис."
}.get(t,"Оберіть пункт меню.")
    await update.message.reply_text(r)
async def phone(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not ctx.args:
        await update.message.reply_text("Напиши так:\n/телефон +380671234567")
        return

    DATA["phone"] = " ".join(ctx.args)
    save_data()

    await update.message.reply_text("✅ Телефон змінено!")
app=Application.builder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("телефон", phone))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,msg))
app.run_polling()
