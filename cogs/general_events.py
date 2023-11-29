import discord
from discord.ext import commands
import datetime

CHANNEL_NAME = "polibot-moderation"

class GeneralEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is online!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined guild: {guild.name}")

        channel_name = "polibot-moderation"
        role_name = "PMod"
        role_ID = 0

        existing_role = discord.utils.get(guild.roles, name=role_name)
        if existing_role:
            print(f'{existing_role} role already exists in the server {guild.name}')
            role_ID = existing_role.id
        else:
            new_role = await guild.create_role(name=role_name)
            print(f'The role "{role_name}" has been created with the ID: {new_role.id} in server {guild.name}')
            role_ID = new_role.id

        channel = discord.utils.get(guild.channels, name=channel_name)
        if channel:
            await channel.send('channel is already created')
            print('channel is already created')
        else:
            print(f'creating channel for {guild.name}')
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages = False),
                guild.me: discord.PermissionOverwrite(read_messages = True),
                guild.get_role(role_ID): discord.PermissionOverwrite(read_messages = True)
            }
            poliswag_mod = await guild.create_text_channel(channel_name, overwrites=overwrites)
            print(f'moderation channel sucessfully created for {guild.name}')
            await poliswag_mod.send(f'channel created :sunglasses: and is a private channel for {role_name}s')

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry):
        timeLog = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print('there is an audit log entry, something is happening')
        currGuild = entry.guild
        channel = discord.utils.get(currGuild.channels, name=CHANNEL_NAME)
        if entry.action == discord.AuditLogAction.member_role_update:
            #await channel.send("A MEMBER'S ROLE HAS BEEN UPDATED; TBD\n" + str(entry.before.roles) + "->" + str(entry.after.roles) + "\n" + str(type(entry.after.roles)))
            user = entry.target
            roles_before = entry.before.roles
            roles_after = entry.after.roles

            if roles_after:
                for r in roles_after:
                    await channel.send(f'***{timeLog}***: {user} has new role ***ADDED***: {r}')
            elif roles_before:
                for r in roles_before:
                    await channel.send(f'***{timeLog}***: {user} has new role ***REMOVED***: {r}')


    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

async def setup(bot):
    await bot.add_cog(GeneralEvents(bot))