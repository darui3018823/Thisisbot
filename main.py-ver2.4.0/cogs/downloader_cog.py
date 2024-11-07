from imaplib import Commands
import discord
from discord.ext import commands
import asyncio
import os

class DownloaderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def download_video(self, url):
        # ダウンロード先ディレクトリを指定
        download_dir = 'E:/yt-dlp/bot'

        # yt-dlp.exe のフルパスを指定
        ytdlp_path = 'C:/Users/user/Applications/yt-dlp/yt-dlp.exe'

        # URLに基づいてコマンドリストを変更
        if "twitch.tv" in url:
            command = [
                ytdlp_path,
                '-f', '1080p60+bestaudio',
                '--merge-output-format', 'mp4',
                '--embed-thumbnail',
                '--add-metadata',
                '--output', os.path.join(download_dir, '%(title)s.%(ext)s'),
                url
            ]
        elif "youtube.com" in url or "youtu.be" in url:
            command = [
                ytdlp_path,
                '-f', 'bestvideo+bestaudio',
                '--merge-output-format', 'mp4',
                '--embed-thumbnail',
                '--add-metadata',
                '--output', os.path.join(download_dir, '%(title)s.%(ext)s'),
                url
            ]
        elif "twitter.com" in url or "x.com" in url:
            command = [
                ytdlp_path,
                '--merge-output-format', 'mp4',
                '--embed-thumbnail',
                '--add-metadata',
                '--output', os.path.join(download_dir, '%(title)s.%(ext)s'),
                url
            ]
        else:
            return "対応していないURLです。"

        # コマンドの実行
        try:
            process = await asyncio.create_subprocess_exec(*command,
                                                            stdout=asyncio.subprocess.PIPE,
                                                            stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                return "ダウンロードが完了しました。"
            else:
                return f"エラーが発生しました: {stderr.decode().strip()}"
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"

    @commands.command(name="download", description="yt-dlpを利用して動画をダウンロードします。")
    @commands.describe(url="Youtube, Twitch, Twitter Video URL")
    async def youtube_download(self, interaction: discord.Interaction, url: str):
        message, error = await self.download_video(url)

        embed = discord.Embed(title="動画ダウンロード", color=discord.Color.blue())
        if message:
            embed.description = message
        else:
            embed.description = error

        await interaction.response.send_message(embed=embed)

    @commands.context_menu(name="Download Video")
    async def download_youtube_video(self, interaction: discord.Interaction, message: discord.Message):
        url = message.content  # メッセージからURLを取得
        result = await self.download_video(url)
        await interaction.response.send_message(result)

# ボットにCogを追加する関数
async def setup(bot):
    await bot.add_cog(DownloaderCog(bot))
