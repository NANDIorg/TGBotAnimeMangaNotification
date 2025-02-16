from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()
tg_token = os.getenv("TG_TOKEN")

def start(update: Update, context: CallbackContext) -> None:
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    chat_id = update.effective_chat.id

    cursor.execute(f"SELECT * FROM users WHERE chat_id = \"{chat_id}\"")
    row = cursor.fetchall()
    if len(row) > 0:
        update.message.reply_text(f"Вы уже зарегистрированы, используйте /help для команд")
    else:
        cursor.execute(f"INSERT INTO users (chat_id) VALUES (\"{chat_id}\")")
        conn.commit()
        update.message.reply_text(f"Вы успешно зарегистрированы для получения уведомлений, вам осталось только настроить их")

    conn.close()


def main():
    updater = Updater(tg_token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()