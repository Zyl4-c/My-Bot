import discord
from discord.ext import commands

class DMMember(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # สร้าง embed
        embed = discord.Embed(
            title="ยินดีต้อนรับ!",
            description=f"สวัสดีค่ะ {member.name}! ยินดีต้อนรับสู่เซิร์ฟเวอร์ของเรา\nถ้าหากหาห้องไม่เจอให้กด ลิงค์นี้ https://discord.com/channels/888357875938885632/973039956291387412 \nและกดที่รูปเครื่องหมายถูกเพื่อรับยศมองเห็นห้องได้เลย",
            color=discord.Color.dark_purple()
        )
        # ส่ง embed ใน DM
        await member.send(embed=embed)

# เชื่อมต่อ cog กับ client
async def setup(client):
    await client.add_cog(DMMember(client)) 