
import discord
from discord.ext import commands
import random
from random import randint
import os
import asyncio
import imageslist
import json

client = commands.Bot(command_prefix = 'yuki ')
os.chdir(r'C:\Users\Naiman\Documents\Développement\Python\YukiPython\Yuki')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('I refuse.'))
    print('Le Bot est prêt')

@client.event
async def on_member_join(member):
    # Design
    welcome_channel = client.get_channel(572840726132686891)
    await welcome_channel.send(f'Bienvenue **{member}** dans **La Mafia Portuaire** !')
    await welcome_channel.send(file=discord.File('nya.gif'))
    print(f'{member} a rejoint le serveur.')

    # Database
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    # Code
    await update_data(users, member)

    with open(r'users.json', 'w') as f:
        json.dump(users, f)

@client.event
async def on_message(message):
     # Database
    with open('users.json', 'r') as f:
        users = json.load(f)

        if message.author.bot:
            return
        else:
            await update_data(users, message.author)
            await add_experience(users, message.author, 5)
            await level_up(users, message.author, message.channel)
    
    
    with open('users.json', 'w') as f:
        json.dump(users, f)
        
async def update_data(users, user):
    if not user.id in users:
        users[str(user.id)] = {}
        users[str(user.id)][user.name] = {}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['level'] = 1

async def add_experience(users, user, exp):
    users[str(user.id)]['experience'] += exp

async def level_up(users, user, channel):
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await client.send_message(channel, f'{user.mention} est monté au niveau {lvl_end}')
        user[str(user.id)]['level'] = lvl_end


@client.event
async def on_member_remove(member):
    welcome_channel = client.get_channel(572840726132686891)
    await welcome_channel.send(f'**{member}** a quitté l\'aventure :crab:')
    await welcome_channel.send(file=discord.File('goodbye.gif'))
    print(f'{member} a quitté le serveur.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['Sûrement !',
                'Sans aucun doute',
                'Probablement',
                'Oui.',
                'I refuse.',
                'Repose ta question plus tard !']
                
    await ctx.send(f'Question: {question}\nRéponse: {random.choice(responses)}')


@client.command()
async def clear(ctx, default_amount=5):
    await ctx.channel.purge(limit=default_amount+1)
    message = await ctx.send(f'**Yuki** a supprimé **{default_amount-1}** messages !')
    await asyncio.sleep(4)
    await message.delete()

@client.command()
async def say(ctx, *, args):
    await ctx.send(f'{args}')

@client.command()
async def hug(ctx, member : discord.User = None):


    #EMBEDS

    images_list = imageslist.get_images_list()

    hug_count = 0
    message_author = ctx.message.author.display_name

    if member:    
        embed = discord.Embed(
        title = None,
        description = f'{message_author} fait un calin à {member}',
        colour = discord.Colour.blue()
        )

        embed.set_footer(text=f'C\'est le {hug_count+1}er calin que Yuki donne !')
        embed.set_image(url= random.choice(images_list))

        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
        title = None,
        description = f'{message_author} se fait un calin',
        colour = discord.Colour.blue()
        )

        embed.set_footer(text=f'C\'est le {hug_count+1}er calin que Yuki donne !')
        embed.set_image(url= random.choice(images_list))

        await ctx.send(embed=embed)

@client.command()
async def roulette(ctx, *, args):

    server_members_list = ctx.message.guild.members
    await ctx.send(f'Le gagnant du **{args}** est : {server_members_list[randint(0, len(server_members_list)-1)].name}')

@client.command()
async def addhuggif(ctx, gif = None):

    if gif:
        imageslist.append(gif)
        await ctx.send('Le gif a bien été ajouté à la liste !')
    else:
        await ctx.send('S\'il te plaît, renseigne un gif **valide** !')

@client.command()
async def removehuggif(ctx, gif = None):

    yuki_channel = client.get_channel('634328175991586816')

    if gif:
        if not gif in imageslist.get_images_list:
            await ctx.send('Le GIF n\'est pas dans la liste !')
        else:
            imageslist.remove(gif)
            await ctx.send('Le gif a bien été retiré de la liste !')
            await yuki_channel.send(imageslist.get_images_list)
    else:
        await ctx.send('S\'il te plaît, renseigne un gif **valide** !')
    
    


       
        

client.run('NjI2MTcyNDQ3Njc0MzM1Mjky.XaIJNg.So6kioHFPKjOvmuts-ykfccekFk')