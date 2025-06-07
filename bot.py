import os
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.message_content = True  # Wichtig für Befehle ab API v2

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Bot ist eingeloggt als {bot.user}")

@bot.command()
async def ping(ctx):
    print(f"[INFO] {ctx.author} ({ctx.author.id}) benutzte '!ping'.")
    await ctx.send("Pong!")

PERK_API_URL = "https://dbd-api.herokuapp.com/perks"

def get_shrine_perks():
    url = "https://nightlight.gg/shrine"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    perk_elements = soup.select("h2.text-xl.font-semibold")
    perks = [el.text.strip() for el in perk_elements[:4]]
    return perks

def get_perk_data(perk_name):
    res = requests.get(PERK_API_URL)
    if res.status_code != 200:
        return None

    all_perks = res.json()
    for perk in all_perks:
        if perk["name"].lower() == perk_name.lower():
            return perk
    return None

@bot.command()
async def shrine(ctx):
    print(f"[INFO] {ctx.author} ({ctx.author.id}) benutzte '!shrine'.")
    try:
        perk_names = get_shrine_perks()
        embeds = []

        for name in perk_names:
            perk = get_perk_data(name)
            if perk:
                embed = discord.Embed(
                    title=perk["name"],
                    description=perk["description"],
                    color=0xA71F2A
                )
                embed.set_thumbnail(url=perk["icon"])
                embeds.append(embed)
            else:
                await ctx.send(f"Konnte keine Daten zu **{name}** finden.")

        for embed in embeds:
            await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"Fehler beim Abrufen der Shrine-Daten: {e}")

token = os.getenv("TOKEN")
if token is None:
    print("Fehlender TOKEN in Umgebungsvariablen")
else:
    bot.run(token)
