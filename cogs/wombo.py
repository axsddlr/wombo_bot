from json import dumps

import discord
import requests
from discord import app_commands
from discord.ext import commands

import utils.reference as ref


async def generate(prompt: str, style: str):
    with requests.Session() as session:
        r = session.post(
            "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw",
            json={"returnSecureToken": True})
        data = r.json()
        token = data["idToken"]
        auth_headers = {"Authorization": "bearer " + token}

        # retrieve task id
        r = session.post("https://app.wombo.art/api/tasks", headers=auth_headers, json=dumps({"premium": False}))
        data = r.json()

        task_id = data["id"]

        # Start the task
        query = {"input_spec": {
            "display_freq": 10,
            "prompt": prompt,
            "style": ref.styles[str(style)]  # refers to python file that maps int to string
        }}
        r = session.put("https://app.wombo.art/api/tasks/" + task_id, json=dumps(query), headers=auth_headers)
        data = r.json()

    while True:
        r = session.get("https://app.wombo.art/api/tasks/" + task_id, headers=auth_headers)
        data = r.json()
        state = data["state"]

        if state == "completed":
            break
        if state == "failed":
            print(data)
            raise RuntimeError(data)

    finishedImage_url = data["photo_url_list"][-1]
    return finishedImage_url


class Wombo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description='generate AI art from https://app.wombo.art')
    # @app_commands.guilds(discord.Object(id=<guild id>)) If you want to define specific guilds (Currently,
    # this is global)
    @app_commands.guilds()
    async def art(self, ctx: discord.Interaction,  prompt: str, style: str):
        """generate AI art from https://app.wombo.art"""
        await ctx.response.defer()  # wait for followup message
        c = await generate(prompt, style)
        await ctx.followup.send(c)


async def setup(bot):  # set async function
    await bot.add_cog(Wombo(bot))  # Use await
