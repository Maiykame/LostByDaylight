import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Wichtig für Befehle ab API v2

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ist eingeloggt als {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

token = os.getenv("TOKEN")
if token is None:
    print("Fehlender TOKEN in Umgebungsvariablen")
else:
    bot.run(token)
