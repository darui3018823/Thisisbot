import discord
from discord.ext import commands

daruksid = 973782871963762698

class Contact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def contact(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send(
                "ご連絡ありがとうございます。\nリプライをせずにこのメッセージのあとに、main!を付けて送信くださいませ。\n以下にテンプレートを掲載します。ご利用ください。\nキャンセルする際はcancel!とご入力ください。\nメールでのご連絡をご希望の場合はmail!とご入力ください。\n※お問い合わせ内容は1,2行で簡潔にご記入ください\n※ユーザー名は返信を希望される場合は記入ください。\n\nmain!\nお問い合わせ内容:\nユーザー名:\n利用端末:\n本文:"
            )
        else:
            await ctx.send("このコマンドはDMでのみ使用できます。")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            if message.content.startswith("main!"):
                owner = await self.bot.fetch_user(daruksid)
                await owner.send(
                    f"{message.content}\n\n送信者詳細\nユーザ名: {message.author.name}\nユーザID: {message.author.id}\n送信日時: {message.created_at}"
                )
                await message.author.send(
                    "ご連絡ありがとうございます。\n送信が完了しました。daruからのご連絡が数日以内にありますので、今しばらくお待ちください。"
                )
            elif message.content.startswith("sent!"):
                owner = await self.bot.fetch_user(daruksid)
                await owner.send(
                    f"{message.content}\n\n送信者詳細\nユーザ名: {message.author.name}\nユーザID: {message.author.id}\n送信日時: {message.created_at}"
                )
                await message.author.send(
                    "ありがとうございます。\n確認次第、お問い合わせ内容の再確認メールをこちらから送信いたします。\n@icloud.comからのメールがブロックされている場合はメールが届かない可能性があります。"
                )
            elif message.content == "cancel!":
                await message.author.send("チケットを終了しました。\n再度ご利用になる場合は`daruks!contact`とご入力ください。")
            elif message.content == "mail!":
                await message.author.send(
                    "メールでのご連絡を承ります。\n以下の情報を送信ください。\nsent!を先頭につけることで送信できます\nメールアドレス:\nご連絡を希望のメールアドレス:\nお問い合わせ内容:"
                )

async def setup(bot):
    await bot.add_cog(Contact(bot))
