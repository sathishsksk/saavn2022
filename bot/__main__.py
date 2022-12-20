import shutil, psutil
import signal
import os
import asyncio

from signal import signal, SIGINT
from os import path as ospath, remove as osremove, execl as osexecl
from subprocess import run as srun, check_output
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from time import time
from sys import executable

from wserver import start_server_async
from bot.addons.utils import logger
from bot.helpers.media_info import *
import os
from bot.messages.creator import *
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
dest = "bot/telegramMusic/"

from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.message_utils import *

TOKEN = '5595298904:AAExEMcbyKGA3cBdIECmFB-AD55Zx8L0uOM'


    
def restart(update, context):
    restart_message = sendMessage("Restarting, Please wait!", context.bot, update)
    # Save restart message object in order to reply to it after restarting
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    fs_utils.clean_all()
    alive.terminate()
    web.terminate()
    os.execl(executable, executable, "-m", "bot")

    

def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


def log(update, context):
    sendLogFile(context.bot, update)
    
    
def start(update, context):
    fname = update.message.chat.first_name
    update.message.reply_text(
        start_msg(fname), parse_mode="MarkdownV2")


def help(update, context):
    update.message.reply_text(help_msg(), parse_mode="MarkdownV2")


def list(update, context):
    files = os.listdir("/app/bot/telegramMusic")
    string = ""
    for l in files:
        if l.endswith(".mp3"):
            s = "<b>"+l+"</b>"+"\n"
            string = string+s
    if string:
        update.message.reply_html(string)
    else:
        update.message.reply_html("No songs are currently present")


def contact(update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(
        "Contact", url="telegram.me/TgBotsChat")], ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Contact The Maker:', reply_markup=reply_markup)


def error_handler(update, context):
    logger.error(f"Error {traceback.format_exc()}")


def download(update, context: CallbackContext):
    query = update.message.text
    if 'https://www.saavn' in query or 'https://www.jiosaavn' in query:
        if not context.user_data.get('downloading', False):
            if "/song/" in query:
                msg = update.message.reply_text("Getting song info 🔎🔎")
                send_song(update, context, query, msg)

            elif "/album" in query:
                msg = update.message.reply_text("Getting album info 🔎🔎")
                send_album(update, context, query, msg)

            elif "/playlist/" or "/featured/" in query:
                msg = update.message.reply_text("Getting playlist info 🔎🔎")
                send_playlist(update, context, query, msg)
            else:
                wrong_link(update)
        else:
            process_exist(update)
    else:
        wrong_link(update)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    
    if IS_VPS:
        asyncio.get_event_loop().run_until_complete(start_server_async(PORT))
    # Check if the bot is restarting
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        bot.edit_message_text("Restarted successfully!", chat_id, msg_id)
        os.remove(".restartmsg")

    PORT = int(os.environ.get('PORT', '8443'))

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("list", list))

    dp.add_handler(CommandHandler("contact", contact))
    
    dp.add_handler(CommandHandler("Restart", restart))
    
    dp.add_handler(CommandHandler("ping", ping))
    
    dp.add_handler(CommandHandler("log", log))

    dp.add_handler(MessageHandler(Filters.text, download, run_async=True))

    dp.add_error_handler(error_handler)

    updater.start_polling()
    
    logger.info("Bot Started!")
    
    signal.signal(signal.SIGINT)


app.start()
main()

main_loop.run_forever()
