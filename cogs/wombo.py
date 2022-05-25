import os
import pathlib
from enum import Enum

import discord
import requests
from discord import app_commands
from discord.ext import commands

from utils.generator import gen_image


class Styles(Enum):
    synthwave = 1
    ukiyoe = 2
    no_style = 3
    steampunk = 4
    fantasy_art = 5
    vibrant = 6
    hd = 7
    pastel = 8
    psychic = 9
    dark_fantasy = 10
    mystical = 11
    festive = 12
    baroque = 13
    etching = 14
    sdali = 15
    wuhtercuhler = 16
    provenance = 17
    rose_gold = 18
    moonwalker = 19
    blacklight = 20
    psychedelic = 21
    ghibil = 22
    surreal = 23
    love = 24
    death = 25
    robots = 26


class Wombo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description='generate AI art from https://app.wombo.art')
    @app_commands.describe(prompt="insert word or phrase that art will be based on", style='What style do you want to '
                                                                                           'generate a Wombo Dream '
                                                                                           'from?')
    # @app_commands.guilds(discord.Object(id=<guild id>)) If you want to define specific guilds (Currently,
    # this is global)
    @app_commands.guilds()
    async def art(self, ctx: discord.Interaction, prompt: str, style: Styles):
        """generate AI art from https://app.wombo.art"""
        await ctx.response.defer()  # wait for followup message
        c = await gen_image(prompt, style)

        img_file = f"{prompt}_{style.name}.png"

        with open(img_file, "wb") as file:
            file.write(requests.get(c).content)
            file.close()

        # check if file exists
        path = pathlib.Path(img_file)
        if path.exists():
            await ctx.followup.send(file=discord.File(img_file))
            for img_file in os.listdir("./"):
                if img_file.endswith(".png"):
                    os.remove(img_file)


async def setup(bot):  # set async function
    await bot.add_cog(Wombo(bot))  # Use await
