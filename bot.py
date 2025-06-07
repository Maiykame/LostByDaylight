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
    print(f"[INFO] {ctx.author} ({ctx.author.id}) benutzte '!shrine'.")
    try:
        url = "https://api.nightlight.gg/v1/shrine?pretty=true"
        res = requests.get(url)
        res.raise_for_status()

        data = res.json()
        perks = data.get("perks", [])
        if not perks:
            await ctx.send("Keine Shrine-Perks gefunden.")
            return

        # Nur die Namen extrahieren
        perk_names = [perk["name"] for perk in perks]

        # Sende als formatierte Liste
        msg = "**Aktuelle Shrine of Secrets Perks:**\n" + "\n".join(f"- {name}" for name in perk_names)
        await ctx.send(msg)

    except Exception as e:
        await ctx.send(f"Fehler beim Abrufen der Shrine-Daten: {e}")

token = os.getenv("TOKEN")
if token is None:
    print("Fehlender TOKEN in Umgebungsvariablen")
else:
    bot.run(token)
