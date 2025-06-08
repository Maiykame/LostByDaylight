import os
import discord
from discord.ext import commands
import requests

# Globale Mapping-Tabelle für Reaction Roles
reaction_role_messages = {}

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

@bot.event
async def on_ready():
    print(f"Bot ist eingeloggt als {bot.user}")
    await create_reaction_message(1381197888985763910, {
        "💻": 1364631941307043972, # PC
        "🎮": 1364631972621844541, # Playstation
        "🟢": 1364632015042908180, # XBox
        "🔴": 1364632054335144056# Switch
    })

async def create_reaction_message(message_id: int, emoji_role_map: dict):
    reaction_role_messages[message_id] = emoji_role_map

    # Hole Nachricht, um Reaktionen zu setzen
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                message = await channel.fetch_message(message_id)
                for emoji in emoji_role_map:
                    await message.add_reaction(emoji)
                return
            except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                continue

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id not in reaction_role_messages:
        return

    emoji_map = reaction_role_messages[payload.message_id]
    role_id = emoji_map.get(str(payload.emoji))
    if not role_id:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    role = guild.get_role(role_id)

    if guild and member and role and not member.bot:
        await member.add_roles(role)
        print(f"✅ Rolle {role.name} zugewiesen an {member.name}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id not in reaction_role_messages:
        return

    emoji_map = reaction_role_messages[payload.message_id]
    role_id = emoji_map.get(str(payload.emoji))
    if not role_id:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    role = guild.get_role(role_id)

    if guild and member and role and not member.bot:
        await member.remove_roles(role)
        print(f"❌ Rolle {role.name} entfernt von {member.name}")

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
