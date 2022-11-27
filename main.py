import sqlite3

import logging
from telegram import Update

from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters, Updater, CallbackContext, Filters,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def start(update: Update, context: CallbackContext) -> int:
    conn = sqlite3.connect('UsersDb.db')

    cur = conn.cursor()
    cur.execute("SELECT NAME FROM USERS WHERE ID= ? ", (update.message.from_user.id,))

    one_result = cur.fetchone()

    if one_result is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, как тебя зовут?")
        return 0

    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, " + str(one_result[0]))


def get_name(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    msg = update.message.text

    conn = sqlite3.connect('UsersDb.db')

    cur2 = conn.cursor()

    name = msg

    user = (update.message.from_user.id, name)
    cur2.execute('INSERT INTO USERS VALUES(?,?)', user)
    conn.commit()

    update.message.reply_text(
        "Привет," + msg,
    )
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    update.message.reply_text(
        "Bye! I hope we can talk again some day."
    )

    return ConversationHandler.END


if __name__ == '__main__':
    print('STARTED FUCKEN WORK')
    updater = Updater(token='5764317978:AAHGYsPsCziPutNohfL2DZNclSDgQlA-8gU', use_context=True)

    dispatcher = updater.dispatcher

    convHandler = ConversationHandler(entry_points=[MessageHandler(Filters.text & ~Filters.command, start)],
                                      states={
                                          0: [MessageHandler(Filters.text & ~Filters.command, get_name)]
                                      },
                                      fallbacks=[CommandHandler('cancel', cancel)])

    dispatcher.add_handler(convHandler)

    updater.start_polling()

    updater.idle()
