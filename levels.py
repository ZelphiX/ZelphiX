import discord
from discord.ext import commands
import os

class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client

        os.chdir(r'C:\Users\Naiman\Documents\Développement\Python\Shina\Shina')

    
    
    
    async def lvl_up(self, user):
        current_xp = user['xp']
        current_lvl = user['lvl']

        if current_xp >= round((4 * (current_lvl ** 3)) / 5):
            await self.client.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id = $2 AND guild_id = $3", current_lvl + 1, user['user_id'], user['guild_id'])   
            return True
        else:
            return False
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.author.bot:
            return

        await self.client.process_commands(message)

        author_id = str(message.author.id)
        author_name = message.author.name
        guild_id = str(message.guild.id)

        user = await self.client.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)


        if not user:
            await self.client.pg_con.execute("INSERT INTO users (user_id, guild_id, lvl, xp) VALUES ($1, $2, 1, 0)", author_id, guild_id)

        user = await self.client.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        await self.client.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + 1, author_id, guild_id)

        if await self.lvl_up(user):
            print(f"GG {message.author} tu es monté au niveau **{user['lvl'] + 1}**")

    @commands.command()
    async def rank(self, ctx, member : discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.client.pg_con.fetch("SELECT * FROM users WHERE user_id = $1, AND guild_id = $2", author_id, guild_id)

        if not user:
            await ctx.send('Cet utilisateur n\'est pas dans la liste !')
        else:
            embed = discord.Embed(
                color=member.color,
                timestamp=ctx.message.author.created_at
                )
            embed.set_author(name=f'Level - {member}', icon_url=self.client.user.avatar_url)

            embed.add_field(name="Level", value=users[0]['level'])
            embed.add_field(name="XP", value=self.users[0]['experience'])

            await ctx.send(embed=embed)
           


def setup(client):
    client.add_cog(Levels(client))


