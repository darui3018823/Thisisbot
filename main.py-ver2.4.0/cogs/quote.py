import discord
from discord.ext import commands
import requests
from io import BytesIO

class QuoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(
            discord.app_commands.ContextMenu(
                name="Create Quote Image",
                callback=self.generate_quote
            )
        )

    async def generate_quote(self, interaction: discord.Interaction, message: discord.Message):
        if not isinstance(message, discord.Message):
            await interaction.response.send_message("無効なメッセージが指定されました。")
            return

        Ahoshinet_Chinatsu_Icon = 'https://cdn.discordapp.com/avatars/1258342490990182473/ab48ea947274af5adf7403b97cad68b0.png?size=1024'

        user = message.author
        user_name = user.name
        display_name = user.display_name
        display_avatar_url = user.display_avatar.url if user.display_avatar else Ahoshinet_Chinatsu_Icon
        # デバッグ情報を出力
        print(f"User to send data: {user.display_name}")
        print(f"Avatar URL: {display_avatar_url}")
        print(f"User name: {user_name}")
        print(f"Display name: {display_name}")
        print(f"Message Content: {message.content}")

        # APIのエンドポイントURL
        api_url = 'https://api.voids.top/quote'
        print(f"API URL: {api_url}")

        # 取得した情報を新しいデータに追加
        miqdata = {
            'username': user_name,
            'display_name': display_name,
            'text': message.content,  # メッセージ内容
            'avatar': display_avatar_url,
            'color': True
        }

        # JSONデータを指定された形式に合わせて整形
        headers = {'Content-Type': 'application/json'}
        post_response = requests.post(api_url, json=miqdata, headers=headers)

        # POSTリクエストの結果を確認
        if post_response.status_code == 201:
            response_data = post_response.json()
            if 'url' in response_data:
                image_url = response_data['url']
                print(f"Image URL: {image_url}")

                # 画像データを取得して返信
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_data = BytesIO(image_response.content)
                    file = discord.File(image_data, filename="quote_image.png")
                    await interaction.response.send_message(content="Quote Image:", file=file)
                else:
                    await interaction.response.send_message(f"画像の取得に失敗しました: {image_response.status_code}")
            else:
                await interaction.response.send_message("画像URLが返されませんでした。")
        else:
            await interaction.response.send_message(f"データ送信中にエラーが発生しました: {post_response.status_code}")

async def setup(bot):
    await bot.add_cog(QuoteCog(bot))
