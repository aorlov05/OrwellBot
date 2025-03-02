import discord
from discord.ext import commands
from google import genai
import os
from dotenv import load_dotenv
from server_data import set_server_ruleset, get_server_ruleset
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)
MONGODB_URI = os.environ.get('MONGODB_URI')
mongo_client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))

@commands.command(name="ruleset")
async def ruleset(ctx, getset: str, *, string: str = ""):
    prompt = get_server_ruleset(mongo_client, ctx.guild.id)
    print(getset)
    if getset == "update":
        print("UPDATING")
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", contents="You are updating a Discord server's ruleset. You will receive a list of rules, and your task is to extract and format them into clear, specific rules and punishments. Your response will be directly added to a text file, so format it exactly as required without any extra text or explanations.\nDo not add any rules that are not explicitly stated.\nDo not include acknowledgments like 'Okay, I understand.'\nOnly output the rules and punishments in a concise, structured format.\nExample Format:\nBan users who say cheese.\nKick users who are being homophobic.\nNow, process the following ruleset and return only the formatted rules and punishments"+ string
        )
        set_server_ruleset(mongo_client, ctx.guild.id, response.text)
    if getset == "current":
        print("CURRENTLY")
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt+"In under 2000 characters, what are the rules outlined?"
        )
        await ctx.send(response.text[:2000])
    if (getset.lower() == "clear"):
        open("prompt.txt", "w").write("")
    if (getset.lower() == "delete"):
        response=client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents="Please look through the ruleset and delete the rule closest matching to this: " +string+" Here is the ruleset, return it exactly how it is now, only deleting the selected rule. Do not affirm: "+prompt
        )
        with open("prompt.txt", "a") as file:
            file.write("\n"+response.text)
            file.flush()
            file.close()

def setup(bot):
    bot.add_command(ruleset)

