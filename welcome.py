# welcome.py
import discord
from discord.ext import commands
import json

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        
        with open('config.json', 'r') as f:
            config = json.load(f)

        if guild_id in config["guilds"]:
            channel_id = config["guilds"][guild_id]["welcome_channel_id"]
            if channel_id == str(member.guild.id):  # Check if the welcome channel is for the current guild
                channel = self.client.get_channel(int(channel_id))

                if channel:
                    server_name = member.guild.name
                    welcome_message = (
                        f"**ยินดีต้อนรับ {member.mention} เข้าสู่เซิร์ฟเวอร์ {server_name.upper()}!**\n"
                        "ขอให้สนุกกับการพูดคุยกันนะ!"
                    )
                    
                    # Embed message to include profile picture
                    embed = discord.Embed(
                        title="**•´¨`*:•.Welcome <3*.:｡*ﾟ‘ﾟ･.｡.**",
                        description=welcome_message,
                        color=discord.Color.green()
                    )
                    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

                    await channel.send(embed=embed)
        else:
            print(f"ยังไม่ได้ตั้งค่าห้อง welcome_channel_id ในเซิร์ฟเวอร์: {member.guild.name}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setwelcomechannel(self, ctx, channel_id: int):
        guild_id = str(ctx.guild.id)

        with open('config.json', 'r') as f:
            config = json.load(f)

        if guild_id not in config["guilds"]:
            config["guilds"][guild_id] = {}
        
        config["guilds"][guild_id]["welcome_channel_id"] = channel_id

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f'Successfully set welcome channel to <#{channel_id}>.')

# Connect cog to client
async def setup(client):
    await client.add_cog(Welcome(client))