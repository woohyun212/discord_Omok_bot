import discord
from discord.ext import commands
from Othello import *
from io import BytesIO
from discord.ext.commands import CommandNotFound

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


@app.command()
async def start(ctx, player2):
    try:
        game = OmokGame(ctx.author.id, getDiscordId(player2))
        game.gameSave()
        out = sendImage(game)
        await ctx.send(f"<@!{ctx.author.id}> vs {player2}\n", file=out)
    except OngoingException:
        _embed = discord.Embed(
            title='게임을 진행중인 플레이어가 있습니다!\n먼저 진행중인 게임을 종료해주세요!',
            color=0xff0000)
        await ctx.send(embed=_embed)


@app.command()
async def ss(ctx, player2, position):
    try:
        game = OmokGame(ctx.author.id, getDiscordId(player2))
        game.putStone(ctx.author.id, position)
        out = sendImage(game)
        game.gameSave()
        await ctx.send(f"<@!{ctx.author.id}> vs {player2}\n", file=out)

    except OngoingException:
        _embed = discord.Embed(
            title='진행중인 게임이 있습니다!\n먼저 진행중인 게임을 종료해주세요!',
            color=0xff0000)
        await ctx.send(embed=_embed)
    except CannotSetStoneException:
        _embed = discord.Embed(
            title='해당 위치에는 돌을 놓을 수 없습니다 ^^',
            color=0xff0000)
        await ctx.send(embed=_embed)


@app.command(name='게임 종료', description="")
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


app.run('ODg1MzYzNTUyNTk1MDg3NDEz.YTl9EA.3BIKD5J7cCjapiIcQb_hYJL8Ko8')
