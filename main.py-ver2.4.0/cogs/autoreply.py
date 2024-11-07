import discord
from discord.ext import commands
import json

class AutoReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('autoreplyset.json', 'r') as f:
            self.disabled_servers = json.load(f).values()  # ServerID のみを取得

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # 対象ワードを検知
        if not await self.check_words(message):
            return

        # DMチャンネルかどうかを確認し、DMでは常に自動返信を有効にする
        if message.guild is None:
            await self.auto_reply(message)
            return

        # サーバーがjsonに載っていないかを確認し、載っていない場合にメッセージを送信
        if str(message.guild.id) not in self.disabled_servers:
            await self.auto_reply(message)
        else:
            await self.bot.process_commands(message)

    async def check_words(self, message):
        # 検知対象のワードリスト
        word_lists = {
            "bad": ["死ね", "しね", "シネ", "カス", "かす"],
            "kazume": ["かずめ", "kazume", "ぴぃまん", "ぴいまん", "kzm"],
            "osu": ["osu!", "osu", "kasu!", "gomi!", "otu!"],
            "paypal": ["ぺいぱる", "ペイパル", "PayPal"]
        }

        # 各ワードリストに基づいて検知
        for category, words in word_lists.items():
            for word in words:
                if word in message.content:
                    message.reply_category = category  # カテゴリを保存
                    return True
        return False

    async def auto_reply(self, message):
        # 検知されたカテゴリに基づいて返信メッセージを決定
        if message.reply_category == "bad":
            await message.reply("そんなこと言うのは良くないよお前が死ね")
        elif message.reply_category == "kazume":
            await message.reply("捕まろうよ〜🥰")
        elif message.reply_category == "osu":
            await message.reply("お前もwelcome to osu!")
        elif message.reply_category == "paypal":
            await message.reply("割ってなんぼやで😎")
        else:
            await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(AutoReply(bot))
