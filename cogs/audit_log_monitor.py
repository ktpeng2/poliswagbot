import discord
from discord.ext import commands
import datetime
from pytz import timezone

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


def memberUpdate(entry, timelog):
    for r in entry.before:
        if r[0] == 'mute':
            if entry.after.mute:
                activityStr = str(f'{entry.user} has muted {entry.target}')
                print(activityStr)
                return activityStr
            else:
                activityStr = str(f'{entry.user} has unmuted {entry.target}')
                print(activityStr)
                return activityStr
        elif r[0] == 'deaf':
            if entry.after.deaf:
                activityStr = str(f'{entry.user} has deafened {entry.target}')
                print(activityStr)
                return activityStr
            else:
                activityStr = str(f'{entry.user} has undeafened {entry.target}')
                print(activityStr)
                return activityStr
        elif r[0] == 'timed_out_until':
            format = "%m-%d-%Y %H:%M:%S"
            now_cst = entry.before.timed_out_until.astimezone(timezone('America/Chicago'))
            activityStr = str(f'{entry.user} has timed out {entry.target} until {now_cst.strftime(format)}')
            print(activityStr)
            return activityStr
        elif r[0] == 'nick':
            if entry.user != entry.target:
                activityStr = str(f'{entry.user} has changed the nickname of {entry.target}: {entry.before.nick} -> {entry.after.nick}')
                print(str(f'{entry.user} has changed the nickname of {entry.target}: {entry.before.nick} -> {entry.after.nick}'))
                return activityStr
            else:
                activityStr = str(f'{entry.target} has changed their nickname: {entry.before.nick} -> {entry.after.nick}')
                print(activityStr)
                return activityStr

def memberRoleUpdate(entry, timeLog):
    user = entry.target
    roles_before = entry.before.roles
    roles_after = entry.after.roles

    if roles_after:
        for r in roles_after:
            activityStr = str(f'***{timeLog}***: {user} has new role ***ADDED***: {r}')
            print(activityStr)
            return activityStr
    elif roles_before:
        for r in roles_before:
            activityStr = str(f'***{timeLog}***: {user} has new role ***REMOVED***: {r}')
            print(activityStr)
            return activityStr

def member_move(entry, timeLog):
    activityStr = str(f'{entry.user} has moved a user to a different vc')
    print(activityStr)
    return activityStr

def member_disconnect(entry, timeLog):
    activityStr = str(f'{entry.user} has disconnected a user')
    print(activityStr)
    return activityStr

class AuditLogMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry):
        timeLog = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print('there is an audit log entry, something is happening')
        currGuild = entry.guild
        channel = discord.utils.get(currGuild.channels, name=CHANNEL_NAME)
        discordALA = discord.AuditLogAction
        discordALD = discord.AuditLogDiff
        match entry.action:
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
                print(f'{entry.action}')
                match entry.action:
                    case discordALA.member_update:
                        await channel.send(memberUpdate(entry, timeLog))
                    case discordALA.member_role_update:
                        await channel.send(memberRoleUpdate(entry, timeLog))
                    case discordALA.member_move:
                        await channel.send(member_move(entry, timeLog))
                    case discordALA.member_disconnect:
                        await channel.send(member_disconnect(entry, timeLog))
                #TODO: break down the member log actions and write meaningful blocks for each

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
            
                
async def setup(bot):
    await bot.add_cog(AuditLogMonitor(bot))