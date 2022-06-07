# (c) Koshik
import os
import asyncio
from config import Config
from Script import script
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from db.sqlalchemyDB import add_user, query_msg, full_userbase


@Client.on_message(filters.command(["help"]))
async def helpmsg(bot, message):
    await message.reply_chat_action("typing")
    d = await message.reply_text("**Processing...⏳**", quote=True)
    await d.edit_text(script.HELP)


@Client.on_message(filters.command(['users']))
async def get_users(bot, message):
    msg = await message.reply_text("**Processing...⏳**", quote=True)
    users = await full_userbase()
    await msg.edit_text(f"**{len(users)} users** are using this bot.\n\n~ @RKrishnaa ~")


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
