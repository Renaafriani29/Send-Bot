# (c) Koshik
import os
import asyncio
from config import Config
from Script import script
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from db.sqlalchaemyDB import add_user, query_msg, full_userbase

#=====================================================================================##

#buttons
BUTTONS1 = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Made By', url='https://t.me/RoBot_V2'),
        InlineKeyboardButton('Channel', url='https://t.me/RKrishnaa')
        ]]
    )

#=====================================================================================##

A = """**Message from** {} **with id** {}.\n\n **Message:** {}"""
NEW = """#NEWUSER \n\n Name:- {} \n ID:- {} \n started your bot."""

#=====================================================================================##

@Client.on_message(filters.command(["start"]))
async def start(bot, update):
    await update.reply_chat_action("typing")
    k = await update.reply_text("**Processing...⏳**", quote=True)
    id = update.from_user.id
    user_name = '@' + update.from_user.username if update.from_user.username else None
    try:
        await add_user(id, user_name)
        await bot.send_message(Config.LOGC, text=NEW.format(update.from_user.mention, update.from_user.id)
    except:
        pass
    await k.edit_text(script.START, reply_markup=BUTTONS1)
