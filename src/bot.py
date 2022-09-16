import logging
import os
import coloredlogs
import motor.motor_asyncio
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from pathlib import Path
from pymongo import MongoClient

log = logging.getLogger("Log Bot")
coloredlogs.install(logger=log)


class LogBot(commands.Bot):
    def __init__(self):
        load_dotenv()
        intents = disnake.Intents.default()

        super().__init__(reload=True, intents=intents)

        logging.basicConfig(
            level=logging.INFO,
            format="(%(asctime)s) %(levelname)s %(message)s",
            datefmt="%m/%d/%y - %H:%M:%S %Z"
        )
        self.loop.create_task(self.prepare_bot())

    def load_cogs(self):
        for file in os.listdir(str(Path(__file__).parents[0]) + "/cogs"):
            if file.endswith(".py") and not file.startswith("_"):
                self.load_extension(f"cogs.{file[:-3]}")

        log.info("All cogs have been loaded. ")

    def run(self):
        if not os.getenv("BOT_TOKEN") or os.getenv("BOT_TOKEN") == "":
            return log.error("No .env file setup with proper token paramter.")
        self.load_cogs()
        super().run(os.getenv("BOT_TOKEN"))


bot = LogBot()
bot.run()
