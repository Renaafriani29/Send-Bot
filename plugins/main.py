# (c) Koshik
import os
import asyncio
from config import Config
from Script import script
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from db.sqlalchemyDB import add_user, query_msg, full_userbase
from plugins.bcast import helpmsg

#=====================================================================================##

#buttons
BUTTONS1 = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⭐ Made By ⭐', url='https://t.me/RoBot_V2'),
        InlineKeyboardButton('💥 Channel 💥', url='https://t.me/RKrishnaa')
        ],[
        InlineKeyboardButton('🙂 Help 🙂', url='https://t.me/TheMsgSendBot?start=help'),
        InlineKeyboardButton('🔐 Close 🔐', callback_data='close')
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
    user_name = (
        f'@{update.from_user.username}' if update.from_user.username else None
    )

    try:
        await add_user(id, user_name)
        await bot.send_message(Config.LOGC, text=NEW.format(update.from_user.mention, update.from_user.id))
    except:
        pass
    if update.text == "/start":
        await k.edit_text(script.START, reply_markup=BUTTONS1)
    else:
        cmd = update.text.split(" ", 1)[1]
        if cmd == "help":
            await helpmsg(bot, update)

@Client.on_message(filters.command(["send"]))
async def sendmsg(bot, message):
    await message.reply_chat_action("typing")
    t = await message.reply_text("__Authenticating...__", quote=True)
    if str(message.from_user.id) not in Config.AUTH_USERS:
        await t.edit_text(script.AUTH)
        return
    await t.edit_text("**Authentication Successful...✅**")
    if not message.reply_to_message:
        await t.edit_text("**Reply to some Message.**")
        return
    if len(message.command) != 2:
        await t.edit_text("/send {user id} \n\n Like:- `/send 1162032262`")
        return
    await t.edit_text("**Sending message...⏳**")
    id = message.text.split(" ")[1]
    try:
        await message.reply_to_message.copy(chat_id=int(id))
        await t.edit_text(script.SEND)
    except Exception as error:
        await t.edit(str(error))


@Client.on_message(filters.private & filters.text)
async def privatemsg(bot, message):
    if str(message.from_user.id) in Config.AUTH_USERS:
        return
    if message.text.startswith('/'):
        return
    await message.reply_chat_action("typing")
    msg = str(message.text)
    d = await message.reply_text("**Processing...⏳**", quote=True)
    try:
        await bot.send_message(Config.LOGC, text=A.format(message.from_user.mention, message.from_user.id, msg))
        await d.edit_text("**Your message has been forwarded to Admin(s) successfully.** It will be reviewed and you will get a reply soon.\n\n**~ @RKrishnaa ~**")
    except Exception as error:
        await d.edit_text(str(error))
        await message.reply_text("**Please report this Error to:** @RoBot_V2")

#===========>
@Client.on_callback_query()
async def cb_data(bot, update):
    if update.data == "close":
        await update.message.delete()
#===========>
