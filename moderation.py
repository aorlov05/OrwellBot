import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @app_commands.describe(user="The user to kick.", reason="The reason for kicking.")
    async def kick(self, ctx, user: discord.User, *, reason: str = "No Reason Given") -> None:
        """
        Kick a user from the server

        Parameters:
        ctx: the command context
        user: the user to kick from the server
        reason: the reason to kick the user, defaults to "No Reason Given"

        Returns:
        None
        """
        member = ctx.guild.get_member(user.id)
        # Check if the user is an admin
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                description="Cannot kick, User is an administrator.", color=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            # Try kicking user
            try:
                await ctx.guild.kick(user, reason=reason)
                embed = discord.Embed(
                    description=f"**{member}** was kicked by **{ctx.author}**!",
                    color=0x00FF00
                )
                embed.add_field(name="Reason:", value=reason)
                await ctx.send(embed=embed)
                # Try dming user with kick message
                try:
                    await member.send(
                        f"You were kicked by **{ctx.author}** from **{ctx.guild.name}**!\nReason: {reason}"
                    )
                except:
                    # Couldn't DM user
                    pass
            except:
                embed = discord.Embed(
                    description="An error occured trying to kick the user, make sure Orwell has permission to kick this user.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @app_commands.describe(user="The user to ban.", reason="The reason for banning.")
    async def ban(self, ctx, user: discord.User, *, reason: str = "No Reason Given") -> None:
        """
        Ban a user from the server

        Parameters:
        ctx: the command context
        user: the user to ban from the server
        reason: the reason to ban the user, defaults to "No Reason Given"

        Returns:
        None
        """
        member = ctx.guild.get_member(user.id)
        # Check if the user is an admin
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                description="Cannot ban, User is an administrator.", color=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            # Try banning user
            try:
                await ctx.guild.ban(user, reason=reason)
                embed = discord.Embed(
                    description=f"**{member}** was banned by **{ctx.author}**!",
                    color=0x00FF00
                )
                embed.add_field(name="Reason:", value=reason)
                await ctx.send(embed=embed)
                # Try dming user with ban message
                try:
                    await member.send(
                        f"You were banned by **{ctx.author}** from **{ctx.guild.name}**!\nReason: {reason}"
                    )
                except:
                    # Couldn't DM user
                    pass
            except:
                embed = discord.Embed(
                    description="An error occured trying to ban the user, make sure Orwell has permission to ban this user.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @app_commands.describe(user="The user to timeout.", reason="The reason for timeout.")
    async def timeout(self, ctx, user: discord.User, days: int, hours: int, minutes: int, *, reason: str = "No Reason Given") -> None:
        """
        timeout a user from the server

        Parameters:
        ctx: the command context
        user: the user to timeout from the server
        days: days to timeout
        hours: hours to timeout
        minutes: minutes to timeout
        reason: the reason to timeout the user, defaults to "No Reason Given"

        Returns:
        None
        """
        time: timedelta = timedelta(days=days, hours=hours, minutes=minutes)
        member = ctx.guild.get_member(user.id)
        # Check if the user is an admin
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                description="Cannot timeout, User is an administrator.", color=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            # Try timing out user
            try:
                await member.timeout(time, reason=reason)
                embed = discord.Embed(
                    description=f"**{member}** was timed out by **{ctx.author}** for **{days}** days, **{hours}** hours, and **{minutes}** minutes.\nReason: {reason}!",
                    color=0x00FF00
                )
                embed.add_field(name="Reason:", value=reason)
                await ctx.send(embed=embed)
                # Try dming user with timeout message
                try:
                    await member.send(
                        f"You were timed out by **{ctx.author}** from **{ctx.guild.name}**!\nReason: {reason}"
                    )
                except:
                    # Couldn't DM user
                    pass
            except:
                embed = discord.Embed(
                    description="An error occured trying to timeout the user, make sure Orwell has permission to timeout this user.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @app_commands.describe(messageID="The message ID to delete", reason="The reason for delete.")
    async def delete_message(self, ctx, message_id: int, *, reason: str):
        print(message_id)
        try:
            message = await ctx.fetch_message(message_id)
            print(message)
            await message.delete()
            embed = discord.Embed(
                description=f"**{message.author}**'s message **{message_id}** deleted from **{ctx.guild.name}** by **{ctx.author}**!\nReason: {reason}", color=0x00FF00
            )
            await ctx.send(embed=embed)

        except:
            embed = discord.Embed(
                description=f"Failed to delete message **{message_id}** from **{ctx.guild.name}**",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
