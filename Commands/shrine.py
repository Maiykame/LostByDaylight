import os
import discord
import requests

async def shrine_command(ctx):
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
