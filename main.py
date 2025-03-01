import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)

@bot.event
async def on_ready():
    print("online")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("pong")

bot.run("X")
