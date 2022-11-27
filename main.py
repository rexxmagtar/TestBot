import sqlite3



import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('UsersDb.db')

    cur = conn.cursor()
    cur.execute("SELECT NAME FROM USERS WHERE ID= ? ", (update.message.from_user.id,))

    one_result = cur.fetchone()

    if one_result is None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, как тебя зовут?")
        return 0

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, "+str(one_result[0]))


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    msg = update.message.text

    conn = sqlite3.connect('UsersDb.db')

    cur2 = conn.cursor()

    name = msg

    user = (update.message.from_user.id, name)
    cur2.execute('INSERT INTO USERS VALUES(?,?)', user)
    conn.commit()

    await update.message.reply_text(
        "Привет,"+msg,
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    await update.message.reply_text(
        "Bye! I hope we can talk again some day."
    )

    return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token('5764317978:AAHGYsPsCziPutNohfL2DZNclSDgQlA-8gU').build()

    convHandler = ConversationHandler(entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, start)],
                                      states={
                                          0:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)]
                                      },
                                      fallbacks=[CommandHandler('cancel', cancel)])

    application.add_handler(convHandler)

    application.run_polling()
