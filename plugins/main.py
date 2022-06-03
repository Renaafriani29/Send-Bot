# (c) Koshik
import os
from config import Config
from Script import script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

#buttons
BUTTONS1 = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Made By', url='https://t.me/koshik_17'),
        InlineKeyboardButton('Channel', url='https://t.me/RKrishnaa')
        ]]

@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_chat_action("typing")
    k = await update.reply_text("**Processing...⏳**", quote=True)
    await k.edit_text("__Authenticating...__")
    if str(message.from_user.id) not in Config.AUTH_USERS:
        await k.edit_text(script.AUTH)
    return
    await k.edit_text("**Authentication Successful...✅**")
    await k.edit_text(script.START, reply_markup=BUTTONS1)


















