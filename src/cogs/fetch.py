import logging
import os
from typing import Literal
import coloredlogs
import disnake
from disnake.ext import commands
import pymongo
try:
    test_guilds = [int(os.getenv("TEST_GUILD"))]
finally:
    test_guilds = []

log = logging.getLogger("Log cog")
coloredlogs.install(logger=log)

class LogFind(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")  

    @commands.slash_command(name="fetch", guild_ids=test_guilds, description="Fetches modmail log from the database")
    @commands.guild_only()
    async def fetch(self, inter: disnake.ApplicationCommandInteraction, logkey: str) -> None:
        await inter.response.defer()
        myclient = pymongo.MongoClient(os.getenv("MONGO"))
        mydb = myclient["modmail_bot"]
        mycol = mydb["logs"]
        data = mycol.find_one({"key": logkey})
        if data is None:
            await inter.followup.send("Log not found") 
            return
        avatar = data['recipient']['avatar_url']
        messages = data['messages']
        embed = disnake.Embed(title=f"{data['recipient']['name']}({data['recipient']['id']})", color=disnake.Color.blurple())
        embed2 = disnake.Embed(color=disnake.Color.blurple())    
        embed.set_author(name="Modmail Log", icon_url=avatar)
        for x in messages:
            embed.add_field(name=f"`{x['author']['name']}({x['author']['id']})`", value=f"{x['content']}", inline=False)
            
        await inter.followup(embeds=[embed])
 
        for y in messages[31:]:
            embed2.add_field(name=f"`{y['author']['name']}({y['author']['id']})`", value=f"{y['content']}", inline=False)
            
        await inter.send(embed=embed2)            

def setup(bot: commands.Bot):
    bot.add_cog(LogFind(bot))
