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
    user_message = message.content
    print(f"User said: {user_message}")
    if "orwell, " in user_message.lower():
        print("1")
        response=client.models.generate_content(model="gemini-2.0-flash", contents= "be very brief:"+message.content)
        print("2")
        await message.channel.send(response.text[:2000])
    print("3")
    await bot.process_commands(message)

bot.run("X")
