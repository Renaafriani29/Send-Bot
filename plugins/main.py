# (c) Koshik
import os
import asyncio
from config import Config
from Script import script
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from db.sqlalchemyDB import add_user, query_msg, full_userbase

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
    except:
        pass
    await k.edit_text(script.START, reply_markup=BUTTONS1)

@Client.on_message(filters.command(["send"]))
async def sendmsg(bot, message):
    await message.reply_chat_action("typing")
    t = await message.reply_text("__Authenticating...__", quote=True)
    if str(message.from_user.id) not in Config.AUTH_USERS:
        await t.edit_text(script.AUTH)
        return
    await t.edit_text("**Authentication Successful...✅**")
    if not message.reply_to_message:
        await t.edit_text("**Reply to some Message, Sir.. :D**")
        return
    if len(message.command) != 2:
        await t.edit_text("/send {user id} \n\n Like:- `/send 1162032262`", quote=True)
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


@Client.on_message(filters.command(["help"]))
async def helpmsg(bot, message):
    await message.reply_chat_action("typing")
    d = await message.reply_text("**Processing...⏳**", quote=True)
    await d.edit_text(script.HELP)


@Client.on_message(filters.command(['users']))
async def get_users(bot, message):
    msg = await message.reply_text("**Processing...⏳**", quote=True)
    users = await full_userbase()
    await msg.edit_text("**{len(users)} users** are using this bot.\n\n~ @RKrishnaa ~")


@Client.on_message(filters.private & filters.command(['bcast']))
async def broadcast(bot, message):
    if str(message.from_user.id) not in Config.AUTH_USERS:
        await t.edit_text(script.AUTH)
        return
    if message.reply_to_message:
        query = await query_msg()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("**Broadcasting Message.. This will Take Some Time**", quote=True)
        for row in query:
            chat_id = int(row[0])
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                blocked += 1
            except InputUserDeactivated:
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""**Broadcast Completed**

Total Users: `{total}`
Successful: `{successful}`
Blocked Users: `{blocked}`
Deleted Accounts: `{deleted}`
Unsuccessful: `{unsuccessful}`

~ @RKrishnaa ~"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
