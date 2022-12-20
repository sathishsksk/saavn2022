from aiohttp import web
from plugins import web_server
import shutil,psutil
from pyrogram.enums import ParseMode
import sys
from datetime import datetime 
import signal
import asyncio
from signal import signal, SIGINT
from requests import get as rget
from bot.addons.utils import logger
from bot.helpers.media_info import *
import os
from bot.messages.creator import *
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from wserver import start_server_async
dest = "telegramMusic/"

import qbittorrentapi as qba
import telegram.ext as tg

TOKEN = '5862929153:AAGLEMTNGuOslFHfwzl1ncsCvhHTvRhcYCs'
SERVER_PORT = os.environ.get('SERVER_PORT', None)
PORT = os.environ.get('PORT', SERVER_PORT)
IS_VPS = os.environ.get('IS_VPS', None)

async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

def start(update, context):
    fname = update.message.chat.first_name
    update.message.reply_text(
        start_msg(fname), parse_mode="MarkdownV2")


def help(update, context):
    update.message.reply_text(help_msg(), parse_mode="MarkdownV2")


def list(update, context):
    files = os.listdir("/app/telegramMusic")
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

    PORT = int(os.environ.get('PORT', '8443'))

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("list", list))

    dp.add_handler(CommandHandler("contact", contact))

    dp.add_handler(MessageHandler(Filters.text, download, run_async=True))

    dp.add_error_handler(error_handler)

    logger.info("Bot Started!💥")
    
    self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/CodeXBotz")
        self.LOGGER(__name__).info(f""" \n\n       
░█████╗░░█████╗░██████╗░███████╗██╗░░██╗██████╗░░█████╗░████████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗╚══██╔══╝╚════██║
██║░░╚═╝██║░░██║██║░░██║█████╗░░░╚███╔╝░██████╦╝██║░░██║░░░██║░░░░░███╔═╝
██║░░██╗██║░░██║██║░░██║██╔══╝░░░██╔██╗░██╔══██╗██║░░██║░░░██║░░░██╔══╝░░
╚█████╔╝╚█████╔╝██████╔╝███████╗██╔╝╚██╗██████╦╝╚█████╔╝░░░██║░░░███████╗
░╚════╝░░╚════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚══════╝
                                          """)

    #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()
    # updater.start_polling()
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
