import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot_commands import setup_commands


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
setup_commands(bot)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    print("Slash commands synced")

@bot.event
async def setup_hook():
    await bot.tree.sync()


bot.run(TOKEN)