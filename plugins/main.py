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
    )

A = """👆 This message was sent by {} to {}."""


@Client.on_message(filters.command(["start"]))
async def start(bot, update):
    await update.reply_chat_action("typing")
    k = await update.reply_text("**Processing...⏳**", quote=True)
    await k.edit_text("__Authenticating...__")
    if str(update.from_user.id) not in Config.AUTH_USERS:
        await k.edit_text(script.AUTH)
        return
    await k.edit_text("**Authentication Successful...✅**")
    await k.edit_text(script.START, reply_markup=BUTTONS1)

@Client.on_message(filters.command(["send"]))
async def sendmsg(bot, message):
    await message.reply_chat_action("typing")
    if str(message.from_user.id) not in Config.AUTH_USERS:
        await k.edit_text(script.AUTH)
        return
    if not message.reply_to_message:
        await message.reply_text("**Reply to some Message, Sir.. :D**")
        return
    if len(message.command) != 2:
        await message.reply_text("/send {user id} \n\n Like:- `/send 1162032262`", quote=True)
        return
    p = await message.reply_text("**Processing...⏳**", quote=True)
    id = message.text.split(" ")[1]
    try:
        await bot.message.reply_to_message.copy(chat_id=int(id))
        await p.edit_text(script.SEND)
        await message.reply_to_message.forward(LOGC)
        await bot.send_message(LOGC, A.format(message.from_user.id, id)) 
    except Exception as error:
        await p.edit(str(error))
















