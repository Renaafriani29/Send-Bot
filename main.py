# (c) @Koshik

import os
from pyrogram import Client
from config import Config

class Bot(Client):

    def __init__(self):
        super().__init__(
            session_name="Message-Sender-Bot",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins={"root": "plugins"},
            sleep_threshold=5
        )


app = Bot()
app.run()
