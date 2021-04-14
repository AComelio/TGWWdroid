import discord
from discord.ext import commands
import os
import logging
import random

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

@bot.group()
async def roles(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid flag {0.subcommand_passed}, valid flags are "grant" and "remove"'.format(ctx))

@roles.command(name='grant')
async def _grant_role(ctx, role:discord.Role):
    "Grants the requested role to the member"
    await ctx.author.add_roles(role)
    await ctx.send('Role added.')

@_grant_role.error
async def gr_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Role does not exist.')

@roles.command(name='remove')
async def _remove_role(ctx, role: discord.Role):
    "Removes the requested role from the member"
    await ctx.author.remove_roles(role)
    await ctx.send('Role removed')

@_remove_role.error
async def rr_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Role does not exist.')

@bot.command()
async def list_roles(ctx):
    "Lists all roles in the server"
    ret_str = 'This server contains the following roles:\n'
    for r in ctx.guild.roles:
        ret_str += r.name
        ret_str += '\n'
    await ctx.send(ret_str)

def main(token):
    bot.run(token)

if __name__ == '__main__':
    main(os.getenv('TOKEN'))
