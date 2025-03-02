import os
import discord
from discord.ext import commands
from google import genai
from google.genai import types
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import server_data
from filter import set_last_message, check_repeat_message
from server_data import init_server_ruleset

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
    try:
        mongo_client.admin.command('ping')
        # print(check_repeat_message(mongo_client, "123", "Wow!"))
        # set_last_message(mongo_client, "456", "Oh my god")
        print(check_repeat_message(mongo_client, "456", "OH MY GOD"))
        print("Successfully connected to MongoDB!")

        init_server_ruleset(mongo_client, guild)
    except Exception as e:
        print(e)
    await bot.add_cog(Moderation(bot))
    print("online")


@bot.event
async def on_guild_join(guild):
    print("Joining: " + str(guild.id))
    init_server_ruleset(mongo_client, guild.id)


@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
        print(ctx)
        print(f"{ctx.author} said: {ctx.content}")

        if ctx.content.startswith("-init"):
            server_data.init_server_ruleset(mongo_client, ctx.guild.id)

        repeated_message = check_repeat_message(mongo_client, ctx.author.id, ctx.content)
        if repeated_message:
            print(str(ctx.author) + " said " + ctx.content + " multiple times!")
        set_last_message(mongo_client, ctx.author.id, ctx.content)

        await bot.process_commands(ctx)

@bot.command()
async def judge(ctx, *, string: str = ""):
    # prompt = open("prompt.txt", 'r').read() + "\nCONTEXT DONE!"
    prompt = server_data.get_server_ruleset(mongo_client, ctx.guild.id)
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
        # prompt = open("prompt.txt", 'r').read() + "\nCONTEXT DONE!"
        prompt = server_data.get_server_ruleset(mongo_client, ctx.guild.id)
        time = genai_client.models.generate_content(model="gemini-2.0-flash-lite", contents = prompt+"User, "+str(ctx.author)+" says:"+str(ctx.message)+"Respond only with a time formatted as 'Days:Hours:Minutes' (for example '0:2:30') based on how long you think the user should be timed out for this offense.")
        times = time.text.split(':')
        print(times)
        try:
            await modActions.timeout(ctx, user, int(times[0]), int(times[1]), int(times[2]), reason=reason)
        except Exception as e:
            print("Error timing user out: " + e)

ruleset.setup(bot)
bot.run(DISCORD_API_KEY)
