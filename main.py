import keep_alive
keep_alive.keep_alive()
import datetime
start_time = datetime.datetime.utcnow()
import discord
import os
import asyncio
import os.path
import json
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
from dotenv import load_dotenv
load_dotenv()

from cogs.AntiChannel import AntiChannel
from cogs.AntiRemoval import AntiRemoval
from cogs.AntiRole import AntiRole
from cogs.Diagnostics import Diagnostics

def is_allowed(ctx):
    return ctx.message.author.id == 682319844368056331

def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 682319844368056331

def get_prefix(client, ctx):
    with open ('prefixes.json', 'r') as f:
        prefixes = json.load(f)


    return prefixes[str(ctx.guild.id)]

client = commands.Bot(command_prefix= get_prefix, intents = intents)

client.remove_command("help")

client.add_cog(AntiChannel(client))
client.add_cog(AntiRemoval(client))
client.add_cog(AntiRole(client))
client.add_cog(Diagnostics(client))

@client.event
async def on_guild_join(guild):
    with open ('prefixes.json', 'r') as f:
        prefixes = json.load(f)


    prefixes[str(guild.id)] = '>'
    
    with open ('prefixes.json', 'w') as f: 
        json.dump(prefixes , f, indent=4)

@client.event
async def on_guild_remove(guild):
     with open ('prefixes.json', 'r') as f:
        prefixes = json.load(f)


     prefixes.pop(str(guild.id))

     with open ('prefixes.json', 'w') as f: 
         json.dump(prefixes , f, indent=4)

@client.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        
    prefixes[str(ctx.guild.id)] = prefix
    
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
        
    await ctx.send(f'Guild Prefix Changed To: ***{prefix}***')

@client.command(aliases = ['wld'], hidden=True)
@commands.has_permissions(administrator=True)
async def whitelisted(ctx):

  embed = discord.Embed(title=f"Whitelisted users for {ctx.guild.name}", description="")

  with open ('whitelisted.json', 'r') as i:
        whitelisted = json.load(i)
  try:
    for u in whitelisted[str(ctx.guild.id)]:
      embed.description += f"<@{(u)}> - {u}\n"
    await ctx.send(embed = embed)
  except KeyError:
    await ctx.send("Nothing found for this guild!")

@client.command(aliases = ['wl'], hidden=True)
@commands.check(is_server_owner)
async def whitelist(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("You must specify a user to whitelist.")
        return
    with open ('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)


    if str(ctx.guild.id) not in whitelisted:
      whitelisted[str(ctx.guild.id)] = []
    else:
      if str(user.id) not in whitelisted[str(ctx.guild.id)]:
        whitelisted[str(ctx.guild.id)].append(str(user.id))
      else:
        await ctx.send("User is already whitelisted")
        return



    with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
    await ctx.send(f"{user.mention} was successfully whitelisted.")

@client.command(aliases = ['uwl'], hidden=True)
#@commands.check(is_server_owner)
async def unwhitelist(ctx, user: discord.User = None):
  if user is None:
      await ctx.send("You must specify a user to unwhitelist.")
      return
  with open ('whitelisted.json', 'r') as f:
      whitelisted = json.load(f)
  try:
    if str(user.id) in whitelisted[str(ctx.guild.id)]:
      whitelisted[str(ctx.guild.id)].remove(str(user.id))
      
      with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
      await ctx.send(f"{user.mention} was successfully unwhitelisted.")
  except KeyError:
    await ctx.send("This user was never whitelisted, or an error has occured.")

@client.command()
async def info(ctx):
    await ctx.send(embed=discord.Embed(title="Santana Info", description=f"{len(client.guilds)} servers, {len(client.users)} users | Database is connected"))

@client.command()   
async def help(ctx):
  embed = discord.Embed(description=f"**Categories (7)**")
  embed.add_field(name="``ANTI``", value="``MOD``", inline=False)
  embed.add_field(name="``FUN``", value="``ABOUT``", inline=False)
  embed.add_field(name="``SERVER``", value="``SANTANA``", inline=False)
  embed.add_field(name="``OWNER``", value="``ㅤ``", inline=False)
  embed.add_field(name="``>[category]``", value=f"Made By <@682319844368056331>", inline=False)
  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/774826575521906731/774871425432944650/image0_33.gif')
  embed.set_footer(text='7 Categories | 6 Commands')
  await ctx.send(embed=embed)

@client.event
async def on_ready():
    print("Santana Loaded & Online!")


client.run(TOKEN)
