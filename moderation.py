import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @app_commands.describe(user="The user to kick.", reason="The reason for kicking.")
    async def kick(self, ctx, user: discord.User, reason: str = "No Reason Given") -> None:
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
    async def ban(self, ctx, user: discord.User, reason: str = "No Reason Given") -> None:
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
    @commands.has_permissions(timeout_members=True)
    @commands.bot_has_permissions(timeout_members=True)
    @app_commands.describe(user="The user to timeout.", reason="The reason for timeout.")
    async def timeout(self, ctx, user: discord.User, reason: str = "No Reason Given") -> None:
        """
        timeout a user from the server

        Parameters:
        ctx: the command context
        user: the user to timeout from the server
        reason: the reason to timeout the user, defaults to "No Reason Given"

        Returns:
        None
        """
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
                await ctx.guild.timeout(user, reason=reason)
                embed = discord.Embed(
                    description=f"**{member}** was timed out by **{ctx.author}**!",
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