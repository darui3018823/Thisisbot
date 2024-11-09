import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
from datetime import datetime

class PackageTracking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def take_screenshot(self, url, tracking_id):
        firefox_options = FirefoxOptions()
        firefox_options.add_argument('--headless')  # ヘッドレスモードで起動
        firefox_options.add_argument('--window-size=1200x800')  # ウィンドウサイズの指定

        # geckodriver のパスを指定
        service = FirefoxService(executable_path='C:/geckodriver/geckodriver.exe')  # geckodriver のパスを設定
        driver = webdriver.Firefox(service=service, options=firefox_options)

        try:
            driver.get(url)
            screenshot_path = f"screenshot_{tracking_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(screenshot_path)
            return screenshot_path
        finally:
            driver.quit()

    @commands.slash_command(name="track", description="Track a package")
    async def track(self, ctx, service: str, tracking_id: str):
        # -を除去
        tracking_id = tracking_id.replace('-', '')

        if service.lower() == 'ヤマト運輸':
            url = f"https://member.kms.kuronekoyamato.co.jp/parcel/detail?pno={tracking_id}"
        elif service.lower() == '日本郵便':
            url = f"https://trackings.post.japanpost.jp/services/srv/search?requestNo1={tracking_id}&requestNo2=&requestNo3=&requestNo4=&requestNo5=&requestNo6=&requestNo7=&requestNo8=&requestNo9=&requestNo10=&search.x=53&search.y=28&startingUrlPatten=&locale=ja"
        else:
            await ctx.send("Invalid service selected. Please choose either 'ヤマト運輸' or '日本郵便'.")
            return

        # スクリーンショットの取得
        screenshot_path = self.take_screenshot(url, tracking_id)
        
        # スクリーンショットを Discord チャンネルに送信
        with open(screenshot_path, 'rb') as file:
            await ctx.send("Here is the tracking result:", file=discord.File(file, filename=screenshot_path))
        
        # スクリーンショットファイルを削除
        os.remove(screenshot_path)