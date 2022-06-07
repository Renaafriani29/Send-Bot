# (c) Koshik
import os
import math
import json
import time
import shutil
import heroku3
import requests
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
BT_STRT_TM = time.time()
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", "")

#=====================================================================================##


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {Dic_powerN[n]}B"

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


@Client.on_message((filters.private | filters.group) & filters.command('status'))
async def bot_dyno_status(client,message):
    px = await message.reply_text("**Fetching Bot Status...✨**", quote=True)
    if HEROKU_API_KEY:
        try:
            server = heroku3.from_key(HEROKU_API_KEY)

            user_agent = (
                'Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/80.0.3987.149 Mobile Safari/537.36'
            )
            accountid = server.account().id
            headers = {
            'User-Agent': user_agent,
            'Authorization': f'Bearer {HEROKU_API_KEY}',
            'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
            }

            path = f"/accounts/{accountid}/actions/get-quota"

            request = requests.get(f"https://api.heroku.com{path}", headers=headers)

            if request.status_code == 200:
                result = request.json()

                total_quota = result['account_quota']
                quota_used = result['quota_used']

                quota_left = total_quota - quota_used

                total = math.floor(total_quota/3600)
                used = math.floor(quota_used/3600)
                hours = math.floor(quota_left/3600)
                minutes = math.floor(quota_left/60 % 60)
                days = math.floor(hours/24)

                usedperc = math.floor(quota_used / total_quota * 100)
                leftperc = math.floor(quota_left / total_quota * 100)

                quota_details = f"""
**Heroku Account Status**
> __You have **{total} hours** of free dyno quota available each month.😉__
> __Dyno hours used this month__ ;
        - **{used} hours🙃**  ( {usedperc}% )
> __Dyno hours remaining this month__ ;
        - **{hours} hours😁**  ( {leftperc}% )
        - **Approximately {days} days!🥳🥳**
"""
            else:
                quota_details = ""
        except:
            print("`Check your Heroku API key...`")
            quota_details = ""
    else:
        quota_details = ""

    uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - BT_STRT_TM))

    await px.edit_text(
        "**🙇🏻‍♂️ Current status of This Bot! 🙇🏻‍♂️**\n\n"
        f"> __BOT Uptime__ : **{uptime}**\nBot was restarted **{uptime}** ago..\n\n"
        f"{quota_details}"
    )
