import discord
from discord.ext import commands
import ntplib
from datetime import datetime

# ボットのインテントを設定
intents = discord.Intents.default()
intents.message_content = True

# ボットのプレフィックスを設定
bot = commands.Bot(command_prefix='daruks!', intents=intents)

# NTPserver address
NTP_SERVER = 'ntp.nict.jp'

# Get JST from NTP server
def get_japan_time():
    client = ntplib.NTPClient()
    response = client.request(NTP_SERVER, version=3)
    return datetime.fromtimestamp(response.tx_time)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # bot status
    activity = discord.Game(name="🥰🥰🥰🥰🥰平和にいこうよ〜🥰🥰🥰🥰🥰")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    bad_words = ["死ね", "しね", "シネ", "カス", "かす"]
    for word in bad_words:
        if word in message.content:
            await message.reply("そんなこと言うのは良くないよお前が死ね")
            return

    if "かずめ" in message.content:
        await message.reply("捕まろうよ〜🥰")
        return

    paypal_words = ["ぺいぱる", "ペイパル", "PayPal","paypal"]
    for word in paypal_words:
        if word in message.content:
            await message.reply("割ってなんぼやで😎")
            return

    if "えっち" in message.content:
        await message.reply("えっちなのはダメ!死刑!!")
        return

    osu_words = ["osu!", "osu", "kasu!", "gomi!", "otu!"]
    for word in osu_words:
        if word in message.content:
            await message.reply("お前もwelcome to osu!\nhttps://osu.ppy.sh/")
            return


    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)
# delete command
@bot.command()
async def delete(ctx):
    if ctx.message.reference:
        reference = ctx.message.reference.resolved
        if reference and reference.author == bot.user:
            await reference.delete()
            await ctx.message.delete()
        else:
            await ctx.reply("削除できません")
    else:
        await ctx.reply("削除するメッセージを返信してください")
# your userid
@bot.command()
async def myid(ctx):
    await ctx.reply(f'あなたのユーザーIDは {ctx.author.id} です')
# bot explanation
@bot.command()
async def custom_help(ctx):
    await ctx.reply("やあ、ブロ。これはdaruksのbotやで\n単語に返信するだけやで、ほな。")
# ping!
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.reply(f'Pong! {latency}ms')
# JST indicate
@bot.command()
async def jptime(ctx):
    japan_time = get_japan_time()
    await ctx.reply(f'日本標準時: {japan_time.strftime("%Y-%m-%d %H:%M:%S")}')

bot.run('Token')
