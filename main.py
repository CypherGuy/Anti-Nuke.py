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


def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id

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

@client.command(aliases = ['wld'], hidden=True)
async def whitelisters(ctx):

  embed = discord.Embed(title=f"Whitelist for {ctx.guild.name}", description="")

  with open ('whitelisted.json', 'r') as i:
        whitelisted = json.load(i)
  try:
    for u in whitelisted[str(ctx.guild.id)]:
      embed.description += f"<@{(u)}> - {u}\n"
    await ctx.send(embed = embed)
  except KeyError:
    await ctx.send("Nothing found for this guild!")


@client.command(aliases = ['wl'], hidden=True)
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
async def unwhitelist(ctx, user: discord.User = None):
  if user is None:
      await ctx.send("You must specify a user to unwhitelist.")
      return
  with open ('whitelisted.json', 'r') as f:
      whitelisted = json.load(f)
  try:
    if str(user.id) in whitelisted[str(ctx.guild.id)]:
      del whitelisted[f"{str(ctx.guild.id)}"][0] #This removes the first item in the guild, please suggest a way to fix this.
      
      with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
      await ctx.send(f"{user.mention} was successfully unwhitelisted.")
  except KeyError:
    await ctx.send("This user was never whitelisted, or an error has occured.")

client.run(TOKEN)
