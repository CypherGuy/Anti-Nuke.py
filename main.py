import datetime
start_time = datetime.datetime.utcnow()
import discord
import os
import os.path
import json
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

def get_prefix(client, ctx):
    with open ('prefixes.json', 'r') as f:
        prefixes = json.load(f)


    return prefixes[str(ctx.guild.id)]

client = commands.Bot(command_prefix= get_prefix, intents = intents)

@client.event
async def on_guild_join(guild):
    with open ('prefixes.json', 'r') as f:
        prefixes = json.load(f)


    prefixes[str(guild.id)] = '$'

    with open ('prefixes.json', 'w') as f: 
        json.dump(prefixes , f, indent=4)

@client.event
async def on_guild_remove(guild):
     with open ('prefixes.json', 'r') as f:
        prefixes = json.load(f)


     prefixes.pop(str(guild.id))

     with open ('prefixes.json', 'w') as f: 
         json.dump(prefixes , f, indent=4)

@client.event
async def on_ready():
    print(f"{client.user.name} Is Ready!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Ready, made by Cypher_Guy#7831"))

@client.command()
async def whitelisters(ctx):

  embed = discord.Embed(title=f"Whitelist for {ctx.guild.name}", description="")

  with open ('whitelisted.json', 'r') as i:
        whitelisted = json.load(i)

  for i in whitelisted:
    embed.description += f"<@{(i)}> - {i}\n"

  await ctx.send(embed = embed)

@client.command(aliases = ['wl'], hidden=True)
async def whitelist(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("You must specify a user to whitelist.")
    with open ('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)


    whitelisted[str(user.id)] = {}


    with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
    await ctx.send(f"{user.mention} was successfully whitelisted.")

@client.command(aliases = ['uwl'], hidden=True)
@commands.check(is_server_owner)
async def unwhitelist(ctx, user: discord.User = None):
    if user is None:
        await ctx.send("You must specify a user to unwhitelist.")
    with open ('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)
    try:
      del whitelisted[f"{user.id}"]


      with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
      await ctx.send(f"{user.mention} was successfully unwhitelisted.")
    except KeyError:
      await ctx.send("This user was never whitelisted.")

@client.command()
async def info(ctx):
    await ctx.send(embed=discord.Embed(title="robbery info", description=f"{len(client.guilds)} servers, {len(client.users)} users | Database is connected."))

client.run(YOUR_TOKEN)
