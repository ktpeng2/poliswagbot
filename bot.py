import discord
from discord.ext import commands
from discord.ext.commands import MemberNotFound

import config

import db_CRUD as db

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'poliswag bot up and ready to go\t{bot.user.name} online')

@bot.event
async def on_guild_join(guild):

    #outputting any new server joins
    print(f'joined {guild.name}: {guild.id}')
    
    #init variables
    channel_name = "polibot-moderation"
    role_name = "polibot-moderation"
    roleID = 0

    #creating moderation variable for members that will be able to see the chat
    existing_role = discord.utils.get(guild.roles, name=role_name)
    if existing_role:
        print(f'{existing_role} role already exists in server {guild.name}')
        roleID = existing_role.id
    else:
        new_role = await guild.create_role(name=role_name)
        print(f"The role '{role_name}' has been created with the ID: {new_role.id} in server {guild.name}")
        roleID = new_role.id

    #creating moderation channel, allowing the bot and the moderation role created above able to read it
    channel = discord.utils.get(guild.channels, name=channel_name)
    if channel:
        await channel.send('channel is already created')
        print('channel is alredy created')
    else:
        print(f'creating channel for {guild.name}')
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            guild.get_role(roleID): discord.PermissionOverwrite(read_messages=True),
        }
        poliswag_mod = await guild.create_text_channel(channel_name, overwrites=overwrites)
        print(f'moderation channel sucessfully created for {guild.name}')
        await poliswag_mod.send('channel created :sunglasses: and is a private channel')

@bot.event
async def on_member_update(before, after):
    guild = after.guild
    channel = discord.utils.get(guild.channels, name="polibot-moderation")
    if before.name != after.name:
        await channel.send(f"```Username changed:\n{before.name} -> {after.name}```")
        print(f"Username changed: {before.name} -> {after.name}")

    if before.nick != after.nick:
        await channel.send(f"```User {after.name} changed nickname:\n{before.nick} -> {after.nick}```")
        print(f"User {after.name} changed nickname: {before.nick} -> {after.nick}")

@bot.event
async def on_member_remove(member):
    message = f"Member {member.name} has left the server."
    print(message)
    guild = member.guild
    channel = guild.system_channel  # Get the system channel of the guild (where welcome messages are usually sent)

    if channel is not None:
        message = f"{member.display_name} has left the server."  # Customize the message as desired
        await channel.send(message)

@commands.command()
async def curr_server_info(ctx, arg):
    await ctx.send(f'command being run in: {ctx.guild.id} \({ctx.guild.name}\)')

@commands.command()
async def lookup(ctx, username):
    guild = ctx.guild

    member = discord.utils.find(lambda m: m.name == username, guild.members)
    if member is not None:
        await ctx.send(f'Unique ID: {member.id}\nUsername: {member.name}\nDisplay Name: {member.display_name}\nGlobal Name: {member.global_name}')
    else:
        await ctx.send("Member not found in the server.")

@commands.command()
async def manual_add_server(ctx):
    guildID = ctx.guild.id
    guildName = ctx.guild.name
    print(type(guildID))
    print(len(str(guildID)))

    await ctx.send('adding server into db')
    db.insertTest(guildID, guildName)
    await ctx.send('server insert to db sucessful, do a manual check')

@commands.command()
async def resetTables(ctx):
    db.resetTables()

@commands.command()
async def createDB(ctx):
    db.create_Database()

@commands.command()
async def createTables(ctx):
    db.create_Tables()

@commands.command()
async def manual_insert_user(ctx, username):
    guild = ctx.guild
    member = discord.utils.find(lambda m: m.name == username, guild.members)
    if member is not None:
        db.insertUser(guild.id, member.id)
    else:
        await ctx.send("Member not found in the server.")

@commands.command()
async def removeGuild(ctx):
    guild = ctx.guild
    db.removeGuild(guild.id)

@commands.command()
async def cycle(ctx):
    guild = ctx.guild
    memString = ""
    for member in guild.members:
        memString += str(member.id) + " : " + str(member.name) + "\n"

    await ctx.send(memString)


bot.add_command(curr_server_info)
bot.add_command(lookup)
bot.add_command(manual_add_server)
bot.add_command(resetTables)
bot.add_command(createDB)
bot.add_command(createTables)
bot.add_command(manual_insert_user)
bot.add_command(removeGuild)
bot.add_command(cycle)


bot.run(config.TOKEN)