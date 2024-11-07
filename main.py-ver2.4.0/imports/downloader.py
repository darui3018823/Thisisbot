import random
import string
import subprocess
import os
import asyncio

async def download_video(interaction, url):
    # ダウンロード先ディレクトリを指定
    download_dir = 'E:/yt-dlp/bot'

    # yt-dlp.exe のフルパスを指定
    ytdlp_path = 'C:/Users/user/Applications/yt-dlp/yt-dlp.exe'

    # URLに基づいてコマンドリストを変更
    if "twitch.tv" in url:
        command = [
            ytdlp_path,
            '-f', '1080p60+bestaudio',  # 最大画質を指定
            '--merge-output-format', 'mp4',
            '--embed-thumbnail',  # サムネイルを埋め込む
            '--add-metadata',  # メタデータを追加
            '--output', os.path.join(download_dir, '%(title)s.%(ext)s'),  # 保存先
            url
        ]
    elif "youtube.com" in url or "youtu.be" in url:
        command = [
            ytdlp_path,
            '-f', 'bestvideo+bestaudio',
            '--merge-output-format', 'mp4',
            '--embed-thumbnail',  # サムネイルを埋め込む
            '--add-metadata',  # メタデータを追加
            '--output', os.path.join(download_dir, '%(title)s.%(ext)s'),  # 保存先
            url
        ]
    elif "twitter.com" in url or "x.com" in url:
        command = [
            ytdlp_path,
            '--merge-output-format', 'mp4',
            '--embed-thumbnail',  # サムネイルを埋め込む
            '--add-metadata',  # メタデータを追加
            '--output', os.path.join(download_dir, '%(title)s.%(ext)s'),  # 保存先
            url
        ]
    else:
        await interaction.followup.send("最高画質での保存ができない場合があります。")
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        
        command = [
            ytdlp_path,
            '--merge-output-format', 'mp4',
            '--output', os.path.join(download_dir, f'{random_string}.mp4'),  # 保存先
            url
        ]

    # コマンドの実行
    try:
        # 出力を無視してコマンドを実行
        subprocess.run(command, check=True)
        print("Download Completed.")
        return ('Complete')
    except subprocess.CalledProcessError as e:
        # エラーが発生した場合の処理
        print(f"Error: {e}")
        return e