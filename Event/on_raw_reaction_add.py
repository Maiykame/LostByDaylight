from Misc.create_reaction_message import reaction_role_messages

async def on_raw_reaction_add_event(bot, payload):
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
