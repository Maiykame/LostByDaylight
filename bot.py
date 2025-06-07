import os
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

@bot.event
async def on_ready():
    print(f"Bot ist eingeloggt als {bot.user}")

@bot.command()
async def ping(ctx):
    print(f"[INFO] {ctx.author} ({ctx.author.id}) benutzte '!ping'.")
    await ctx.send("Pong!")

@bot.command()
async def shrine(ctx):
    url = "https://api.nightlight.gg/v1/shrine?pretty=true"
    res = requests.get(url)

    if res.status_code != 200:
        await ctx.send(f"Fehler: Status-Code {res.status_code}")
        return

    text = res.text
    # Die Perks sind durch Kommas getrennt, vor dem '|'
    perks_part = text.split('|')[0].strip()
    perks = [p.strip() for p in perks_part.split(',')]

    msg = "**Aktuelle Shrine of Secrets Perks:**\n" + "\n".join(f"- {perk}" for perk in perks)
    await ctx.send(msg)

token = os.getenv("TOKEN")
if token is None:
    print("Fehlender TOKEN in Umgebungsvariablen")
else:
    bot.run(token)
