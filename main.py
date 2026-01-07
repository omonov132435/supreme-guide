from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

words = [
    ("apple", "olma"),
    ("book", "kitob"),
    ("water", "suv"),
    ("school", "maktab"),
    ("teacher", "o‘qituvchi"),
]

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_chat.id] = {"i": 0, "side": "en"}
    await send_card(update, context)

async def send_card(update, context):
    chat_id = update.effective_chat.id
    state = user_state[chat_id]
    en, uz = words[state["i"]]
    text = en if state["side"] == "en" else uz

    keyboard = [[InlineKeyboardButton("🔄 Bosish", callback_data="flip")]]
    markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=markup)
    else:
        await update.message.reply_text(text, reply_markup=markup)

async def flip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    state = user_state[q.message.chat.id]

    if state["side"] == "en":
        state["side"] = "uz"
    else:
        state["side"] = "en"
        state["i"] = (state["i"] + 1) % len(words)

    await send_card(update, context)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(flip))
app.run_polling()
