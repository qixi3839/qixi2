import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from game import BlackjackGame

logging.basicConfig(level=logging.INFO)
games = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎉 欢迎来到 21 点游戏！输入 /join 加入游戏。")

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    if chat_id not in games:
        games[chat_id] = BlackjackGame()

    game = games[chat_id]
    response = game.add_player(user_id, user_name)
    await update.message.reply_text(response)

async def hit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if chat_id in games:
        response = games[chat_id].player_hit(user_id)
        await update.message.reply_text(response)

async def stand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if chat_id in games:
        response = games[chat_id].player_stand(user_id)
        await update.message.reply_text(response)

def main():
    import os
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("hit", hit))
    app.add_handler(CommandHandler("stand", stand))

    app.run_polling()

if __name__ == "__main__":
    main()
