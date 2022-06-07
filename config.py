# (c) @Koshik
import os


class Config(object):
# Your Telegram API Hash, get from my.telegram.org
  APP_ID = int(os.environ.get("APP_ID", ""))
# Your Telegram API Hash, get from https://my.telegram.org
  API_HASH = os.environ.get("API_HASH", "")
# Your Telegram Bot Token
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
# Auth Users who can send Send Messages
  AUTH_USERS = {
      str(x)
      for x in os.environ.get("AUTH_USERS", "1162032262").split()
  }
# LOG Channel Where you get Messages from users.
  LOGC = int(os.environ.get('LOG_CHANNEL', -1001711489998))
# Database 
  DB_URI = os.environ.get("DATABASE_URL", "")
