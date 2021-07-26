import discord
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands
from discord import DMChannel
import os
import asyncio
import datetime
from discord.ext.commands.core import command
from discord.utils import get
import requests
import json
import praw
import random
from discord.activity import Game
intents = discord.Intents.all()
reddit = praw.Reddit(client_id = "DcPay4CDWuJKLQ",
                    client_secret = "Ns7C_Yedfk1Yv7pjbLqmOh51m6gueA",
                    username="kanekikun1234",
                    password = "kaneki1234",
                    user_agent="kaneki1",
                    check_for_async=False)
client = commands.Bot(command_prefix="$",intents=intents)



@client.event
async def on_ready():

   await client.change_presence(status=discord.Status.idle, activity=Game(name="Freaking_Friends!"  ))
#Non-Points functions !
@client.command(name="avatar")
async def avatar(ctx, * , member: discord.Member=None):
    if not member:
        member = ctx.message.author
        authimg = member.avatar_url

    emd = discord.Embed(colour=member.color , timestamp= ctx.message.created_at)
    emd.set_author(name=f"Avatar of {member}")
    emd.set_image(url = member.avatar_url)
    emd.set_footer(text="Hopefully a freaky one !", icon_url="https://cdn.discordapp.com/avatars/857563578252263434/a54307039b0122c355a9dc8ef3c53f2f.png?size=1024")

    msg = await ctx.send(embed=emd)
    await msg.add_reaction('🤟')

@client.command(name='meme')
async def meme(ctx):
    subreddit = reddit.subreddit("memes")
    top = subreddit.top(limit = 100)
    all_subs = []
    for submission in top :
        all_subs.append(submission)
        rand = random.choice(all_subs)
    
    name = rand.title
    url = rand.url

    emd=discord.Embed(title=name,color=0x00ff00)
    emd.set_image(url=url)
    msg = await ctx.send(embed=emd)
    await msg.add_reaction('🤣')

# @client.command(name='prefix')
# async def prefix(context):
#         myembed = discord.Embed(title="Bot Prefixes of Freaking Friends !",description="The listed below are the bot prefixes", color=0x00ff00)
#         myembed.add_field(name='Dank',value="Dank Memer 's prefix is pls.")
#         myembed.add_field(name='Groovy',value="Groovy's prefix is -p . ")
#         myembed.add_field(name='Rythm',value="Rythm's prefix is !p . ")
#         myembed.add_field(name='Rythm 2',value="Rythm 2's prefix is >p ")
#         myembed.add_field(name='Mantaro',value="Mantaro's prefix is ~>")
#         myembed.add_field(name='Marriage-Bot',value="Marriage-Bot prefix is m! ")
#         myembed.add_field(name='PokeTwo',value="PokeTwo prefix is p! ")
#         myembed.add_field(name='Naruto Botto',value="Naruto bot prefix is n")
#         myembed.add_field(name='Carl',value="Carl prefix is *")
#         generalchannel = client.get_channel(843705964112117815)
#         myembed.set_author(name="kira_uchiha",icon_url="https://cdn.discordapp.com/avatars/843389018254344203/a_59ced54d9985383211df4e4afaf7a72f.gif?size=1024")
#         myembed.set_thumbnail(url="https://cdn.discordapp.com/icons/843705964112117810/a_08ed2ea85dfa95332d42bc6089ab2713.gif?size=1024")
#         myembed.set_footer(text="Hope you like our server!",icon_url="https://cdn.discordapp.com/emojis/852919699386007592.gif?v=1")
#         await context.message.channel.send(embed=myembed)
@client.command(name="vote")    
async def vote(ctx):
    emd1 = discord.Embed(title="Vote us !",description="You all know that we are a growing community and need more users to enhance this server . So I request you to vote our server on top.gg. Your vote will decide the future of this server![Vote us!](https://top.gg/servers/843705964112117810/vote)", color=discord.Colour.blurple() ,timestamp= ctx.message.created_at)
    emd1.set_image(url="https://cdn.discordapp.com/attachments/853251869023666236/856436485955911680/vibes.png")
    emd1.set_thumbnail(url=f'{ctx.guild.icon_url}')
    emd1.set_footer(text='Please vote us !',icon_url="https://cdn.discordapp.com/attachments/853251869023666236/856437935859695646/4078-nagatoro-starstruck.png")
    await ctx.send(embed=emd1)

#Points-functions !

@client.event
async def on_member_join(member):
    with open('user.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('user.json', 'w') as f:
        json.dump(users, f, indent=4)

    await update_data(users, member)
@client.event
async def on_message(message):
    if message.author.bot == False :
        with open('user.json', 'r') as f:
            users = json.load(f)
    
        await update_data(users, message.author)
        await add_points(users, message.author, 0.2)
        await got_points(users, message.author, message)

        with open('user.json', 'w') as f :
            json.dump(users, f, indent=4)
        
        await client.process_commands(message)
al= ['BAL','points','p']       
@client.command(name='bal',aliases=al)
async def bal(ctx,*,member:discord.Member=None):
    if not member:
        member = ctx.message.author
        authimg = member.avatar_url
    with open('user.json', 'r') as f:
        users = json.load(f)
        daily= users[f'{member.id}']['dailypoints']
        weekly = users[f'{member.id}']['weeklypoints']
    emd = discord.Embed(colour=member.color , timestamp= ctx.message.created_at)
    emd.set_author(name=f"😽Points of {member}!😽")
    emd.add_field(name='Daily Points:',value=f'**{round(daily)} points!**', inline=True)
    emd.add_field(name='Weekly Points:',value=f'**{round(weekly)} points!**', inline= True)
    emd.set_thumbnail(url = member.avatar_url)
    await ctx.send(embed=emd)

@client.command(name="dclaim")
async def dclaim(ctx,points = None):
    
    if points == None :
        await ctx.send(f'{ctx.message.author.mention}**Please enter the number of points that you want to claim !Example - `$dclaim 20 `')
    with open('user.json', 'r') as f:
        users = json.load(f)
        daily= users[f'{ctx.message.author.id}']['dailypoints']
    points = int(points)    
    if points > daily :
        await ctx.send(f'{ctx.message.author.mention}You do not have enough points to claim the daily reward for {points}!')
    if points < daily :
        rulers = get(ctx.guild.roles, name='👑Freaky_Rulers👑')
        generals = get(ctx.guild.roles, name='🧙‍♀️Freaky_General🧙‍♂️')
        modchannel = client.get_channel(866250468304093194)
        await modchannel.send(f'{rulers.mention}{generals.mention}{ctx.message.author} wants to claim a daily reward of {points} points.{ctx.message.author} has {round(daily)} daily points !Their id is {ctx.message.author.id}.')
        await ctx.send(f'{ctx.message.author.mention} your claim request has been sent! You will be contacted soon!')
@client.command(name="wclaim")
async def wclaim(ctx,points = None):
    if points == None :
        await ctx.send(f'{ctx.message.author.mention}**Please enter the number of points that you want to claim !Example - `$wclaim 40`')
    with open('user.json', 'r') as f:
        users = json.load(f)
        weekly= users[f'{ctx.message.author.id}']['weeklypoints']
    points = int(points)   
    if points > weekly :
        await ctx.send(f'{ctx.message.author.mention}You do not have enough points to claim the weekly reward for {points}!')
    if points < weekly :
       rulers = get(ctx.guild.roles, name='👑Freaky_Rulers👑')
       generals = get(ctx.guild.roles, name='🧙‍♀️Freaky_General🧙‍♂️')
       modchannel = client.get_channel(853251869023666236) 
       await modchannel.send(f'{rulers.mention}{generals.mention}{ctx.message.author} wants to claim a weekly reward of {points} points.{ctx.message.author} has {round(weekly)} weekly  points !. Their id is {ctx.message.author.id}.')
       await ctx.send(f'{ctx.message.author.mention} your claim request has been sent! You will be contacted soon!')
@client.command(name="deduct",)  
async def deduct(ctx,points,type:str = None,member : discord.Member = None) :
      
       
      if ctx.author.guild_permissions.administrator :
          points1 = int(points)
          with open('user.json', 'r') as f:
            users = json.load(f)
            daily = users[f'{member.id}']['dailypoints'] 
            weekly = users[f'{member.id}']['weeklypoints'] 
            dailycut = daily - points1
            weeklycut = weekly - points1
            if type == 'daily':
                users[f'{member.id}']['dailypoints'] = dailycut
            elif type == 'weekly':
                users[f'{member.id}']['weeklypoints'] = weeklycut
            with open('user.json', 'w') as f :
                json.dump(users, f, indent=4)
      await ctx.send(f'Deducted {points1} points from {member.mention}!')

@client.command(name="gift")
async def gift(ctx,points:int = None,type1:str = None, member: discord.Member = None):
    if points == None:
        await ctx.send(f'{ctx.author.mention} ***also enter the points. Example -*** `$gift 20  daily/weekly @mentionuser`')
    elif member == None :
        await ctx.send(f'{ctx.author.mention} ***also mention the user. Example -*** `$gift 20 daily/weekly @mentionuser`')
    elif type1 == None:
        await ctx.send(f'{ctx.author.mention} also enter the type , .i.e. daily or weekly Example - `$gift 20 daily/weekly @mentionuser`')
    with open('user.json', 'r') as f:
            users = json.load(f)
            daily = users[f'{ctx.message.author.id}']['dailypoints'] 
            weekly = users[f'{ctx.message.author.id}']['weeklypoints'] 
    if type1 == 'weekly': 
        if points > weekly:
            await ctx.send(f'{ctx.author.mention} **You dont have enough weekly points to give to {member.mention}!Chat some more and gain points !**')
        if weekly > points:
            dailycut = round(daily) - points
            weeklycut = round(weekly) - points
            
            
            users[f'{ctx.message.author.id}']['weeklypoints'] -= points
            
            users[f'{member.id}']['weeklypoints'] += points
            with open('user.json', 'w') as f :
                json.dump(users, f, indent=4)
            await ctx.send(f'🥳{ctx.message.author.mention} has gifted you  {points} weekly points! {member.mention}!🥳')
    elif type1 == 'daily':
        if points > daily:
            await ctx.send(f'{ctx.author.mention} You dont have enough daily  points to give to {member.mention}!Chat some more and gain points !')
        if daily > points:
            dailycut = round(daily) - points
            weeklycut = round(weekly) - points
            
            
            users[f'{ctx.message.author.id}']['weeklypoints'] -= points
            users[f'{ctx.message.author.id}']['dailypoints'] -= points
            users[f'{member.id}']['weeklypoints'] += points
            users[f'{member.id}']['dailypoints'] += points
            with open('user.json', 'w') as f :
                json.dump(users, f, indent=4)
            await ctx.send(f'🥳{ctx.message.author.mention} has gifted you {points} daily points! {member.mention}!🥳')

@client.command(name="gstart")
@commands.has_role('🎉Giveaway Team🎉')
async def gstart(ctx,min:int = None,winn:int=None,img1:str = None,*,prize:str = None):
    if min == None:
        await ctx.send(f'{ctx.message.author.mention} ***enter the giveaway time!***')
    elif prize == None:
        await ctx.send(f'{ctx.message.author.mention} ***enter you giveaway item dude!***')
    elif winn == None:
        await ctx.send(f'{ctx.message.author.mention} ***enter the number of winners!***')
    emd = discord.Embed(title=f"{prize}!🎉",description=f"***Giveaway by*** {ctx.message.author.mention}",color = discord.Color.blue())
    emd.set_thumbnail(url=ctx.guild.icon_url)
    emd.set_image(url=img1)
    
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = min*60)
    emd.add_field(name="Winners :", value=f"**{winn} Winners!**")
    emd.add_field(name="Ends At:", value=f"{end}** UTC **")
    emd.set_footer(text=f"React Fast!Ends {min} minutes from now!")

    my_msg = await ctx.send(embed=emd)
    await my_msg.add_reaction('🥳')
    await asyncio.sleep(min*60)
    newmsg = await ctx.channel.fetch_message(my_msg.id)
    users = await newmsg.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    ids = [i.id for i in users]
    winners = random.sample(ids,winn)
    for l  in winners:
        usermem = ctx.guild.get_member(l)
        await ctx.send(f'{usermem.mention} you have won {prize}!DM {ctx.message.author.mention}to claim your {prize}🎉')
        await usermem.send(f'🎉You have won the give away of {prize}! Please message {ctx.message.author.name} to claim your Prize!🎉')
        
@client.command(name='greroll')    
async def greroll(ctx,id:int= None):
    if id == None:
        await ctx.send(f'{ctx.message.author.mention} enter the message id too.Example - `$greroll 879789727399837 ')
    elif id!= None:
        try:
            newmsg = await ctx.channel.fetch_message(id)
            users = await newmsg.reactions[0].users().flatten()
            users.pop(users.index(client.user))
            ids = [i.id for i in users]
            winners = random.choice(ids)
            usermem = ctx.guild.get_member(winners)
            await ctx.send(f'The new winner is {usermem.mention}!')
        except:
            await ctx.send(f'{ctx.message.author.mention} Hmmm, it seems that you entered a wrong id. Try doing it correctly again.')
    
@client.command(name="reset")
@commands.has_role('👑Freaky_Rulers👑')
async def reset(ctx,typ:str = None):
    members = ctx.guild.members
    if typ == None:
        await ctx.send(f'{ctx.message.author.mention}mention daily or weekly dude!')
    elif typ == "daily":
        for member in members:
            
            with open('user.json', 'r') as f:
                    users = json.load(f)
            if  f'{member.id}' in users :

                daily = users[f'{member.id}']['dailypoints'] 
                pointsdiff= users[f'{member.id}']['pointsdiff'] 
                users[f'{member.id}']['dailypoints'] -= daily
                users[f'{member.id}']['pointsdiff'] -= pointsdiff
                with open('user.json', 'w') as f :
                    json.dump(users, f, indent=4)
                await ctx.send(f'Reset {typ}points to 0!')
    elif typ == "all":
        for member in members:
            
            with open('user.json', 'r') as f:
                    users = json.load(f)
            if  f'{member.id}' in users :

                daily = users[f'{member.id}']['dailypoints'] 
                weekly = users[f'{member.id}']['weeklypoints'] 
                pointsdiff= users[f'{member.id}']['pointsdiff'] 
                users[f'{member.id}']['dailypoints'] -= daily
                users[f'{member.id}']['pointsdiff'] -= pointsdiff
                users[f'{member.id}']['weeklypoints'] -= weekly
                with open('user.json', 'w') as f :
                    json.dump(users, f, indent=4)
                await ctx.send(f'Reset {typ}points to 0!')
@client.command(name='adminhelp')
async def adminhelp(ctx):
    rulers = get(ctx.guild.roles, name='👑Freaky_Rulers👑')
    await ctx.send(f'{rulers.mention}***Come here guys! Somebody needs your help!***')
@client.command(name='modhelp')
async def modhelp(ctx):
    generals = get(ctx.guild.roles, name='🧙‍♀️Freaky_General🧙‍♂️')
    await ctx.send(f'{generals.mention}***Come here guys! Somebody needs your help!***')
@client.command(name="add")
@commands.has_role('👑Freaky_Rulers👑')
async def reset(ctx,typ:str = None,points:int = None):
    members = ctx.guild.members
    if typ == None:
        await ctx.send(f'{ctx.message.author.mention}mention daily or weekly dude!')
    elif typ == "daily":
        for member in members:
            
            with open('user.json', 'r') as f:
                    users = json.load(f)
            if  f'{member.id}' in users :

                daily = users[f'{member.id}']['dailypoints'] 
                pointsdiff= users[f'{member.id}']['pointsdiff'] 
                weekly = users[f'{member.id}']['weeklypoints'] 
                users[f'{member.id}']['dailypoints'] +=points
                users[f'{member.id}']['pointsdiff'] += points
                users[f'{member.id}']['weeklypoints'] += points
                with open('user.json', 'w') as f :
                    json.dump(users, f, indent=4)
                await ctx.send(f' Add {points} {typ}points to everyone who have participated so far!')
    elif typ == 'weekly':
        for member in members:
            
            with open('user.json', 'r') as f:
                    users = json.load(f)
            if  f'{member.id}' in users :

                 
                
                users[f'{member.id}']['weeklypoints'] += points
                with open('user.json', 'w') as f :
                    json.dump(users, f, indent=4)
                await ctx.send(f' Add {points} {typ}points to everyone who have participated so far!')            
@client.command(name='addanime')
@commands.has_role('OG')
async def addsm(ctx,link:str = None,*,anime:str = None):
    if anime == None:
        await ctx.send(f'{ctx.message.author.mention} also enter the anime name . Example -`$addanime https://animixplay.to/ tokyo revengers` ')
    elif link == None:
        await ctx.send(f'{ctx.message.author.mention}also add your link. Example- `$addanime  https://animixplay.to/ attack on titan`')
    if anime!=None and link!=None:
        with open('anime.json', 'r') as f:
            typusu = json.load(f)
        if anime in typusu:
            await ctx.send(f'{ctx.message.author.mention}{anime} has already been added!')
        else:
            typusu[f'{anime}'] = f'{link}'  
            with open('anime.json','w') as f:
                json.dump(typusu,f,indent=4) 
            await ctx.send(f'{ctx.message.author.mention}Thanks for adding {anime} link !')   
@client.command(name='getanime')
async def getanime(ctx,*,anime:str = None):
    if anime == None:
        await ctx.send(f'{ctx.message.author.mention}enter the anime dumbass!😆')
    elif anime != None:
        with open('anime.json', 'r') as f:
            typusu = json.load(f)
        anilink = typusu[f'{anime}']
        await ctx.send(f'{ctx.message.author.mention} **Here you go! The link of {anime} ! **')
        await ctx.send(f'{anilink}')
@client.command(name='moviestream')
@commands.has_role('👑Freaky_Rulers👑')
async def moviestream(ctx,img:str = None,streamlink:str = None,*,moviename:str = None):
    emd = discord.Embed(title=f'🎥{moviename} is being streamed!🎥', description=f'[Click me!]({streamlink})**to join the stream!**',color= discord.Colour.dark_gold())
    emd.set_image(url=f'{img}')
    emd.set_thumbnail(url=f'{ctx.guild.icon_url}')
    emd.set_author(name=f'{ctx.message.author.name}',icon_url=ctx.message.author.avatar_url)
    emd.set_footer(text=f'Stream by {ctx.message.author.name}',icon_url= 'https://cdn.discordapp.com/emojis/852578319027142656.png')
    chating_arena = client.get_channel(853251869023666236)
    ti = 0
    while ti<4:
        await ctx.send(embed=emd)
        await chating_arena.send(embed=emd)
        await asyncio.sleep(10*60)
@client.command(name='servericon') 
async def servericon(ctx):
    emd = discord.Embed(title=f'Icon of {ctx.guild.name}!',color=discord.Colour.purple())          
    emd.set_image(url=f'{ctx.guild.icon_url}')
    emd.set_footer(text='Hows it!',icon_url='https://cdn.discordapp.com/emojis/852578319027142656.png')
    my_msg = await ctx.send(embed=emd)
    await my_msg.add_reaction('🤟')






    
#Helper functions !
async def update_data(users, user):
    if not f'{user.id}' in users :
        users[f'{user.id}'] = {}
        
        users[f'{user.id}']['dailypoints'] = 0
        users[f'{user.id}']['weeklypoints'] = 0
        users[f'{user.id}']['pointsdiff'] = 0

async def add_points(users, user, points):
    users[f'{user.id}']['dailypoints'] +=points
    users[f'{user.id}']['weeklypoints'] +=points

async def got_points(users,user, message):
    daily= users[f'{user.id}']['dailypoints']
    diff = users[f'{user.id}']['pointsdiff']
    if daily - diff >20 and daily - diff < 20.4:
        emd = discord.Embed(title=f"Congrats! ",description=f" {user.mention}***🧚‍♂️You got 20 Points !***🧚‍♂️",color =0x00ff00)
        emd.set_thumbnail(url=user.avatar_url)
        dif = daily - diff
        users[f'{user.id}']['pointsdiff'] += dif
        await message.channel.send(embed= emd)
        






client.run('ODU3NTYzNTc4MjUyMjYzNDM0.YNRaUQ.nZAFUaY5ISPnc-nnl6Js4LgBDkc')