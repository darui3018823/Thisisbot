import asyncio
import re
import discord
import psutil

# Eドライブの詳細取得
async def get_drive_usage(drive_path):
    # 非同期でドライブの情報を取得
    loop = asyncio.get_running_loop()
    usage = await loop.run_in_executor(None, psutil.disk_usage, drive_path)

    # 使用率、空き容量、全体容量を取得
    usage_percentage = usage.percent
    FreeSpace_Percentage = round(100 - usage_percentage, 1)  # 小数点第1位で四捨五入
    free_space_gb = usage.free / (1024 ** 3)  # GBに変換
    total_space_gb = usage.total / (1024 ** 3)  # GBに変換

    return f"{FreeSpace_Percentage}%({free_space_gb:.2f}GB/{total_space_gb:.2f}GB)"

# yt-dlpのembed処理
async def send_downloading_embed(interaction, usage_info):
    FreeSpace_info = await get_drive_usage("E:/")
    DownloadingNowEmbed = discord.Embed(title="yt-dlp.exe",
                                        description="Processing received URL",
                                        color=0x1e90ff
                                        )
    DownloadingNowEmbed.add_field(name="Free Space", value=FreeSpace_info, inline=False)
    DownloadingNowEmbed.set_footer(text="It may take a few minutes for your video to process.")
    await interaction.response.send_message(embed=DownloadingNowEmbed)
async def send_complete_embed(interaction, url):
    CompleteEmbed = discord.Embed(title="yt-dlp.exe",
                                   description="Download Completed.",
                                   color=0x00ff00
                                   )
    CompleteEmbed.add_field(name="Video URL", value=url, inline=False)
    CompleteEmbed.set_footer(text="Powered by yt-dlp, ffmpeg")
    await interaction.followup.send(embed=CompleteEmbed)
async def download_failure_embed(interaction, url, result, RunningUser):
    #エラーメッセージの処理
    def Text_Check(text):
        # 文字数を確認
        if len(result) > 100:
            # 100文字目で切って、メッセージを返す
            trimmed_text = text[:100]
            return trimmed_text
        else:
            return result
    
    ErrorText = Text_Check(result)
    
    FailureEmbed = discord.Embed(title="yt-dlp.exe",
                                 description="Download Failure...\nPlease try again.",
                                 color=0xff0000
                                 )
    FailureEmbed.add_field(name="Video URL", value=url, inline=False)
    FailureEmbed.add_field(name="Error Text", value=ErrorText, inline=False)
    FailureEmbed.set_footer(text="Powered by yt-dlp, ffmpeg")
    await interaction.response.send_message(embed=FailureEmbed)
async def HelpMessage_Embed(interaction):
    # Embed構築
    HelpMessageEmbed = discord.Embed(title="yt-dlp.exe",
                                     description="This Command Help!",
                                     color=0xffff00
                                     )
    HelpMessageEmbed.add_field(name="対応サービス", value="[Youtube](https://youtube.com)\n[Twitter(X)](https://twitter.com)\n[Twitch](https://twitch.tv)\n一部短縮URLは対応していない可能性があります。\nその際は[こちら](https://daruks.com/Contact/)よりお問い合わせください", inline=False)
    HelpMessageEmbed.add_field(name="利用しているアプリケーション", value="[yt-dlp](https://github.com/yt-dlp/yt-dlp/releases)\n[ffmpeg](https://www.ffmpeg.org/download.html#build-windows)\n[Windows builds from gyan.dev](https://www.gyan.dev/ffmpeg/builds/)", inline=False)
    HelpMessageEmbed.set_footer(text="Powered by yt-dlp, ffmpeg")
    await interaction.response.send_message(embed=HelpMessageEmbed)
def extract_first_url(message_content):
    # 正規表現を使用してメッセージからURLを抽出
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, message_content)
    return urls[0] if urls else None
async def FUCKYOU(interaction):
    embed = discord.Embed(
        title="yt-dlp.exe",
        description="You are not a registered user!"
    )
    
    await interaction.response.send_message(embed=embed)