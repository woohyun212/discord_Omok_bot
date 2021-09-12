import discord
from discord.ext import commands
from Othello import *
from io import BytesIO
from discord.ext.commands import CommandNotFound
import json

app = commands.Bot(command_prefix='o!', help_command=None)


@app.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(app.user.name)
    print('connection was succesful')
    await app.change_presence(status=discord.Status.online, activity=None)


@app.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return await ctx.send("그런 명령어 없습니다~")
    raise error


@app.command()
async def hello(ctx):
    await ctx.send('Hello, World!')


# @app.command()
# async def 임베드(ctx):
#     _embed = discord.Embed(
#         title='This is Embed',
#         description='This is description of Embed',
#         color=0x00ff00)
#     _embed.add_field(
#         name='This is feild 1',
#         value='This is Value of Field 1',
#         inline=True)
#     await ctx.send(embed=_embed)


def sendImage(game):
    with BytesIO() as image_binary:
        game.getImageFromBoard().save(image_binary, 'png')
        image_binary.seek(0)
        return discord.File(fp=image_binary, filename="image.png")


def getDiscordId(name_tag):
    return int(name_tag[3:21])


@app.command(name='start', description='Game start')
async def start(ctx, player2):
    game = OmokGame(ctx.author.id, getDiscordId(player2))
    game.gameSave()
    out = sendImage(game)
    _embed = discord.Embed(
        title=f'{game.color[game.turn]}이 선입니다.',
        color=0xff0000)
    await ctx.send(f"<@!{ctx.author.id}> vs {player2}\n", file=out, embed=_embed)
    return await ctx.send(f"<@!{ctx.author.id}> 가 `{game.color[ctx.author.id]}` 이고,\n"
                          f"{player2} 가 `{game.color[getDiscordId(player2)]}` 입니다.")


al_nu = dict(zip('ABCDEFGHIJKLMNOPQRS', map(int, '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19'.split())))


@app.command(name='ss', description="Set Stone")
async def ss(ctx, player2, position):
    game = OmokGame(ctx.author.id, getDiscordId(player2))
    if game.isAnotherGameOnGoing():
        _embed = discord.Embed(
            title='진행중인 게임이 있습니다!\n먼저 진행중인 게임을 종료해주세요!',
            color=0xff0000)
        return await ctx.send(embed=_embed)
    position = position.upper()
    x, y = al_nu[position[:1]], int(position[1:])
    if game.isMyTurn(ctx.author.id):
        _embed = discord.Embed(
            title='당신의 차례가 아닙니다!',
            color=0xff0000)
        return await ctx.send(embed=_embed)
    elif game.isAbleSetStone(x, y):
        _embed = discord.Embed(
            title='해당 위치에는 돌을 놓을 수 없습니다 ^^',
            color=0xff0000)
        return await ctx.send(embed=_embed)
    game.putStone(ctx.author.id, x, y)
    out = sendImage(game)
    _embed = discord.Embed(
        title=f'{game.color[game.turn]}의 차례입니다.',
        color=0x55ee00)
    await ctx.send(f"<@!{ctx.author.id}> vs {player2}\n", file=out, embed=_embed)


@app.command(name='end', description="게임 종료")
async def end(ctx, player2):
    game = OmokGame(ctx.author.id, getDiscordId(player2))
    game.gameTerminate()
    _embed = discord.Embed(
        title='게임이 종료되었습니다.',
        color=0xaa1faa)
    await ctx.send(embed=_embed)


@app.command(name="help", description="Returns all commands available")
async def help(ctx):
    helptext = "```"
    for command in app.commands:
        helptext += f"{command}\n"
    helptext += "```"
    await ctx.send(helptext)


with open('keys.json') as json_file:
    data = json.load(json_file)
app.run(data["Bot_Key"])
