import discord
from discord.ext import commands
from Othello import *

app = commands.Bot(command_prefix='o!')


@app.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(app.user.name)
    print('connection was succesful')
    await app.change_presence(status=discord.Status.online, activity=None)


@app.command()
async def hello(ctx):
    await ctx.send('Hello, World!')


@app.command()
async def 임베드(ctx):
    _embed = discord.Embed(
        title='This is Embed',
        description='This is description of Embed',
        color=0x00ff00)
    _embed.add_field(
        name='This is feild 1',
        value='This is Value of Field 1',
        inline=True)
    await ctx.send(embed=_embed)


@app.command()
async def 게임시작(ctx, player1, player2):
    game = OthelloGame(player1, player2)
    print(game.printBoard(),)
    _embed = discord.Embed(
        title=f'5Mok',
        description=game.printBoard(),
        color=0x00ff00)
    await ctx.send(f"{player1} vs {player2}\n",embed=_embed)




app.run('ODg1MzYzNTUyNTk1MDg3NDEz.YTl9EA.3BIKD5J7cCjapiIcQb_hYJL8Ko8')
