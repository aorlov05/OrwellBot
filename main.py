import os
import discord
from discord.ext import commands
from google import genai
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
load_dotenv()
DISCORD_API_KEY = os.environ.get('DISCORD_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
MONGODB_URI = os.environ.get('MONGODB_URI')

from moderation import Moderation

client = genai.Client(api_key=GEMINI_API_KEY)
mongo_client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)

@bot.event
async def on_ready():
    try:
        mongo_client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    await bot.add_cog(Moderation(bot))
    print("online")

@bot.event
async def on_message(message):
    print(message)
    print(f"User said: {message.content}")
    await bot.process_commands(message)

@bot.command(name="ruleset")
async def ruleset(message, getset:str, string:str):
    print(getset)
    if (getset=="update"):
        response = client.models.generate_content(model="gemini-2.0-flash-lite",contents="These rules are for a Discord Server, understand them because you will be moderating:"+string)
        await message.channel.send(response.text[:2000])
    if (getset=="current"):
        response = client.models.generate_content(model="gemini-2.0-flash-lite", contents="In under 2000 characters, What are the rules of this Discord Server?")
        await message.send(response.text[:2000])

bot.run(DISCORD_API_KEY)
