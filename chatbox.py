import discord
from discord.ext import commands
import aiohttp
import random
import re
import os
from bs4 import BeautifulSoup

class ChatBox(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rdmeme(self, ctx):
        async with aiohttp.ClientSession() as session:
            pages = random.randint(1, 10)
            url = f"https://giphy.com/search/meme?page={pages}"

            async with session.get(url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')

                gif_urls = [img['src'] for img in soup.find_all('img') if re.search(r'\.gif', img['src'])]
                if not gif_urls:
                    await ctx.send("ไม่พบ GIF ในหน้านี้")
                    return

                random_gif_url = random.choice(gif_urls)

                async with session.get(random_gif_url) as gif_response:
                    gif_data = await gif_response.read()

                file_name = "random_meme.gif"

                with open(file_name, 'wb') as f:
                    f.write(gif_data)

                with open(file_name, 'rb') as f:
                    await ctx.send(file=discord.File(f))

                os.remove(file_name)

# เชื่อมต่อ cog กับ client
async def setup(client):
    await client.add_cog(ChatBox(client))
