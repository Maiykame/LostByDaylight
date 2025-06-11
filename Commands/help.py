import discord

async def help_command(ctx):
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
