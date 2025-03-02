import os
import discord
from discord.ext import commands
from google import genai
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from filter import set_last_message, check_repeat_message

from dotenv import load_dotenv
load_dotenv()
DISCORD_API_KEY = os.environ.get('DISCORD_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
MONGODB_URI = os.environ.get('MONGODB_URI')

import ruleset
from moderation import Moderation

genai_client = genai.Client(api_key=GEMINI_API_KEY)
mongo_client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)

@bot.event
async def on_ready():
    try:
        mongo_client.admin.command('ping')
        # print(check_repeat_message(mongo_client, "123", "Wow!"))
        # set_last_message(mongo_client, "456", "Oh my god")
        print(check_repeat_message(mongo_client, "456", "OH MY GOD"))
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    await bot.add_cog(Moderation(bot))
    print("online")

@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
        print(ctx)
        print(f"{ctx.author} said: {ctx.content}")

        repeated_message = check_repeat_message(mongo_client, ctx.author.id, ctx.content)
        if repeated_message:
            print(str(ctx.author) + " said " + ctx.content + " multiple times!")
        set_last_message(mongo_client, ctx.author.id, ctx.content)

        await bot.process_commands(ctx)

ruleset.setup(bot)
bot.run(DISCORD_API_KEY)
