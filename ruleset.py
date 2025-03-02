import discord
from discord.ext import commands
from google import genai
import os
from dotenv import load_dotenv
from server_data import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)
MONGODB_URI = os.environ.get('MONGODB_URI')
mongo_client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))

@commands.command(name="ruleset")
async def ruleset(ctx, arg: str, *, string: str = ""):
    """
    Depending on the argument, ruleset can update the MongoDB database

    Parameters:
    ctx: command context
    arg: helper argument to modify the ruleset
    string: the ruleset string

    Returns:
    None
    """
    prompt = get_server_ruleset(mongo_client, ctx.guild.id)
    match arg.lower():
        case "view":
            response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt + "In under 2000 characters, what are the rules outlined?")
            embed = discord.Embed(
                description=response.text[:2000], color=0x3D8EFF
            )
            await ctx.send(embed=embed)
        case "replace":
            response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents="You are updating a Discord server's ruleset. You will receive a list of rules, and your task is to extract and format them into clear, specific rules and punishments. Your response will be directly added to a text file, so format it exactly as required without any extra text or explanations.\nDo not add any rules that are not explicitly stated.\nDo not include acknowledgments like 'Okay, I understand.'\nOnly output the rules and punishments in a concise, structured format.\n DO NOT ADD ANY RULES THAT ARE NOT EXPLICITLY STATED IN THE MESSAGE\nExample Format:\nBan users who say cheese.\nKick users who are being homophobic.\nNow, process the following ruleset and return only the formatted rules and punishments" + string)
            set_server_ruleset(mongo_client, ctx.guild.id, response.text)
        case "clear":
            set_server_ruleset(mongo_client, ctx.guild.id, "")
        case "add":
            response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents="You are updating a Discord server's ruleset. You will receive a list of rules, and your task is to extract and format them into clear, specific rules and punishments. Your response will be directly added to a text file, so format it exactly as required without any extra text or explanations.\nDo not add any rules that are not explicitly stated.\nDo not include acknowledgments like 'Okay, I understand.'\nOnly output the rules and punishments in a concise, structured format.\n DO NOT ADD ANY RULES THAT ARE NOT EXPLICITLY STATED IN THE MESSAGE\nExample Format:\nBan users who say cheese.\nKick users who are being homophobic.\nNow, process the following ruleset and return only the formatted rules and punishments" + string)
            add_server_ruleset(mongo_client, ctx.guild.id, response.text)
        case "help":
            embed=discord.Embed(
                description="Available subcommands: view, add, replace, clear, or help",color=0x3D8EFF
            )
            await ctx.send(embed=embed)
        case _:
            embed=discord.Embed(
                description="Invalid usage. Please provide one of the following options: view, add, replace, clear, or help. Usage example: -ruleset view",color=0xFF0000
            )
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_command(ruleset)

