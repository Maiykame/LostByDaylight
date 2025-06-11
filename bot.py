import os
import discord
from discord.ext import commands
import requests

from Event.on_ready import on_ready_event
from Event.on_raw_reaction_add import on_raw_reaction_add_event
from Event.on_raw_reaction_remove import on_raw_reaction_remove_event

from Commands.help import help_command

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

@bot.event
async def on_ready():
    await on_ready_event(bot)

@bot.command()
async def help(ctx):
    await help_command(ctx)

@bot.event
async def on_raw_reaction_add(payload):
    await on_raw_reaction_add_event(bot, payload)

@bot.event
async def on_raw_reaction_remove(payload):
    await on_raw_reaction_remove_event(bot, payload)

@bot.command()
async def shrine(ctx):
    url = "https://api.nightlight.gg/v1/shrine?pretty=true"
    res = requests.get(url)

    if res.status_code != 200:
        await ctx.send(f"❌ Fehler beim Abrufen der Shrine-Daten. Status-Code: {res.status_code}")
        return

    text = res.text
    perks_part = text.split('|')[0].strip()
    perks = [p.strip() for p in perks_part.split(',')]

    embed = discord.Embed(
        title="🛐 Aktuelle Shrine of Secrets",
        description="\n".join(f"- {perk}" for perk in perks),
        color=discord.Color.dark_red()
    )
    embed.set_footer(text="Daten von nightlight.gg")

    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def sudo(ctx, *, message):
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass
    await ctx.send(message)

token = os.getenv("TOKEN")
if token is None:
    print("Fehlender TOKEN in Umgebungsvariablen")
else:
    bot.run(token)
