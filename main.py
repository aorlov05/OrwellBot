import discord
from discord.ext import commands
from google import genai

client = genai.Client(api_key="AIzaSyCcRitudApXCvU63ocM5aV-iViBuxmigik")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)

@bot.event
async def on_ready():
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

bot.run("")
