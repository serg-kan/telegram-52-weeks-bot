import logging
import os
import random
import sys

from datetime import time
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
chat_id = os.getenv("CHAT_ID");
proxy_url = os.getenv("PROXY_URL")
proxy_username = os.getenv("PROXY_USERNAME")
proxy_password = os.getenv("PROXY_PASSWORD")

REQUEST_KWARGS = {
        'proxy_url': proxy_url,
        # Optional, if you need authentication:
        'urllib3_proxy_kwargs': {
            'username': proxy_username,
            'password': proxy_password,
        }
    }

if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
        updater.idle()
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def send_notification(context: CallbackContext):
    context.bot.send_message(chat_id=chat_id,
                             text='One message every minute')

if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS, use_context=True)
    j = updater.job_queue

    job_minute = j.run_daily(send_notification, time(20, 0))

    # updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    # updater.dispatcher.add_handler(CommandHandler("random", random_handler))

    run(updater)
