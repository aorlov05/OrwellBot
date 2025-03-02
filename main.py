import os
import discord
from discord.ext import commands
from google import genai
import ruleset
from dotenv import load_dotenv
from moderation import Moderation
load_dotenv()

DISCORD_API_KEY = os.environ.get('DISCORD_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)
client = genai.Client(api_key=GEMINI_API_KEY)

@bot.event
async def on_ready():
    await bot.add_cog(Moderation(bot))
    print("online")

@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
        print(ctx)
        print(f"{ctx.author} said: {ctx.content}")
        await bot.process_commands(ctx)

ruleset.setup(bot)
bot.run(DISCORD_API_KEY)
