import discord
from discord.ext import commands
import yt_dlp
import asyncio

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.is_paused = False
        self.is_looping = False
        self.current_song = None
        self.voice_client = None
        self.queue = []

    @commands.command()
    async def play(self, ctx, *, search: str):
        voice_client = ctx.guild.voice_client

        if not voice_client:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                voice_client = await channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel")
                return

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'default_search': 'ytsearch1'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            url = info.get('url', '')
            title = info.get('title', 'Unknown Title')
            thumbnail = info.get('thumbnail', '')

        # เพิ่มเพลงลงในคิว
        await self.add_to_queue(ctx, url, title, thumbnail)

        # เล่นเพลงใน voice channel
        if not voice_client.is_playing():
            await self.play_next(ctx)

    async def announce_next_song(self, ctx, title, thumbnail):
        # เพิ่มรูปภาพของผู้ขอเพลงใน Embed
        requester_avatar_url = ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty
        embed = discord.Embed(
            title="กำลังเล่นเพลง",
            description=f"[{title}]",
            color=discord.Color.orange()
        )
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=f"Requested by : {ctx.author.display_name}", icon_url=requester_avatar_url)

        # ประกาศข้อมูลเพลงต่อไปใน embed
        if len(self.queue) > 0:
            next_song = self.queue[0]['title']  # เลือกชื่อเพลงจากข้อมูลในคิว
            embed.add_field(name="เพลงต่อไป", value=next_song, inline=False)
        else:
            embed.add_field(name="เพลงต่อไป", value="ยังไม่มีเพลงในคิว", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            self.is_looping = False
            #await ctx.send("เพลงถูกหยุดแล้ว!")

    @commands.command()
    async def skip(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            #await ctx.send("เพลงถัดไป!")

    @commands.command()
    async def pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            self.is_paused = True
            await ctx.send("เพลงหยุดชั่วคราวแล้ว!")

    @commands.command()
    async def resume(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and self.is_paused:
            voice_client.resume()
            self.is_paused = False
            await ctx.send("ฟังต่อได้แล้ว!")
        elif not voice_client:
            await ctx.send("ไม่มีเพลงที่ถูกหยุดชั่วคราวในขณะนี้")
        else:
            await ctx.send("ไม่มีเพลงที่ถูกหยุดชั่วคราว")

    @commands.command()
    async def loop(self, ctx):
        self.is_looping = not self.is_looping
        await ctx.send(f"Loop : {'ON' if self.is_looping else 'OFF'}")

    @commands.command()
    async def queue(self, ctx):
        if len(self.queue) > 0:
            queue_list = "\n".join(f"{idx + 1}. {song['title']}" for idx, song in enumerate(self.queue))
            await ctx.send(f"เพลงในคิว:\n{queue_list}")
        else:
            await ctx.send("คิวว่างเปล่า")

    async def add_to_queue(self, ctx, url, title, thumbnail):
        self.queue.append({'url': url, 'title': title, 'thumbnail': thumbnail})

    async def play_next(self, ctx):
        if self.queue:
            song = self.queue.pop(0)
            url = song['url']
            title = song['title']
            thumbnail = song['thumbnail']

            voice_client = ctx.guild.voice_client
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
            voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options), after=lambda e: self.client.loop.create_task(self.play_next(ctx)))

            await self.announce_next_song(ctx, title, thumbnail)
        else:
            voice_client = ctx.guild.voice_client
            await voice_client.disconnect()

async def setup(client):
    await client.add_cog(Music(client))