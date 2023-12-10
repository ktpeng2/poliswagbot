import discord
from discord.ext import commands
import datetime

CHANNEL_NAME = "polibot-moderation"

def checkAuditLogFields(entry):
    if entry.action:
        print(f'there is an action {entry.action}')
    if entry.after:
        print(f'there is an after: {entry.after}')
    if entry.before:
        print(f"there is a before: {entry.before}")
    if entry.category:
        print(f'there is a category: {entry.category}')
    if entry.changes:
        print(f'there is a change: {entry.changes}')
    if entry.changed_at:
        print(f'there is a change timestamp: {entry.changed_at}')
    if entry.extra:
        print(f'there is an extra: {entry.extra}')
    if entry.guild:
        print(f'there is a guild: {entry.guild}')
    if entry.id:
        print(f'there is an id: {entry.id}')
    if entry.reason:
        print(f'there is a reason: {entry.reason}')
    if entry.target:
        print(f'there is a target: {entry.target}')
    if entry.user:
        print(f'there is a user: {entry.user}')
    if entry.user_id:
        print(f'there is a userid: {entry.user_id}')

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
        discordALA = discord.AuditLogAction
        match entry.action:
            case discordALA.member_role_update:
                user = entry.target
                roles_before = entry.before.roles
                roles_after = entry.after.roles

                if roles_after:
                    for r in roles_after:
                        await channel.send(f'***{timeLog}***: {user} has new role ***ADDED***: {r}')
                elif roles_before:
                    for r in roles_before:
                        await channel.send(f'***{timeLog}***: {user} has new role ***REMOVED***: {r}')
            case discordALA.guild_update:
                #checkAuditLogFields(entry)
                await channel.send(f'Something was modified for the server, check the logs\n\t(kt did not want to code all like 10 paths ***TODO***)')

            case discordALA.channel_create | discordALA.channel_update | discordALA.channel_delete:
                #TODO: break down into the 3 sub actions of channel updates
                await channel.send(f'There was a channel that was modified (created, updated, or deleted)')
            case discordALA.overwrite_create | discordALA.overwrite_update | discordALA.overwrite_delete:
                #TODO: look into overwrites
                await channel.send(f'There was a discord overwrite @penguitte look at this so u know what an overwrite is')
            case discordALA.kick | discordALA.member_prune | discordALA.ban | discordALA.unban:
                #TODO: specify 4 different events and write meaningful specific messages for each case
                await channel.send(f'covers a member kick, member prune, ban, or unban')
            case discordALA.member_update | discordALA.member_role_update | discordALA.member_move | discordALA.member_disconnect:
                #TODO: break down the member log actions and write meaningful blocks for each
                await channel.send(f'covers anything that has to do with members')
            case discordALA.bot_add | discordALA.invite_create | discordALA.invite_delete | discordALA.invite_update:
                #TODO: break down invite events
                await channel.send(f'a bot was added, or invite was created/deleted/updated')
            case discordALA.webhook_create | discordALA.webhook_delete | discordALA.webhook_update:
                #TODO: break down webhook events
                await channel.send(f'somethin was done with da webhooks')
            case discordALA.emoji_create | discordALA.emoji_delete | discordALA.emoji_update:
                #TODO: break down emoji actions
                await channel.send(f'something was done to the emojis')
            case discordALA.message_bulk_delete | discordALA.message_delete | discordALA.message_pin | discordALA.message_unpin:
                #TODO: break down message events
                await channel.send(f'something was modified to a message(s)')
            case discordALA.integration_create | discordALA.integration_delete | discordALA.integration_update:
                #TODO: break down integration events
                await channel.send(f'there was an integration event idk what this is check it out')
            case discordALA.stage_instance_create | discordALA.stage_instance_delete | discordALA.stage_instance_update:
                #TODO: break down stage instance events
                await channel.send(f'there was an stage instance event; idk what this is check it out if it occurs')
            case discordALA.sticker_create | discordALA.sticker_delete | discordALA.sticker_update:
                #TODO: break down sticker events
                await channel.send(f'there was an sticker event')
            case discordALA.scheduled_event_create | discordALA.scheduled_event_delete | discordALA.scheduled_event_update:
                #TODO: break down scheduled events event
                await channel.send(f'there was a event event')
            case discordALA.thread_create | discordALA.thread_delete | discordALA.thread_update:
                #TODO: break down thread events
                await channel.send(f'there was a thread event')
            case discordALA.app_command_permission_update:
                #TODO: what is this
                await channel.send('there was an app command permission update; what is this')
            case discordALA.automod_rule_create | discordALA.automod_rule_delete | discordALA.automod_rule_update:
                #TODO: automod rules?
                await channel.send('there was an event with automod rules')
            case discordALA.automod_block_message | discordALA.automod_flag_message | discordALA.automod_timeout_member:
                #TODO: automod moderation
                await channel.send(f'there was a automod moderation event')

        #await channel.send(f'Something was updated in the server: {entry.action}')

 
        


    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

async def setup(bot):
    await bot.add_cog(GeneralEvents(bot))