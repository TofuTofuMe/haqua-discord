# Haqua's Weather Function

from bs4 import BeautifulSoup
from discord.ext import commands
from datetime import datetime, timedelta
from pyowm.owm import OWM
from os import environ
import aiohttp
import discord
import io

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
        utc_time = datetime.utcfromtimestamp(weather.reference_time()).strftime('%H:%M:%S')
        local_time = datetime.fromtimestamp(weather.reference_time()).strftime('%H:%M:%S')
        sunrise_time = datetime.utcfromtimestamp(weather.sunrise_time()).strftime('%H:%M:%S')
        sunset_time = datetime.utcfromtimestamp(weather.sunset_time()).strftime('%H:%M:%S')
        wind = weather.wind()
        dict_celsius = weather.temperature('celsius')
        dict_kelvin = weather.temperature('kelvin')
        humidity = weather.humidity
        celsius_temp = f"{dict_celsius['temp_min']}\xb0C - {dict_celsius['temp_max']}\xb0C"
        kelvin_temp = f"{dict_kelvin['temp_min']} K - {dict_kelvin['temp_max']} K"
        embed = discord.Embed(title=f"Weather at {location}", color=0x00ff80b)
        embed.add_field(name=":clock6: UTC Time", value=f"{utc_time}", inline=True)
        embed.add_field(name=":clock2: Local Time", value=f"{local_time}", inline=True)
        embed.add_field(name=":cloud: Condition", value=f"{weather.status}", inline=True)
        embed.add_field(name=":sweat: Humidity", value=f"{humidity}%")
        embed.add_field(name=":dash: Wind", value=f"{wind['speed']} m/s")
        embed.add_field(name=":thermometer: Temperature", value=f"{dict_celsius['temp']}\xb0C / {dict_kelvin['temp']} K")
        embed.add_field(name=":high_brightness: Min/Max", value=f"{celsius_temp}\n{kelvin_temp}")
        embed.add_field(name=":sunrise: Sunrise", value=f"{sunrise_time}")
        embed.add_field(name=":city_sunset: Sunset", value=f"{sunset_time}")
        embed.set_footer(text="OpenWeatherMap")
        await ctx.send(embed=embed)

    @commands.command()
    async def himawari8(self, ctx, region=None, time=None, band=None):

        if None in {region, time, band}:
            # await ctx.send("Himawari-8 Usage:\n`.himawari8 [region] [HHmm] [B13/B03/SND]`")
            time = datetime.utcnow()
            file_time = (time - timedelta(minutes=30)).strftime('%H%M')
            region = 'se2'
            band = 'snd'
        if time == '0000':
            file_time = '2350'
        else:
            if type(time) is datetime:
                pass
            else:
                file_time = int(time) - 10
                if file_time == 0:
                    file_time = '0000'
            if len(str(file_time)) <= 4:
                file_time = str(file_time).zfill(4)
            if int(file_time[3]) > 0:
                file_time = file_time[:3] + '0'
            if int(file_time[2]) > 5:
                file_time = file_time[:2] + '50'
            
        file_url = f'https://www.data.jma.go.jp/mscweb/data/himawari/img/{region}/{region}_{band}_{file_time}.jpg'
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as resp:
                file_size = resp.headers['content-length']
                message = await ctx.send(f"Downloading data... [Bytes: {file_size}]")
                satellite_img = await resp.read()
                open('cache/himawari8.png', 'wb').write(satellite_img)

        file = discord.File('cache/himawari8.png')
        embed = discord.Embed(title="Himawari-8 Satellite Data", url=file_url, color=0x0080ff)
        embed.set_image(url='attachment://himawari8.png')
        # embed.add_field(name="Region", value=region)
        # embed.add_field(name="Band", value=band)
        # embed.add_field(name="Time", value=time)
        embed.set_footer(text="MSC-JMA")
        await ctx.send(content=None, embed=embed, file=file)
        await message.delete()
        
    @commands.command()
    async def pagasagif(self, ctx, last_hour=False):

        if last_hour == True:
            file_url = 'https://src.meteopilipinas.gov.ph/repo/mtsat-colored/24hour/latest-him-colored-hourly.gif'
        else:
            file_url = 'https://src.meteopilipinas.gov.ph/repo/mtsat-colored/24hour/latest-him-colored.gif'
        
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url, ssl=False) as resp:
                file_size = resp.headers['content-length']
                date_modified = resp.headers['last-modified']
                message = await ctx.send(f"Downloading data... [Bytes: {file_size}]")
                satellite_img = await resp.read()
                open('cache/himawari8.gif', 'wb').write(satellite_img)
        
        file = discord.File('cache/himawari8.gif')
        embed = discord.Embed(title="Himawari-8 Animated Satellite Data", url=file_url, color=0x0080ff)
        embed.set_image(url='attachment://himawari8.gif')
        embed.add_field(name="Last Hour", value=last_hour)
        embed.add_field(name="Animation Date", value=date_modified)
        embed.set_footer(text="DOST-PAGASA & MSC-JMA")
        await ctx.send(content=None, embed=embed, file=file)
        await message.delete()
        
def setup(bot):
    bot.add_cog(Weather(bot))
