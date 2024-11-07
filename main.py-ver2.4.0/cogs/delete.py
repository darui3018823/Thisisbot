import discord
from discord.ext import commands
import json
import os

class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.authorized_users = self.load_permissions()

    # 権限を持つユーザーIDをperm.jsonから読み込む
    def load_permissions(self):
        if not os.path.exists('perm.json'):
            return {}
        with open('perm.json', 'r', encoding='UTF-8') as f:
            data = json.load(f)
            return {v: k for k, v in data.items()}  # IDをキー、名前を値に反転

    @commands.command(name='delete')
    async def delete(self, ctx):
        if str(ctx.author.id) not in self.authorized_users:
            await ctx.send("あなたにはこのコマンドを実行する権限がありません。")
            return

        if ctx.message.reference is None:
            await ctx.send("リプライ元のメッセージが見つかりません。")
            return

        referenced_message = ctx.message.reference.resolved
        try:
            await referenced_message.delete()
            print("メッセージが削除されました。")
        except discord.Forbidden:
            await ctx.send("このメッセージを削除する権限がありません。")

async def setup(bot):
    await bot.add_cog(Delete(bot))
