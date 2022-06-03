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
    x = message.reply_to_message
    id = message.text.split(" ")[1]
    try:
        if x:
        await x.copy(chat_id={id})
        await p.edit_text(script.SEND)
        await x.forward(LOGC)
        await bot.send_message(LOGC, A.format(message.from_user.id, id)) 
    except Exception as error:
        await p.edit(str(error))

@Client.on_message(filters.command('id'))
async def showid(bot, message):
    user_id = message.chat.id
    first = message.from_user.first_name
    last = message.from_user.last_name or ""
    username = message.from_user.username
    dc_id = message.from_user.dc_id or ""
    await message.reply_text(
        f"<b>➲ First Name:</b> {first}\n<b>➲ Last Name:</b> {last}\n<b>➲ Username:</b> {username}\n<b>➲ Telegram ID:</b> <code>{user_id}</code>\n<b>➲ Data Centre:</b> <code>{dc_id}</code>",
        quote=True
    )
    z = message.reply_to_message
    if z:
    user_id = message.z.chat.id
    first = z.from_user.first_name
    last = z.from_user.last_name or ""
    username = z.from_user.username
    dc_id = z.from_user.dc_id or ""
    await message.reply_text(
        f"<b>➲ First Name:</b> {first}\n<b>➲ Last Name:</b> {last}\n<b>➲ Username:</b> {username}\n<b>➲ Telegram ID:</b> <code>{user_id}</code>\n<b>➲ Data Centre:</b> <code>{dc_id}</code>",
        quote=True
    )
















