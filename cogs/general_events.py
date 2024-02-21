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

    #monitors who joins/leaves voice channels
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.mute is None or before.deaf is None:
            if not before.channel:
                print(f'{member} has joined vc {after.channel}')
            elif not after.channel:
                print(f'{member} has left vc {before.channel}')
            else:
                print(f'{member} has swapped vc channels: {before.channel} -> {after.channel}')
        

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

async def setup(bot):
    await bot.add_cog(GeneralEvents(bot))