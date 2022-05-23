# Haqua's Admin Functions

import discord
import datetime
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.is_owner()
    @commands.has_permissions(manage_messages=True)
    async def announce(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(f"{message}")

    @commands.command(aliases=['del'])
    # @commands.is_owner()
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, *messages):
        for message_id in messages:
            message_id = int(message_id)
            message = await ctx.channel.fetch_message(message_id)
            await message.delete()
        await ctx.message.delete()
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def move(self, ctx, channel_name, *message_id):
        try:
            for id in message_id:
                msg_id = int(id)
                print(message_id)
                message = await ctx.channel.fetch_message(msg_id)
                channel = discord.utils.get(ctx.guild.channels, name=channel_name)
                embed = discord.Embed()
                if message.attachments:
                    message_attachment = message.attachments[0]
                    embed.description = message.content
                    embed.url = message_attachment.url
                    embed.set_image(url=message_attachment.proxy_url)
                    
                if message.embeds:
                    message_embed = message.embeds[0]
                    if message_embed.title:
                        embed.title = message_embed.title
                    embed.description = message.content + '\n' + message_embed.description
                    embed.set_thumbnail(url=message_embed.thumbnail.proxy_url)
                    if message_embed.author:
                        embed.add_field(name='Author', value=message_embed.author.name)
                    if message_embed.fields:
                        for field in message_embed.fields:
                            embed.add_field(name=field.name, value=field.value, inline=field.inline)
                    embed.set_image(url=message_embed.image.proxy_url)
                    embed.url = message_embed.url
                else:
                    embed.description = message.content
                    
                embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                embed.set_footer(text=(message.created_at + datetime.timedelta(hours=8)))
                
                await channel.send(embed=embed)
                await message.delete()
                await ctx.message.delete()
        except Exception as error:
            raise error
            await ctx.send('Invalid input.')
            
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def rolename(self, ctx, role, name):
        try:
            role = discord.utils.get(ctx.author.guild.roles, name=role)
            await role.edit(name=name)
            await ctx.send(f"Changed role name of `{role}` to `{name}`.")
        except Exception as error:
            raise error
            await ctx.send('Error occurred.')
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def rolecolour(self, ctx, role, r, g, b):
        r, g, b = int(r), int(g), int(b)
        try:
            role = discord.utils.get(ctx.author.guild.roles, name=role)
            await role.edit(colour=discord.Colour.from_rgb(r, g, b))
            await ctx.send(f"Changed role colour of `{role}` to `{r, g, b}`.")
        except Exception as error:
            raise error
            await ctx.send('Error occurred.')

def setup(bot):
    bot.add_cog(Admin(bot))
