# Haqua's Weather Function
# written by GrenadeSpamr

from discord.ext import commands
from datetime import datetime
from os import environ
from pyowm.owm import OWM
import discord

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.owm_token = environ.get('owm_token')

    @commands.command()
    async def weather(self, ctx, *, location):
        owm = OWM(self.owm_token)
        weather_manager = owm.weather_manager()
        weather_location = weather_manager.weather_at_place(location)
        weather = weather_location.weather
        utcTime = datetime.utcfromtimestamp(weather.reference_time()).strftime('%H:%M:%S')
        localTime = datetime.fromtimestamp(weather.reference_time()).strftime('%H:%M:%S')
        sunriseTime = datetime.utcfromtimestamp(weather.sunrise_time()).strftime('%H:%M:%S')
        sunsetTime = datetime.utcfromtimestamp(weather.sunset_time()).strftime('%H:%M:%S')
        wind = weather.wind()
        dictCelsius = weather.temperature('celsius')
        dictKelvin = weather.temperature('kelvin')
        humidity = weather.humidity
        celsiusTemp = f"{dictCelsius['temp_min']}\xb0C - {dictCelsius['temp_max']}\xb0C"
        kelvinTemp = f"{dictKelvin['temp_min']} K - {dictKelvin['temp_max']} K"
        embed = discord.Embed(title=f"Weather at {location}", color=0x00ff80b)
        embed.add_field(name=":clock6: UTC Time", value=f"{utcTime}", inline=True)
        embed.add_field(name=":clock2: Local Time", value=f"{localTime}", inline=True)
        embed.add_field(name=":cloud: Condition", value=f"{weather.status}", inline=True)
        embed.add_field(name=":sweat: Humidity", value=f"{humidity}%")
        embed.add_field(name=":dash: Wind", value=f"{wind['speed']} m/s")
        embed.add_field(name=":thermometer: Temperature", value=f"{dictCelsius['temp']}\xb0C / {dictKelvin['temp']} K")
        embed.add_field(name=":high_brightness: Min/Max", value=f"{celsiusTemp}\n{kelvinTemp}")
        embed.add_field(name=":sunrise: Sunrise", value=f"{sunriseTime}")
        embed.add_field(name=":city_sunset: Sunset", value=f"{sunsetTime}")
        embed.set_footer(text="Powered by openweathermap.org")
        await ctx.send(embed=embed)

    @commands.command()
    async def himawari8(self, ctx, region, time, band):
        if None in {region, time, band}:
            await ctx.send("Himawari-8 Usage: `.himawari8 [region] [HH:mm] [B13/B03/SND]`")

#        for entry in {region, time, band}:
#            entry.lower()

        fileUrl = f'https://www.data.jma.go.jp/mscweb/data/himawari/img/{region}/{region}_{band}_{time}.jpg'
        embed = discord.Embed(title=f"Himawari-8 Satellite Data", url=fileUrl, color=0x0080ff)
        embed.set_image(url=fileUrl)
        embed.add_field(name="Region", value=region)
        embed.add_field(name="Band", value=band)
        embed.add_field(name="Time", value=time)
        embed.set_footer(text="Meteorological Satellite Center of JMA")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Weather(bot))
