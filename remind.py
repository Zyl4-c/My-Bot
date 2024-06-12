import discord
from discord.ext import commands, tasks
from datetime import datetime, time, timedelta

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1247533496952688700  # ใส่ ID ของช่องที่ต้องการส่งข้อความ
        self.reminder_loop.start()

    def cog_unload(self):
        self.reminder_loop.cancel()

    @tasks.loop(minutes=1)
    async def reminder_loop(self):
        now = datetime.now()
        current_time = now.time()
        today = now.weekday()  # Monday is 0 and Sunday is 6

        # ตรวจสอบเวลาปัจจุบันและส่งข้อความตามวันและเวลา
        if current_time == time(19, 55):  # ส่งข้อความเวลา 19:30 PM
            channel = self.bot.get_channel(self.channel_id)
            if today == 0:  # จ
                await channel.send(
                    "วันจันทร์\n"
                    "ท่าเล่นอก:\n"
                    "1. Push Up 5 Sets x ฝึกจนหมดแรง\n"
                    "2. Dumbbell Fly 3 Sets x ฝึกจนหมดแรง"
                )
            elif today == 1:  # อ
                await channel.send(
                    "วันอังคาร\n"
                    "ท่าเล่นแขน:\n"
                    "1. Bicep Curl 3 Sets x ฝึกจนหมดแรง\n"
                    "2. Hammer Curl 3 Sets x ฝึกจนหมดแรง\n"
                    "3. Tricep Extension 3 Sets x ฝึกจนหมดแรง\n"
                    "4. Kick Back 3 Sets x ฝึกจนหมดแรง"
                )
            elif today == 2:  # พ
                await channel.send(
                    "วันพุธ\n"
                    "ท่าเล่นขา:\n"
                    "1. Squat Jump 5 Sets x ฝึกจนหมดแรง\n"
                    "2. Lunge Jump 5 Sets x ฝึกจนหมดแรง\n"
                    "3. Stiff Leg Deadlift 5 Sets x ฝึกจนหมดแรง"
                )
            elif today == 3:  # พฤ
                await channel.send(
                    "วันพฤหัสบดี\n"
                    "ท่าเล่นไหล่:\n"
                    "1. Dumbbell Row 5 Sets x ฝึกจนหมดแรง\n"
                    "2. Dumbbell Shrug 3 Sets x ฝึกจนหมดแรง\n"
                    "3. Dumbbell Deadlift 3 Sets x ฝึกจนหมดแรง"
                )
            elif today == 4:  # ศ
                await channel.send(
                    "วันศุกร์\n"
                    "พักได้แล้ว:\n"
                )
            elif today == 5:  # ส
                await channel.send(
                    "วันเสาร์\n"
                    "ท่าเล่นไหล่:\n"
                    "1. Dumbbell Shoulder Press 5 Sets x ฝึกจนหมดแรง\n"
                    "2. Front Raise 3 Sets x ฝึกจนหมดแรง\n"
                    "3. Lateral Raise 3 Sets x ฝึกจนหมดแรง\n"
                    "4. Reverse Fly 3 Sets x ฝึกจนหมดแรง"
                )
            elif today == 6:  # อา
                await channel.send(
                    "วันอาทิตย์\n"
                    "วันนี้ว่างอยากทำอะไรทำได้เลย!!"
                )

    @reminder_loop.before_loop
    async def before_reminder_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Reminder(bot))