import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import random
import os
import re

class ChatBox(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rdmeme(self, ctx):
        # สุ่มหน้าเว็บสำหรับการสุ่ม GIF
        pages = random.randint(1, 10)  # สุ่มหน้าเว็บจาก 1 ถึง 10 (ตัวอย่างเท่านั้น)
        url = f"https://giphy.com/search/meme"  # เปลี่ยน URL ตามที่คุณต้องการ

        # ทำร้องขอเข้าถึงหน้าเว็บและดึงเนื้อหา
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # ค้นหา URL ของ GIF จากเว็บ
        gif_urls = []
        for img in soup.find_all('img'):
            gif_urls.append(img['src'])

        # สุ่ม URL ของ GIF
        random_gif_url = random.choice(gif_urls)

        # ดาวน์โหลด GIF
        gif_response = requests.get(random_gif_url)
        gif_data = gif_response.content

        # แยกชื่อไฟล์และนามสกุลของไฟล์จาก URL
        file_name = re.search(r'/([^/]+\.[^/]+)$', random_gif_url).group(1)

        # บันทึกไฟล์ GIF ในโฟลเดอร์ชั่วคราว
        with open(file_name, 'wb') as f:
            f.write(gif_data)

        # ส่งไฟล์ GIF ไปยังแชท Discord
        with open(file_name, 'rb') as f:
            await ctx.send(file=discord.File(f))

        # ลบไฟล์ GIF ที่บันทึกชั่วคราว
        os.remove(file_name)

# เชื่อมต่อ cog กับ client
async def setup(client):
    await client.add_cog(ChatBox(client))