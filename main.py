# (c) @Koshik

import os
from pyrogram import Client
from config import Config

def main():
    plugins = dict(root="plugins")
    app = Client("Message-Sender-Bot",
                 bot_token=Config.BOT_TOKEN,
                 api_id=Config.APP_ID,
                 api_hash=Config.API_HASH,
                 plugins=plugins,
                 workers=100)

    app.run()


if __name__ == "__main__":
    main()
