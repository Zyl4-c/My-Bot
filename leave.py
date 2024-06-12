import discord
from discord.ext import commands
import json

class Leave(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = str(member.guild.id)
        
        with open('config.json', 'r') as f:
            config = json.load(f)

        if guild_id in config["guilds"]:
            channel_id = config["guilds"][guild_id]["quit_channel_id"]
            if channel_id == str(member.guild.id):  # Check if the quit channel is for the current guild
                channel = self.client.get_channel(int(channel_id))

                if channel:
                    server_name = member.guild.name
                    leave_message = (
                        f"**{member.name} ได้ออกจากเซิร์ฟเวอร์ {server_name.upper()} แล้ว!**\n"
                        "ขอให้คุณโชคดี!"
                    )
                    
                    # Embed message to include profile picture
                    embed = discord.Embed(
                        title="**•´¨`*:•.Bye Bye*.:｡*ﾟ‘ﾟ･.｡.**",
                        description=leave_message,
                        color=discord.Color.red()
                    )
                    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

                    await channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setquitchannel(self, ctx, channel_id: int):
        guild_id = str(ctx.guild.id)

        with open('config.json', 'r') as f:
            config = json.load(f)

        if guild_id not in config["guilds"]:
            config["guilds"][guild_id] = {}
        
        config["guilds"][guild_id]["quit_channel_id"] = channel_id

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f'Successfully set quit channel to <#{channel_id}>.')

# Connect cog to client
async def setup(client):
    await client.add_cog(Leave(client))