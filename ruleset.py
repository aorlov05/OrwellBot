import discord
from discord.ext import commands
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)

@commands.command(name="ruleset")
async def ruleset(ctx, getset: str, *, string: str = ""):
    prompt = open("prompt.txt", 'r').read() + "\nCONTEXT DONE!"
    print(getset)
    if getset == "update":
        print("UPDATING")
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", contents="You are updating a Discord server's ruleset. You will receive a list of rules, and your task is to extract and format them into clear, specific rules and punishments. Your response will be directly added to a text file, so format it exactly as required without any extra text or explanations.\nDo not add any rules that are not explicitly stated.\nDo not include acknowledgments like 'Okay, I understand.'\nOnly output the rules and punishments in a concise, structured format.\nExample Format:\nBan users who say cheese.\nKick users who are being homophobic.\nNow, process the following ruleset and return only the formatted rules and punishments"+ string
        )
        with open("prompt.txt", "a") as file:
            file.write("\n"+response.text)
            file.flush()
            file.close()
    if getset == "current":
        print("CURRENTLY")
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt+"In under 2000 characters, what are the rules of this Discord Server?"
        )
        await ctx.send(response.text[:2000])

@commands.command(name="judge")
async def judge(ctx, *, string: str = ""):
    prompt = open("prompt.txt", 'r').read() + "\nCONTEXT DONE!"
    punishment = client.models.generate_content(model="gemini-2.0-flash-lite", contents=prompt+"User, "+str(ctx.author)+" says:"+string+"Respond only with 'kick', 'ban', or 'timeout'")
    print(punishment.text)

def setup(bot):
    bot.add_command(ruleset)
    bot.add_command(judge)
