import discord
from discord.ext import commands
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)

prompt = "You are solely in charge of moderating a Discord server. You will be provided the rules. You will be asked to judge certain messages, you can respond exactly with 'remove', 'timeout','kick', or 'ban'"
result = client.models.generate_content(model="gemini-2.0-flash-lite", contents=prompt)

@commands.command(name="ruleset")
async def ruleset(ctx, getset: str, *, string: str = ""):
    if getset == "update":
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", contents="These rules are for a Discord Server, understand them because you will be moderating: " + string
        )
        await ctx.send(response.text[:2000])

    elif getset == "current":
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents="In under 2000 characters, what are the rules of this Discord Server?"
        )
        await ctx.send(response.text[:2000])

@commands.command(name="judge")
async def judge(ctx, *, string: str = ""):
    print(string)
    punishment = client.models.generate_content(model="gemini-2.0-flash-lite", contents=string)
    print(punishment.text)

def setup(bot):
    bot.add_command(ruleset)
    bot.add_command(judge)
