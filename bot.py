import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def startup(self):
        await bot.wait_until_ready()
        # await bot.tree.sync(guild=discord.Object(id=<guild id>))  # If you want to define specific guilds,
        # pass a discord object with id (Currently, this is global)
        await bot.tree.sync()
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="/art"))
        print('Sucessfully synced applications commands')
        print(f'Connected as {bot.user}')

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                    print("{0} is online".format(filename[:-3]))
                except Exception as e:
                    print("{0} was not loaded".format(filename))
                    print(f"[ERROR] {e}")

        self.loop.create_task(self.startup())


bot = Bot()

bot.run(TOKEN)
