import os
import discord
from discord.ext import commands
from moderation import Moderation
from dotenv import load_dotenv
load_dotenv()
DISCORD_API_KEY = os.environ.get('DISCORD_API_KEY')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)

@bot.event
async def on_ready():
    await bot.add_cog(Moderation(bot))
    print("online")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("pong")

bot.run(DISCORD_API_KEY)
