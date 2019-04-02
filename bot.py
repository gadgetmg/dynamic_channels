import discord
import os
import re

class Bot(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_voice_state_update(self, member, before, after):
        # Get the channel's basename
        def get_basename(channel):
            match = re.search("^(.*) [0-9]*$", channel.name)
            if match is not None:
                return match.group(1)

        # Get the channel's iteration
        def get_iteration(channel):
            match = re.search("^.* ([0-9]*)$", channel.name)
            if match is not None:
                return int(match.group(1))

        # If the channels match, the member only muted or unmuted
        if before.channel == after.channel:
            return

        # Channel just joined by the first member
        if after.channel and re.match("^.* [0-9]*$", after.channel.name) and len(after.channel.members) == 1:
            # Add a new channel
            channel = await member.guild.create_voice_channel(
                # Create with all the attributes from the current channel
                name=get_basename(after.channel) + " " + str(get_iteration(after.channel) + 1),
                overwrites=dict(after.channel.overwrites),
                category=after.channel.category,
                position=after.channel.position,
                bitrate=after.channel.bitrate,
                user_limit=after.channel.user_limit
            )
            # In some cases (position 0), the API won't respect the position of the new channel
            if channel.position != after.channel.position:
                await channel.edit(
                    # When editing, position has to be 1 greater
                    position=after.channel.position + 1
                )
            # Renumber the position of voice channels as Discord doesn't respect its own documentation
            for i, channel in enumerate(member.guild.voice_channels):
                if channel.position != i:
                    await channel.edit(
                        position = i
                    )

        # Channel just left
        if before.channel and re.match("^.* [0-9]*$", before.channel.name):
            def filter_channel_group(channel):
                # Channel must be in the same category
                if channel.category_id != before.channel.category_id:
                    return False
                # Basenames have to match
                elif get_basename(channel) != get_basename(before.channel):
                    return False
                else:
                    return True

            # Get a list of all the channels in the group
            channel_group = list(filter(filter_channel_group, member.guild.channels))

            empty = 0
            for channel in channel_group:
                # Count empty channels
                if len(channel.members) == 0:
                    empty += 1

            iteration = 1
            for channel in channel_group:
                # Delete all but one of the empty channels
                if empty > 1 and len(channel.members) == 0:
                    await channel.delete()
                    empty -= 1
                else:
                    # Renumber the rest of the channels to be sequential
                    if get_iteration(channel) != iteration:
                        await channel.edit(
                            name=get_basename(channel) + " " + str(iteration)
                        )
                    iteration += 1

bot = Bot()
bot.run(os.environ.get('API_KEY'))
