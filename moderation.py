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

