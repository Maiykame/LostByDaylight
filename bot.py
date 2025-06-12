import os
import discord
from discord.ext import commands

from Event.on_ready import on_ready_event
from Event.on_raw_reaction_add import on_raw_reaction_add_event
from Event.on_raw_reaction_remove import on_raw_reaction_remove_event

from Commands.help import help_command
from Commands.shrine import shrine_command
from Commands.sudo import sudo_command

from Mod_Commands.kick import kick_command

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
    await shrine_command(ctx)

@bot.command()
@commands.has_permissions(administrator=True)
async def sudo(ctx, message):
    await sudo_command(ctx, message)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Kein Grund angegeben"):
    kick_command(ctx, member, *, reason)

token = os.getenv("TOKEN")
if token is None:
    print("Fehlender TOKEN in Umgebungsvariablen")
else:
    bot.run(token)
