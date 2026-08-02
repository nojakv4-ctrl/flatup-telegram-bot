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

app=Application.builder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("phone", phone))
app.add_handler(CommandHandler("dates", dates))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,msg))
app.run_polling()
