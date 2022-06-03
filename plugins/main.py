# (c) Koshik
import os
from config import Config
from Script import script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

#buttons
BUTTONS1 = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Made By', url='https://t.me/RoBot_V2'),
        InlineKeyboardButton('Channel', url='https://t.me/RKrishnaa')
        ]]
    )

A = """**Message from** {} **with id** {}.\n\n **Message:** {}"""


@Client.on_message(filters.command(["start"]))
async def start(bot, update):
    await update.reply_chat_action("typing")
    k = await update.reply_text("**Processing...⏳**", quote=True)
    await k.edit_text(script.START, reply_markup=BUTTONS1)

@Client.on_message(filters.command(["send"]))
async def sendmsg(bot, message):
    await message.reply_chat_action("typing")
    t = await message.reply_text("__Authenticating...__")
    if str(message.from_user.id) not in Config.AUTH_USERS:
        await k.edit_text(script.AUTH)
        return
    await t.edit_text("**Authentication Successful...✅**")
    if not message.reply_to_message:
        await message.reply_text("**Reply to some Message, Sir.. :D**")
        return
    if len(message.command) != 2:
        await message.reply_text("/send {user id} \n\n Like:- `/send 1162032262`", quote=True)
        return
    await t.edit_text("**Sending message...⏳**", quote=True)
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
    
@Client.on_message(filters.command(["help"]))
async def sendmsg(bot, message):
    await message.reply_chat_action("typing")
    d = await message.reply_text("**Processing...⏳**", quote=True)
    await d.edit_text(script.HELP)


























