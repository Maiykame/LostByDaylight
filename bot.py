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
    await create_reaction_message(1381198483746324572, {
        "💻": 1364631941307043972, # PC
        "🎮": 1364631972621844541, # Playstation
        "🟢": 1364632015042908180, # XBox
        "🔴": 1364632054335144056# Switch
    })
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name='!help')
    )

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📖 Hilfe – Befehlsübersicht",
        description="Liste aller verfügbaren Befehle:",
        color=discord.Color.blurple()
    )

    commands_info = [
        ("!help", "Zeigt diese Hilfeseite an."),
        ("!shrine", "Zeigt den zurzeitigen Shrine of Secrets an."),
    ]

    for name, desc in commands_info:
        embed.add_field(name=name, value=desc, inline=False)

    embed.set_footer(text="Bot entwickelt von Maiykame")

    await ctx.send(embed=embed)

async def create_reaction_message(message_id: int, emoji_role_map: dict):
    reaction_role_messages[message_id] = emoji_role_map

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
    res = requests.get("https://api.nightlight.gg/v1/shrine?pretty=true")
    if res.status_code != 200:
        return await ctx.send(f"❌ Fehler: Status-Code {res.status_code}")
    shrine_names = [p.strip() for p in res.text.split('|')[0].split(',')]

    all_perks = requests.get("https://api.nightlight.gg/v1/perks").json()
    perks = [p for p in all_perks if p["name"] in shrine_names]

    embed = discord.Embed(
        title="🛐 Shrine of Secrets – Aktuelle Perks",
        color=discord.Color.dark_purple()
    )
    for p in perks:
        embed.add_field(
            name=f'{p["name"]} ({p["role"]} – {p["character"]})',
            value=p["description"],
            inline=False
        )
    embed.set_footer(text="Daten via nightlight.gg")
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
