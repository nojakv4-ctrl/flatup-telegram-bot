import os
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

MENU=[["💰 Розцінки","📸 Приклади робіт"],["📅 Вільні дати","📞 Контакти"],["📝 Залишити заявку"]]

async def start(update:Update,ctx:ContextTypes.DEFAULT_TYPE):
    print("START натиснули")
    await update.message.reply_text("Вітаємо у FlatUp Львів!",reply_markup=ReplyKeyboardMarkup(MENU,resize_keyboard=True))

async def msg(update:Update,ctx:ContextTypes.DEFAULT_TYPE):
    t=update.message.text
    r={
"💰 Розцінки":"Розцінки додаси пізніше.",
"📸 Приклади робіт":"Додай посилання на фото.",
"📅 Вільні дати":"Напиши актуальні дати.",
"📞 Контакти":"Телефон: ...",
"📝 Залишити заявку":"Напишіть ім'я, телефон і короткий опис."
}.get(t,"Оберіть пункт меню.")
    await update.message.reply_text(r)

app=Application.builder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,msg))
app.run_polling()
