import discord
from discord.ext import commands
import requests
import json

class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client
        # Load the API key from config.json
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.api_key = config.get('weather_api_key')

    @commands.command()
    async def weather(self, ctx, *, city: str):
        if not self.api_key:
            await ctx.send("API key is not set in config.json")
            return

        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + self.api_key + "&q=" + city + ",TH&units=metric"
        
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404" and "main" in data:
            main = data["main"]
            wind = data["wind"]
            weather_desc = data["weather"][0]["description"]

            temp = main["temp"]
            feels_like = main["feels_like"]
            temp_min = main["temp_min"]
            temp_max = main["temp_max"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            wind_speed = wind["speed"]

            weather_embed = discord.Embed(
                title=f"Weather in {city}, Thailand",
                color=discord.Color.blue()
            )
            weather_embed.add_field(name="Description", value=weather_desc.capitalize(), inline=False)
            weather_embed.add_field(name="Temperature", value=f"{temp}°C (feels like {feels_like}°C)", inline=False)
            weather_embed.add_field(name="Min/Max Temperature", value=f"Min: {temp_min}°C / Max: {temp_max}°C", inline=False)
            weather_embed.add_field(name="Pressure", value=f"{pressure} hPa", inline=False)
            weather_embed.add_field(name="Humidity", value=f"{humidity}%", inline=False)
            weather_embed.add_field(name="Wind Speed", value=f"{wind_speed} m/s", inline=False)

            await ctx.send(embed=weather_embed)
        else:
            await ctx.send("City not found in Thailand. Please check the city name and try again.")

async def setup(client):
    await client.add_cog(Weather(client))