import os
import discord
from discord.ext import commands
from google import genai
from google.genai import types
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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
modActions: Moderation = Moderation(bot)

config = types.GenerateContentConfig(tools=[modActions.timeout, modActions.kick, modActions.ban])

@bot.event
async def on_ready():
    # try:
    #     mongo_client.admin.command('ping')
    #     print("Successfully connected to MongoDB!")
    # except Exception as e:
    #     print(e)
    await bot.add_cog(modActions)
    print("online")

@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
        print(ctx)
        print(f"{ctx.author} said: {ctx.content}")
        await bot.process_commands(ctx)

@bot.command()
async def judge(ctx, *, string: str = ""):
    prompt = open("prompt.txt", 'r').read() + "\nCONTEXT DONE!"
    punishment = genai_client.models.generate_content(model="gemini-2.0-flash-lite", contents=prompt+"User, "+str(ctx.author)+" says:"+string+"Respond only with 'kick', 'ban', or 'timeout', followed by a colon ':' and a brief reason for the punishment in under 100 characters.")
    reason = punishment.text.split(':')
    await punish(ctx, reason[0], ctx.author, reason[1])


async def punish(ctx, message: str, user: discord.User, reason: str):
    ctx.author = "Orwell"
    if message.lower() == 'kick':
        await modActions.kick(ctx, user, reason=reason)
    elif message.lower() == 'ban':
        await modActions.ban(ctx, user, reason=reason)
    elif message.lower() == 'timeout':
        prompt = open("prompt.txt", 'r').read() + "\nCONTEXT DONE!"
        time = genai_client.models.generate_content(model="gemini-2.0-flash-lite", contents = prompt+"User, "+str(ctx.author)+" says:"+str(ctx.message)+"Respond only with a time formatted as 'Days:Hours:Minutes' (for example '0:2:30') based on how long you think the user should be timed out for this offense.")
        times = time.text.split(':')
        print(times)
        try:
            await modActions.timeout(ctx, user, int(times[0]), int(times[1]), int(times[2]), reason=reason)
        except Exception as e:
            print("Error timing user out: " + e)

ruleset.setup(bot)
bot.run(DISCORD_API_KEY)
