import asyncio
import random
import re
import shlex
from typing import Optional
import discord
from discord.ext import commands
from discord import Attachment, File, Interaction, app_commands
import os
import subprocess
import json
from datetime import datetime,timedelta
from httpcore import TimeoutException
import ipinfo
import logging
from io import BytesIO
import pytz
import requests
from googletrans import Translator
import psutil
import time
from discord.app_commands import (
    allowed_installs,
)
import wmi
import GPUtil
from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from imports.downloader import download_video 
from imports.log_func import log_command
from imports.random_async import(
    Argument_is_None_Embed, None_Check_Process, Running_Random_Choice, Success_Embed_Send, Unknown_Error, ve_Embed
    )
from imports.ytdlp_async import(
    extract_first_url, get_drive_usage,
    send_downloading_embed, send_complete_embed,
    download_failure_embed, HelpMessage_Embed
    )
from imports.preload import(
    get_current_directory, get_python_version,
    is_virtual_env, load_permissions,
    load_blacklist, save_blacklist,
    load_commands_json, convert_link,
    log_conversion, save_permissions,
)

translator = Translator()
intents = discord.Intents.default()
intents.message_content = True
ipinfo_access_token = 'Token'
daruksstatustime = datetime.now()

bot = commands.Bot(command_prefix='daruks!', intents=intents)
daruks = 973782871963762698
start_time = datetime.now()
ipinfo_handler = ipinfo.getHandler(ipinfo_access_token)
botversion = 'Ver.2.4.0 Beta'
PowerShellVersion = '5.1.22621'
GECKODRIVER_PATH = 'C:/geckodriver/geckodriver.exe'

# WebSocket Pingを測定するための変数
websocket_ping = None
ping_start_time = None

#それぞれの初期化
authorized_users = load_permissions()
commands_dict = load_commands_json()
blacklist = load_blacklist()

# setup cog files
async def setup_cogs():
    try:
        # Cogの読み込み
        await bot.load_extension("cogs.delete")
        print("delete.py Load complete.")

        await bot.load_extension("cogs.contact-cog")
        print("contact-cog.py Load complete.")

        await bot.load_extension("cogs.py_cog")
        print("py_cog.py Load complete.")

        await bot.load_extension("cogs.iplookup_cog")
        print("iplookup_cog.py Load complete")

        await bot.load_extension("cogs.quote")
        print("quote.py Load complete")


    except Exception as e:
        print(f"An error occurred while loading cogs: {e}")

#Track cmd
async def take_screenshot(url, tracking_id):
    firefox_options = FirefoxOptions()
    firefox_options.add_argument('--headless')  # ヘッドレスモードで起動
    firefox_options.add_argument('--window-size=1200x800')  # ウィンドウサイズの指定

    # geckodriver のパスを指定
    service = FirefoxService(executable_path='C:/geckodriver/geckodriver.exe')  # geckodriver のパスを設定
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        driver.get(url)
        
        # ページのサイズを取得
        body = driver.find_element(By.TAG_NAME, 'body')
        body_width = body.size['width']
        body_height = body.size['height']

        # ウィンドウサイズを設定
        driver.set_window_size(body_width, body_height)

        # スクリーンショットを保存
        screenshot_path = f"screenshot_{tracking_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        return screenshot_path
    finally:
        driver.quit()

# cmd list
admincmdlist = [
        "- perm",
        "daruks!perm <add,delete,list> <UserID>",
        "権限を管理します",
        "- blacklist",
        "daruks!blacklist <add,delete,list> <UserID>",
        "ブラックリストを管理します",
        "- py",
        "daruks!py <Python Code,Python File>",
        "Pythonコードを実行しその出力結果を送信します。",
        "- powershell",
        "daruks!powershell <command>",
        "PowerShellでコマンドを実行します",
        "- stop",
        "daruks!stop",
        "botを停止させます",
        "- restart",
        "daruks!restart",
        "botを再起動します",
        ]
needpermcmdlist = [
        "- run",
        "daruks!run <Key Word>",
        "commands.jsonに記載のあるキーワードに対応するものを実行します",
        "- fullpath",
        "daruks!fullpath <Fullpath>",
        "提供されたファイルパスを実行します",
        "- delete",
        "daruks!delete",
        "リプライ先のbotのメッセージを削除します",
        "- export",
        "daruks!export",
        "指定されたファイルをエクスポートします",
        ]
everyonecmd = [
        "- contact",
        "daruks!contact",
        "dmでのみ実行可能",
        "- help",
        "daruks!help",
        "Discord既定のhelpコマンド",
        "- invite",
        "daruks!invite",
        "botの招待リンクを送信",
        "- iplookup",
        "daruks!iplookup <IP Address>",
        "iplookupを行います。IPv4,v6どちらも可能です。",
        "Powered by ipapi.",
        "- miq(beta)",
        "daruks!miq",
        "Quoteを生成します。ベータ版です。",
        "- status",
        "daruks!status",
        "botのステータスを送信します。",
        "- verinfo",
        "daruks!verinfo",
        "botの現在のバージョン情報を送信します",
        "- cmdlist",
        "daruks!cmdlist <1,2,3,all,slash,help or None>",
        "指定された引数に従ってコマンドとそのリストを送信します。",
        "- twLink Convertert(Auto Reply)",
        "`https://x.com`, `https://twitter.com`が先頭についたURLをdmで送信すると`https://fxtwitter.com`に変更されたURLが送信されます。\n;deleteをURLにリプライで送信すると削除できます。"
        ]
cmdlisthelp = [
        "daruks!cmdlist <引数>",
        "提供された引数によって表示するコマンドリストが違います。",
        "",
        "- 1",
        "全てのユーザーが実行可能なコマンド一覧を送信します。",
        "- 2",
        "perm.jsonに記載されているユーザーが実行可能なコマンド一覧を送信します",
        "- 3",
        "管理者のみ実行可能なコマンド一覧を送信します。",
        "- all",
        "コマンドリストを全て送信します。",
        "- slash",
        "スラッシュコマンドの一覧と入力方法を送信します。",
        "- help, None",
        "引数が提供されない、またはhelpが提供されるとこのコマンドを表示します。"
        ]
slashcmdlist = [
        "- export",
        "/export option:filename",
        "指定されたファイルを送信します",
        "- invite",
        "/invite",
        "botの招待リンクを送信します。",
        "- ping",
        "/ping",
        "botのレイテンシを計測します",
        "- serverinfo"
        "/serverinfo",
        "サーバー情報を取得します",
        "- status",
        "/status",
        "botのステータスを送信します",
        "- cmdlist",
        "/cmdlist option:listnum",
        "(このコマンド)対応する引数に対してコマンドリストとその説明を送信します",
        "- active-dev",
        "/active-dev",
        "Discord Active Developer Badgeの取得ページを本人のみ確認可能なメッセージで送信します",
        "- pc_status",
        "/pc_status",
        "実行環境のステータスを送信します。",
        "- userinfo",
        "/userinfo user:UserID, SelectUser, AccountName",
        "userから渡されたユーザーのユーザー情報を取得、送信します。",
        "- track",
        "/track company:運送会社 track_id:追跡番号",
        "各サイトで検索を行いフルスクリーンショットを撮影し送信します。",
        "- ytdl",
        "/ytdl url:YouTube Video Url",
        "urlに渡されたurlをダウンロードします。",
        "- stop",
        "/stop",
        "botを停止させます。管理者のみ実行可能です",
        "- restart",
        "/restart",
        "botを再起動します。管理者のみ実行可能です"
        ]

#解説
This_Version_Info = [
    "",
    "✂︎------------------------------------------✂︎",
    "",
    " Version Information! :",
    " - This Code Version: 2.4.0",
    " - Development Stage: Pre-Release",
    " - Release Date: 24/11/04 1:50",
    " - Note: 重大なバグが潜んでるものだと思ってください",
    "",
    "✂︎------------------------------------------✂︎",
    ""
]

# on_ready
@bot.event
async def on_ready():
    logging.info('Bot is ready.')
    print("Log in Now...")
    print(f'Logged in as {bot.user}')
    print("\n".join(This_Version_Info))
    time.sleep(3)
    await bot.change_presence(activity=discord.CustomActivity("平和に逝こうよ～🥰 "))
    #online(通常及び規定)status=discord.Status.online
    #idle(退席中)status=discord.Status.idle
    #dnd(取り込み中)status=discord.Status.dnd
    await setup_cogs()

    # スラッシュコマンドを同期
    try:
        synced = await bot.tree.sync()  
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

    # on_ready_daruksdm
    on_ready_daruksdm = daruks  # 管理者ユーザーID
    user = await bot.fetch_user(on_ready_daruksdm)
    if user:
        try:
            # UTC+9のタイムゾーンを取得
            tokyo_tz = pytz.timezone('Asia/Tokyo')
            # 現在のUTC時刻を取得
            utc_now = datetime.now(pytz.utc)
            # UTC時刻をUTC+9に変換
            local_now = utc_now.astimezone(tokyo_tz)
            # 時刻をHH:MM:SS形式で表示
            time_str = local_now.strftime("%H:%M:%S")
            
                        
            python_version = get_python_version()
            current_directory = get_current_directory()
            virtual_env_status = is_virtual_env()


            # Embedメッセージの作成
            embed = discord.Embed(
                title="This is bot",
                color=0x00ff00,  # 黄緑色
                description="Bot Status",
            )
            embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
            embed.add_field(name="Bot Latency", value=f"{round(bot.latency * 1000)} ms")
            embed.add_field(name="Bot Run Time at", value=f"{time_str}")
            embed.add_field(name="Load Files", value="All Ready")
            
            embed.add_field(name="Execution Environment", value=current_directory, inline=False)
            embed.add_field(name="Python Version", value=python_version, inline=False)
            embed.add_field(name="Virtual Environment?", value=virtual_env_status, inline=False)

            # Tenor Gif Embed
            gif_url = "https://media1.tenor.com/m/fP8tlr2kTzQAAAAC/forrest-gump-running.gif"
            embed.set_image(url=gif_url)

            embed.set_footer(text=botversion)

            # DMを送信
            await user.send(embed=embed)
            print(f"Sent 'Bot on Ready!' Embed to {user.name}")
        except discord.Forbidden:
            print(f"Could not send DM to {user.name} (ID: {on_ready_daruksdm}), forbidden.")
        except discord.HTTPException as e:
            print(f"Failed to send DM to {user.name} (ID: {on_ready_daruksdm}), error: {e}")

# 通常のコマンドを定義
@bot.command()
async def run(ctx, keyword: str):
    # コマンドが送信されたら:arrows_counterclockwise:を付ける
    await ctx.message.add_reaction('🔄')
    log_command(ctx.author, keyword=keyword, channel_id=ctx.channel.id)  # channel_idを追加
    await run_command(ctx, keyword)

# 新しいフルパスコマンドを定義
@bot.command()
async def fullpath(ctx, *, full_path: str = None):
    # コマンドが送信されたら:arrows_counterclockwise:を付ける
    await ctx.message.add_reaction('🔄')
    log_command(ctx.author, full_path=full_path, channel_id=ctx.channel.id)  # channel_idを追加
    await run_full_path(ctx, full_path)

# Auth Manage
@bot.command()
async def perm(ctx, action: str = None, user_id: int = None):
    admin_id = daruks  # 管理者ユーザーID

    if ctx.author.id != admin_id:
        await ctx.send('You do not have permission to use this command!')
        print(f'Unauthorized user attempted perm command: {ctx.author.id}')  # debug message
        return

    if action is None:
        await ctx.send('Action is a required argument. Use "add" or "delete".')
        return

    if action == 'add':
        if user_id is not None:
            user = await bot.fetch_user(user_id)  # ユーザー情報を取得
            if user and user.name not in authorized_users:
                authorized_users[user.name] = str(user_id)  # user_idを文字列として保存
                save_permissions(authorized_users)
                await ctx.send(f'User {user.name} (ID: {user_id}) added.')
            elif user:
                await ctx.send(f'User {user.name} (ID: {user_id}) is already in the list.')
            else:
                await ctx.send(f'User with ID {user_id} not found.')
        else:
            await ctx.send('Please provide a UserID to add.')

    elif action == 'delete':
        if user_id is not None:
            user_id_str = str(user_id)  # user_idを文字列に変換
            user_name_to_delete = None
            for user_name, id in authorized_users.items():
                if id == user_id_str:
                    user_name_to_delete = user_name
                    break

            if user_name_to_delete:
                del authorized_users[user_name_to_delete]
                save_permissions(authorized_users)
                await ctx.send(f'User {user_name_to_delete} (ID: {user_id}) removed.')
            else:
                await ctx.send(f'User ID {user_id} not found in the list.')
        else:
            await ctx.send('Please provide a UserID to delete.')

# daruks!run
async def run_command(ctx, keyword: str):
    print(f'run_command called with keyword: {keyword}')  # debug message

    if str(ctx.author.id) not in authorized_users.values():
        await ctx.send('You have no authority!')
        print(f'Unauthorized user: {ctx.author.id}') # debug message
        return
    
    command = commands_dict.get(keyword)
    if not command:
        await ctx.send(f'No command found for keyword: {keyword}\nHelp:\nIf the command contains spaces,\nplease use "Key Word"\nCommand List:`daruks!export commands`')
        print(f'No command found for keyword: {keyword}')  # debug message
        return

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        await ctx.message.add_reaction('✅')  # 実行完了後に:white_check_mark:を付ける
        await ctx.send(f'Command output: {result.stdout}')
        print(f'Run User: {ctx.author.id}')
        print(f'Command output: {result.stdout}')  # debug message

    except Exception as e:
        await ctx.send(f'Error: {str(e)}')
        print(f'Error: {str(e)}')  # debug message

    if keyword is None:
        await ctx.send('The value "keyword" was not provided.\nUse:`daruks!run <keyword>`\nGet the value "keyword" with `daruks!export commands`.')
        print(f'value "keyword" was not provided.\ndebug: Running User: {ctx.author.id}')

# daruks!fullpath
async def run_full_path(ctx, full_path: str):
    if str(ctx.author.id) not in authorized_users.values():
        await ctx.send('You have no authority!')
        print(f'Unauthorized user: {ctx.author.id}')  # debug message
        return

    if not os.path.isfile(full_path):
        await ctx.send(f'File not found: {full_path}')
        print(f'File not found: {full_path}')  # debug message
        return

    try:
        result = subprocess.run(full_path, shell=True, capture_output=True, text=True)
        await ctx.message.add_reaction('✅')  # 実行完了後に:white_check_mark:を付ける
        await ctx.send(f'Command output: {result.stdout}')
        print(f'Command output: {result.stdout}')  # debug message

    except Exception as e:
        await ctx.send(f'Error: {str(e)}')
        print(f'Error: {str(e)}')  # debug message

    if full_path is None:
        await ctx.send('The value "full_path" was not provided.\nExample:`daruks!fullpath <fullpath>`')
        print(f'value "full_path" was not provided.\ndebug: Running User: {ctx.author.id}')

# daruks!blacklist
@bot.command()
async def blacklist(ctx, action: str = None, user_id: int = None):
    admin_id = daruks  # 管理者ユーザーID

    if ctx.author.id != admin_id:
        await ctx.send('You do not have permission to use this command!')
        print(f'Unauthorized user attempted blacklist command: {ctx.author.id}')  # debug message
        return

    if action is None:
        await ctx.send('Action is a required argument. Use "add", "delete", or "list".')
        return

    blacklist_data = load_blacklist()  # 変数名を変更

    if action == 'add':
        if user_id is not None:
            user = await bot.fetch_user(user_id)  # ユーザー情報を取得
            if user and user.name not in blacklist_data:
                blacklist_data[user.name] = str(user_id)  # user_idを文字列として保存
                save_blacklist(blacklist_data)
                await ctx.send(f'User {user.name} (ID: {user_id}) added to blacklist.')
            elif user:
                await ctx.send(f'User {user.name} (ID: {user_id}) is already in the blacklist.')
            else:
                await ctx.send(f'User with ID {user_id} not found.')
        else:
            await ctx.send('Please provide a UserID to add.')

    elif action == 'delete':
        if user_id is not None:
            user_id_str = str(user_id)  # user_idを文字列に変換
            user_name_to_delete = None
            for user_name, id in blacklist_data.items():
                if id == user_id_str:
                    user_name_to_delete = user_name
                    break

            if user_name_to_delete:
                del blacklist_data[user_name_to_delete]
                save_blacklist(blacklist_data)
                await ctx.send(f'User {user_name_to_delete} (ID: {user_id}) removed from blacklist.')
            else:
                await ctx.send(f'User ID {user_id} not found in the blacklist.')
        else:
            await ctx.send('Please provide a UserID to delete.')

    elif action == 'list':
        if blacklist_data:
            user_list = '\n'.join([f'{user}: {user_id}' for user, user_id in blacklist_data.items()])
            await ctx.send(f'```Blacklisted Users:\n{user_list}```')
        else:
            await ctx.send('No blacklisted users found.')

    else:
        await ctx.send('Invalid action. Use "add", "delete", or "list".')

# daruks!export
@bot.command()
async def export(ctx, file_type: str = None):
    if file_type is None:
        await ctx.send('Action is a required argument. Use "perm", "blacklist" or "commands".')
        return
    if file_type not in ['blacklist', 'perm', 'commands']:
        await ctx.send('Invalid file type. Use "perm", "blacklist" or "commands".')
        return

    file_name = f'{file_type}.json'
    if not os.path.exists(file_name):
        await ctx.send(f'{file_name} file not found.')
        return
    
    await ctx.send(file=discord.File(file_name))

# daruks!ping
@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000  # bot.latencyは秒単位なので、ミリ秒に変換
    await ctx.send(f'Pong! Latency: {latency:.2f} ms')

# daruks!status
@bot.command(name="status")
async def status(ctx):
    try:
        # Runtimeの表記
        current_time = datetime.now()
        elapsed_time = current_time - daruksstatustime
        total_seconds = int(elapsed_time.total_seconds())

        # 時間、分、秒に変換
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        
        Current_Directory = get_current_directory()
        Py_Ver = get_python_version()
        Venv_Status = is_virtual_env()

        
        # Embedメッセージの作成
        embed = discord.Embed(
            title="This is bot",
            color=0x00ff00,  # 黄緑色
            description="Bot Status",
        )
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        embed.add_field(name="Bot Latency", value=f"{round(bot.latency * 1000)} ms")
        embed.add_field(name="Load JSON File", value="All Ready")
        embed.add_field(name="Execution Time", value=formatted_time)
        
        embed.add_field(name="Python Version", value=Py_Ver, inline=False)
        embed.add_field(name="Execution Environment", value=Current_Directory, inline=False)
        embed.add_field(name="Virtual Environment?", value=Venv_Status, inline=True)

        #Tenor Gif Embed
        gif_url = "https://media1.tenor.com/m/fP8tlr2kTzQAAAAC/forrest-gump-running.gif"
        embed.set_image(url=gif_url)
        
        embed.set_footer(text=f"Created by daru, {botversion}")

        # メッセージを送信
        await ctx.send(embed=embed)
        print("Sent status embed.")
    except discord.Forbidden:
        print(f"Could not send status embed to {ctx.author}.")
    except discord.HTTPException as e:
        print(f"Failed to send status embed, error: {e}")

# daruks!stopコマンド
@bot.command()
async def stop(ctx):
    # 権限確認
    if ctx.author.id != daruks:  # 管理者ユーザーID
        await ctx.send('You do not have permission to use this command!')
        return
    
    # 終了メッセージ
    await ctx.send('Bot is stopping...')
    await ctx.message.add_reaction('✅')

    await bot.close()

#daruks!verinfo
@bot.command(name="verinfo")
async def status(ctx):
    try:
        update_details = [
    "- コードのリリース形態をLatestに変更",
    "- 軽便なバグの修正",
    "- コマンドの機能改善",
    "- コードの機能改善",
    "- 一部コマンドの仕様変更",
    "- ほぼ全てのスラッシュコマンドをユーザーインストールに対応",
    "  - 今後テキストコマンドは順次スラッシュコマンドに移植します。"
    ]
        know_issue  = [
    "daruks!powershell, perm及びロギング関係が正常に動作しない不具合",
    
    ]

        # Embedメッセージの作成
        embed = discord.Embed(
            title="Bot Version info",
            color=0x0040FF,
            description="This Version Detail."
        )
        embed.add_field(name=f"This is bot {botversion}", value="\n".join(update_details), inline=False)
        embed.add_field(name="Known Issues.", value="\n".join(know_issue), inline=False)
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        
        embed.set_footer(text=f"Created by daru, {botversion}")

        # メッセージを送信
        await ctx.send(embed=embed)
        print("Sent version info embed.")
    except discord.Forbidden:
        print(f"Could not send version info embed to {ctx.author}.")
    except discord.HTTPException as e:
        print(f"Failed to send version info embed, error: {e}")

@bot.command()
async def miq(ctx):
    # リプライ元のメッセージが存在するか確認
    if ctx.message.reference:
        try:
            # リプライ元のメッセージを取得
            original_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            
            # リプライ元のメッセージのユーザーを取得
            reply_user = original_message.author
            guild = ctx.guild
            
            # ユーザーのアカウント名、表示名を取得
            user_name = reply_user.name
            display_name = reply_user.display_name

            # サーバー上で個別設定されているアイコンのURLを生成
            if reply_user.avatar:
                if guild:
                    # サーバー上で個別に設定されているアイコンの場合
                    display_avatar_url = f"https://cdn.discordapp.com/guilds/{guild.id}/users/{reply_user.id}/avatars/{reply_user.avatar}.png?size=1024"
                else:
                    # アカウントの通常のアイコン
                    display_avatar_url = reply_user.display_avatar.url
            else:
                display_avatar_url = 'https://example.com/default-avatar.png'

            # デバッグ出力
            print(f"User to send data: {display_name}")
            print(f"Message: {original_message.content}")
            print(f"Avatar URL: {display_avatar_url}")
            print(f"User name: {user_name}")
            print(f"Display name: {display_name}")

            # APIのエンドポイントURL
            api_url = 'https://api.voids.top/quote'
            print(f"API URL: {api_url}")

            # APIにGETリクエストを送信してJSONデータを取得
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                print(f"Received JSON data: {data}")

                # 取得した情報を新しいデータに追加
                miqdata = {
                    'username': user_name,
                    'display_name': display_name,
                    'text': original_message.content if original_message else "No original message",
                    'avatar': display_avatar_url,
                    'color': True
                }

                # JSONデータを指定された形式に合わせて整形
                post_data = {
                    'content-type': 'application/json',
                    'data': miqdata
                }
                print(f"Data to send in POST request: {post_data}")

                # APIにPOSTリクエストを送信
                headers = {'Content-Type': 'application/json'}
                post_response = requests.post(api_url, json=miqdata, headers=headers)
                if post_response.status_code == 201:
                    response_data = post_response.json()
                    if 'url' in response_data:
                        image_url = response_data['url']
                        print(f"Image URL: {image_url}")

                        # 画像データを取得してリプライ
                        image_response = requests.get(image_url)
                        if image_response.status_code == 200:
                            image_data = BytesIO(image_response.content)
                            file = discord.File(image_data, filename="quote_image.png")
                            await ctx.send(f"Quote Picture(This Command is beta.): {file}")
                        else:
                            await ctx.send(f"画像の取得に失敗しました: {image_response.status_code}")
                    else:
                        await ctx.send("画像URLが返されませんでした。")
                else:
                    await ctx.send(f"データ送信中にエラーが発生しました: {post_response.status_code}")
            else:
                await ctx.send(f'データ取得中にエラーが発生しました: {response.status_code}')
        except Exception as e:
            await ctx.send(f"エラーが発生しました: {str(e)}")
    else:
        await ctx.send("リプライ元のメッセージが見つかりません。")

# daruks!invite
@bot.command(name="invite")
async def invite(ctx):
    try:
        # Embedメッセージの作成
        embed = discord.Embed(
            title="This is bot invitation",
            color=0x00ff00,  # 黄緑色
        )
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        embed.add_field(name="Invitation with administrator privileges", value="[Administrator privileges](https://discord.com/oauth2/authorize?client_id=1240343650664185886&permissions=8&integration_type=0&scope=bot)", inline=False)
        embed.add_field(name="The bare minimum invitation", value="[Required privileges only](https://discord.com/oauth2/authorize?client_id=1240343650664185886&permissions=1126984386476096&integration_type=0&scope=bot)", inline=False)
        embed.add_field(name="Make your commands available everywhere", value="[User Install](https://discord.com/oauth2/authorize?client_id=1240343650664185886)", inline=False)
        embed.add_field(name="Caution!", value="最低限の権限のみでの利用も可能ですが、\n今後追加されるコマンド等が利用できない可能性があります。", inline=False)
        
        embed.set_footer(text=botversion)

        # メッセージを送信
        await ctx.send(embed=embed)
        print("Sent status embed.")
    except discord.Forbidden:
        print(f"Could not send status embed to {ctx.author}.")
    except discord.HTTPException as e:
        print(f"Failed to send status embed, error: {e}")

# daruks!restart
@bot.command()
async def restart(ctx):

    # Runtimeの表記
    current_time = datetime.now()
    elapsed_time = current_time - daruksstatustime
    total_seconds = int(elapsed_time.total_seconds())

    # 時間、分、秒に変換
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"

    if ctx.author.id != daruks:  # 管理者ユーザーID
        await ctx.send('You do not have permission to use this command!')
        return

    await ctx.send('Bot is Restarting...')
    print(f"Bot Restart at: {formatted_time}")
    await ctx.message.add_reaction('✅')
    os.system("restart.bat")
    await bot.close()

# daruks!cmdlist
@bot.command(name="cmdlist")
async def cmdlist(ctx, option=None):
    try:
        # Embedメッセージの作成
        embed = discord.Embed(
            title="Command Description",
            color=0x0040FF,
        )
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        
        if option == "1":
            embed.add_field(name="Available to Everyone Commands", value="\n".join(everyonecmd), inline=False)
        elif option == "2":
            embed.add_field(name="Need Permission Commands", value="\n".join(needpermcmdlist), inline=False)
        elif option == "3":
            embed.add_field(name="Administrator Commands", value="\n".join(admincmdlist), inline=False)
        elif option == "slash":
            embed.add_field(name="Slash Commands", value="\n".join(slashcmdlist), inline=False)
        elif option == "all":
            embed.add_field(name="Administrator Commands", value="\n".join(admincmdlist), inline=False)
            embed.add_field(name="Need Permission Commands", value="\n".join(needpermcmdlist), inline=False)
            embed.add_field(name="Available to Everyone Commands", value="\n".join(everyonecmd), inline=False)
            embed.add_field(name="Slash Commands", value="\n".join(slashcmdlist), inline=False)
        elif option is None or option.lower() == "help":
            embed.add_field(name="This Command Help", value="\n".join(cmdlisthelp), inline=False)
        else:
            embed.add_field(name="Error", value="Invalid option. Use `1` for everyone commands, `2` for permission commands, `3` for admin commands,`slash` for slash commands, or `all` for all commands.", inline=False)

        embed.set_footer(text=botversion)

        # メッセージを送信
        await ctx.send(embed=embed)
        print("Sent command list embed.")
    except discord.Forbidden:
        print(f"Could not send command list embed to {ctx.author}.")
    except discord.HTTPException as e:
        print(f"Failed to send command list embed, error: {e}")

# daruks!powershell
@bot.command(name="powershell", aliases=['ps'])
async def powershell_command(ctx, *, command: str):
    if ctx.author.id != daruks:
        await ctx.send("あなたにはこのコマンドを実行する権限がありません。")
        return
    
    try:
        # PowerShell コマンドを実行
        result = subprocess.run(
            ["powershell", "-Command", command], capture_output=True, text=True, shell=True
        )
        output = result.stdout or result.stderr

        # ログフォルダの作成
        log_dir = r"C:\Users\user\vsc\fullcode\pslog"
        os.makedirs(log_dir, exist_ok=True)

        # 現在時刻を取得し、ログファイル名を生成
        now = datetime.now()
        logfile = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_log.txt"
        logfile_name = f"./pslog/{logfile}"
        log_filename = os.path.join(log_dir, logfile)

        # ログファイルに出力内容を記録
        with open(log_filename, "w", encoding="utf-8") as log_file:
            log_file.write(f"Run Time at: {now.strftime('%Y/%m/%d %H:%M:%S')}\n")
            log_file.write(f"PowerShell Command: {command}\n")
            log_file.write("PowerShell Output:\n")
            log_file.write(output)
            log_file.write("\n--------\n")

        # print
        print(f"daruks Command\nRun PowerShell Command: {command}\nLog File: {log_filename}")

        # Embed メッセージの作成
        embed = discord.Embed(
            title="PowerShell",
            color=0x00afcc
        )
        embed.add_field(name="Run Command:", value=command, inline=False)
        embed.add_field(name="Command Output", value=logfile_name)
        embed.set_footer(text=f"PowerShell Version{PowerShellVersion}\nBot {botversion}")
        await ctx.send(embed=embed)
    
    except Exception as e:
        await ctx.send(f"エラーが発生しました: {str(e)}")

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
            words = message.content.split()
            new_message = []

            for word in words:
                # スポイラー内外を問わずURLを変換
                stripped_word = word.strip("||")  # スポイラーの || を取り除いてURLをチェック
                if stripped_word.startswith(("https://x.com/", "https://twitter.com/")):
                    converted_url = convert_link(stripped_word)
                    log_conversion(message.author, stripped_word, converted_url)  # ログ記録

                    # スポイラーが元の単語にあった場合は、変換後のURLもスポイラーで囲む
                    if word.startswith("||") and word.endswith("||"):
                        new_message.append(f"||{converted_url}||")
                    else:
                        new_message.append(converted_url)
                else:
                    # 該当しない単語は無視
                    continue

            # 変換後のメッセージがある場合のみ送信
            if new_message:
                await message.channel.send(" ".join(new_message))

    # コマンドの処理を行う
    await bot.process_commands(message)

# daruks!shutdown
@bot.command()
async def shutdown(ctx):
    if ctx.author.id == daruks:
        await ctx.send("PC is Shutdowing...")
        os.system("pcshutdown.bat")
        await bot.close()
    else:
        await ctx.send("You do not have permission to use this command!")


# slash cmd
# /test
@bot.tree.command(name='test', description='slash command test')
async def test(interaction: discord.Interaction):
    await interaction.response.send_message('Hello World')

# /cmdlist
@bot.tree.command(name="cmdlist", description="コマンドリストとその説明")
@app_commands.describe(option="Arguments in the command list to send (e.g., 1, 2, 3, all, prefix, slash, help)")
async def cmdlist(interaction: discord.Interaction, option: str = None):  # 型アノテーションを追加
    try:
        

        # Embedメッセージの作成
        embed = discord.Embed(
            title="Command Description",
            color=0x0040FF,
        )
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        
        if option == "1":
            embed.add_field(name="Available to Everyone Commands", value="\n".join(everyonecmd), inline=False)
        elif option == "2":
            embed.add_field(name="Need Permission Commands", value="\n".join(needpermcmdlist), inline=False)
        elif option == "3":
            embed.add_field(name="Administrator Commands", value="\n".join(admincmdlist), inline=False)
        elif option == "slash":
            embed.add_field(name="Slash Commands", value="\n".join(slashcmdlist), inline=False)
        elif option == "all":
            embed.add_field(name="Administrator Commands", value="\n".join(admincmdlist), inline=False)
            embed.add_field(name="Need Permission Commands", value="\n".join(needpermcmdlist), inline=False)
            embed.add_field(name="Available to Everyone Commands", value="\n".join(everyonecmd), inline=False)
            embed.add_field(name="Slash Commands", value="\n".join(slashcmdlist), inline=False)
        elif option == "prefix":
            embed.add_field(name="Administrator Commands", value="\n\n".join(admincmdlist), inline=False)
            embed.add_field(name="Need Permission Commands", value="\n\n".join(needpermcmdlist), inline=False)
            embed.add_field(name="Available to Everyone Commands", value="\n\n".join(everyonecmd), inline=False)

        elif option is None or option.lower() == "help":
            embed.add_field(name="This Command Help", value="\n".join(cmdlisthelp), inline=False)
        else:
            embed.add_field(name="Error", value="Invalid option. Use `1` for everyone commands, `2` for permission commands, `3` for admin commands,`slash` for slash commands, or `all` for all commands.", inline=False)

        embed.set_footer(text=botversion)

        # メッセージを送信
        await interaction.response.send_message(embed=embed)
        print("Sent command list embed.")
    except discord.Forbidden:
        print(f"Could not send command list embed to {interaction.user}.")
    except discord.HTTPException as e:
        print(f"Failed to send command list embed, error: {e}")

# /invite
@bot.tree.command(name="invite", description="botの招待リンクを送信します")
@allowed_installs(guilds=True, users=True)
async def invite(interaction: discord.Interaction):
    try:
        # Embedメッセージの作成
        embed = discord.Embed(
            title="This is bot invitation",
            color=0x00ff00,  # 黄緑色
        )
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        embed.add_field(name="Invitation with administrator privileges", value="[Administrator privileges](https://discord.com/oauth2/authorize?client_id=1240343650664185886&permissions=8&integration_type=0&scope=bot)", inline=False)
        embed.add_field(name="The bare minimum invitation", value="[Required privileges only](https://discord.com/oauth2/authorize?client_id=1240343650664185886&permissions=1126984386476096&integration_type=0&scope=bot)", inline=False)
        embed.add_field(name="Make your commands available everywhere", value="[User Install](https://discord.com/oauth2/authorize?client_id=1240343650664185886)", inline=False)
        embed.add_field(name="Caution!", value="最低限の権限のみでの利用も可能ですが、\n今後追加されるコマンド等が利用できない可能性があります。", inline=False)
        
        embed.set_footer(text=botversion)

        # メッセージを送信
        await interaction.response.send_message(embed=embed)
        print("Sent status embed.")
    except discord.Forbidden:
        print(f"Could not send status embed to {interaction.user}.")
    except discord.HTTPException as e:
        print(f"Failed to send status embed, error: {e}")

# /stop
@bot.tree.command(name="stop", description="botを停止させます")
async def stop(interaction: discord.Interaction):
    # 権限確認
    if interaction.user.id != daruks:  # 管理者ユーザーID
        await interaction.response.send_message('You do not have permission to use this command!')
        return
    await interaction.response.send_message('Bot is stopping...')
    await bot.close()

#/restart
@bot.tree.command(name="restart", description="botを再起動します")
@allowed_installs(guilds=True, users=True)
async def restart(interaction: discord.Interaction):

    # Runtimeの表記
    current_time = datetime.now()
    elapsed_time = current_time - daruksstatustime
    total_seconds = int(elapsed_time.total_seconds())

    # 時間、分、秒に変換
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    if interaction.user.id != daruks:
        await interaction.response.send_message('You do not have permission to use this command!')
        return
    await interaction.response.send_message('Bot is Restarting...')
    print(f"Bot Run Time: {formatted_time}")
    await bot.close()
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'restart.bat')
    await bot.close()
    os.system(f'"{script_path}"')

# /ping
@bot.tree.command(name="ping", description="botのレイテンシを計測")
@allowed_installs(guilds=True, users=True)
async def ping(interaction: discord.Interaction):
    latency = bot.latency * 1000  # latency is in seconds; convert to milliseconds
    await interaction.response.send_message(f'Latency: {latency:.2f} ms')

# /status
@bot.tree.command(name="status", description="botステータスを送信します")
@allowed_installs(guilds=True, users=True)
async def status(interaction: discord.Interaction):
    thinkingembed = discord.Embed(title="Bot Status", description="Editing Status...", color=discord.Color.orange())
    await interaction.response.send_message(embed=thinkingembed)

    try:
        # Runtimeの表記
        current_time = datetime.now()
        elapsed_time = current_time - daruksstatustime
        total_seconds = int(elapsed_time.total_seconds())

        # 時間、分、秒に変換
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"

        # 現在時刻とランタイムの計算
        running_time = datetime.now() - start_time
        running_time_str = str(timedelta(seconds=int(running_time.total_seconds())))
        
        Current_Directory = get_current_directory()
        Py_Ver = get_python_version()
        Venv_Status = is_virtual_env()

        
        # Embedメッセージの作成
        embed = discord.Embed(
            title="Bot Status",
            color=0x00ff00,  # 黄緑色
            description="Current status of the bot.",
        )
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        embed.add_field(name="Bot Latency", value=f"{round(bot.latency * 1000)} ms", inline=True)
        embed.add_field(name="Load JSON File", value="All Ready", inline=True)
        embed.add_field(name="Uptime", value=running_time_str, inline=True)  # Add uptime
        
        embed.add_field(name="Python Version", value=Py_Ver, inline=False)
        embed.add_field(name="Execution Environment", value=Current_Directory, inline=False)
        embed.add_field(name="Virtual Environment?", value=Venv_Status, inline=True)

        # Tenor Gif Embed
        gif_url = "https://media1.tenor.com/m/fP8tlr2kTzQAAAAC/forrest-gump-running.gif"
        embed.set_image(url=gif_url)
        
        embed.set_footer(text=f"Created by daru, {botversion}")

        # メッセージを送信
        await interaction.edit_original_response(embed=embed)
        print("Sent status embed.")
    except discord.Forbidden:
        print(f"Could not send status embed to {interaction.user}.")
    except discord.HTTPException as e:
        print(f"Failed to send status embed, error: {e}")

# /export
@bot.tree.command(name="export", description="指定されたファイルをエクスポートします")
@app_commands.describe(file_type="Type of file to export (e.g., perm, blacklist, commands)")
async def export(interaction: discord.Interaction, file_type: str):
    # 引数の検証
    valid_file_types = ['blacklist', 'perm', 'commands']
    if file_type not in valid_file_types:
        await interaction.response.send_message('Invalid file type. Use "perm", "blacklist", or "commands".')
        return

    file_name = f'{file_type}.json'
    if not os.path.exists(file_name):
        await interaction.response.send_message(f'{file_name} file not found.')
        return

    # ファイルを送信
    await interaction.response.send_message(file=discord.File(file_name))

#/serverinfo
@bot.tree.command(name="serverinfo", description="サーバー情報の取得")
async def serverinfo_command(interaction: discord.Interaction):
    guild = interaction.guild
    server_info = (
        f"Server Name: {guild.name}\n"
        f"ID: {guild.id}\n"
        f"Member Count: {guild.member_count}\n"
        f"Created at: {guild.created_at}\n"
    )
    await interaction.response.send_message(server_info)

# /userinfo
@bot.tree.command(name="userinfo", description="Get information about a user")
@allowed_installs(guilds=True, users=True)
async def userinfo_command(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user

    # user が None でないことを確認する
    if user is None:
        await interaction.response.send_message("Could not find user information.")
        return

    # サーバープロフィールのアイコンを取得
    display_avatar_url = user.display_avatar.url
    user_info = (
        f"Username: {user.name}\n"
        f"ID: {user.id}\n"
        f"Created at: {user.created_at}\n"
        f"Avatar URL: {display_avatar_url}"
    )
    print(display_avatar_url)
    await interaction.response.send_message(user_info)

# /active-dev
@bot.tree.command(name="active-dev", description="Discord Active Developer Badgeの取得ページを表示します")
@allowed_installs(guilds=True, users=True)
async def active_dev(interaction: discord.Interaction):
    # Discord Active Developer Badge取得ページのURL
    url = "https://discord.com/developers/active-developer"

    # エフェメラルメッセージを送信（本人のみ確認可能）
    await interaction.response.send_message(
        f"Here is the link to obtain the Discord Active Developer Badge: {url}", 
        ephemeral=True
    )

# /pc_restart
@bot.tree.command(name="pc_restart", description="pcもろとも再起動します")
@allowed_installs(guilds=True, users=True)
async def restart(interaction: discord.Interaction):

    # Runtimeの表記
    current_time = datetime.now()
    elapsed_time = current_time - daruksstatustime
    total_seconds = int(elapsed_time.total_seconds())

    # 時間、分、秒に変換
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    if interaction.user.id != daruks:
        await interaction.response.send_message('You do not have permission to use this command!')
        return
    await interaction.response.send_message('PC is Restarting...')
    print(f"Bot Restart at: {formatted_time}")
    os.system("pcrestart.bat")
    await bot.close()

# /pc_shutdown
@bot.tree.command(name="pc_shutdown", description="pcもろとも停止させます")
@allowed_installs(guilds=True, users=True)
async def restart(interaction: discord.Interaction):

    # Runtimeの表記
    current_time = datetime.now()
    elapsed_time = current_time - daruksstatustime
    total_seconds = int(elapsed_time.total_seconds())

    # 時間、分、秒に変換
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    if interaction.user.id != daruks:
        await interaction.response.send_message('You do not have permission to use this command!')
        return
    await interaction.response.send_message('PC is shuting down...')
    print(f"Bot Stop at: {formatted_time}")
    os.system("pcshutdown.bat")
    await bot.close()

# /pc_status
@bot.tree.command(name="pc_status", description="PCのステータスを表示します")
@allowed_installs(guilds=True, users=True)
async def pc_status(interaction: discord.Interaction):
    # 待機
    GetingNowEmbed = discord.Embed(title="PC Status", description="Geting PC Status...", color=discord.Color.orange())
    await interaction.response.send_message(embed=GetingNowEmbed)
    print("Send Wait Message")

    global ping_start_time
    # CPU温度取得
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        temperature_info = w.Sensor()
        found_cpu_temperature = False
        for sensor in temperature_info:
            if sensor.SensorType == u'Temperature' and 'CPU' in sensor.Name:
                cpu_temperature = sensor.Value
                found_cpu_temperature = True
                break
            if not found_cpu_temperature:
                cpu_temperature = "N/A"
    except Exception as e:
        cpu_temperature = f"エラー: {str(e)}"


    # CPU使用率取得
    cpu_usage = psutil.cpu_percent(interval=1)

    # メモリ使用率取得
    memory = psutil.virtual_memory()
    memory_usage_percent = memory.percent
    memory_usage = f"{memory_usage_percent}% "
    memory_usage_option = f"({memory.used / (1024 ** 3):.2f}GB/{memory.total / (1024 ** 3):.2f}GB)"

    # 稼働時間取得
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_string = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))

    # バッテリー残量取得
    battery = psutil.sensors_battery()
    battery_percent = f"{battery.percent}%" if battery else "N/A"

    # DiscordのWebSocket PingとAPI Ping取得
    api_ping = bot.latency  # `await`を削除

    # disk
    disk_usage = psutil.disk_usage('/')
    used_space = disk_usage.used / (1024 ** 3)  # GB単位に変換
    total_space = disk_usage.total / (1024 ** 3)  # GB単位に変換
    disk_usage_percent = disk_usage.percent
    disk_usage_option = f"{disk_usage_percent:.1f}% ({used_space:.2f}GB/{total_space:.2f}GB)"

    # CPU Clock
    def get_cpu_clock_speed():
        try:
            c = wmi.WMI()
            for processor in c.Win32_Processor():
                return f"{processor.MaxClockSpeed} MHz"
        except Exception as e:
            return f"エラー: {e}"
    cpu_clock_speed = get_cpu_clock_speed()

    def get_gpu_info():
        try:
            gpus = GPUtil.getGPUs()
            Gpu_Info = []  # 複数のGPU情報を格納するリスト
            for gpu in gpus:
                Gpu_Name = gpu.name
                GpuLoad = gpu.load * 100
                Gpu_FreeMem = gpu.memoryFree
                Gpu_UsedMem = gpu.memoryUsed
                Gpu_TotalMem = gpu.memoryTotal
                used_VRAM = Gpu_UsedMem / (1024 ** 3)  # GB単位に変換
                total_VRAM = Gpu_TotalMem / (1024 ** 3)
                detailVRAM = f'{GpuLoad}%({used_VRAM:.2f}GB/8.0GB)'  # 小数点2桁にフォーマット
                Gpu_Temperature = gpu.temperature
            
                # 個々のGPU情報を文字列として追加
                Gpu_Info.append(
                    f"┣ GPU: {Gpu_Name}\n"
                    f"┣ VRAM: {detailVRAM}\n"
                    f"┗ GPU Temperature: {Gpu_Temperature}℃"
                )
            
            return "\n".join(Gpu_Info) if Gpu_Info else "N/A"  # リストの内容を結合、なければN/Aを返す

        except Exception:
            return "N/A"
    gpu_info = get_gpu_info()
    
    # OS
    os_version = 'Windows 11 Professional (23H2)'
    
    # Synced Command
    async def Synced_Bot_Commands():
        try:
            synced = await bot.tree.sync()  
            print(f'Synced {len(synced)} command(s)')
            Synced_Command = f'Synced {len(synced)} command(s)'
            return Synced_Command
        except Exception as e:
            print(f'Failed to sync commands: {e}')
            return 'Could not get the Value:('
    result = await Synced_Bot_Commands() 

    #成形
    drkspcStatus = [
        "┣ ネットワーク接続タイプ: Ethernet",
        f"┣ CPU温度: {cpu_temperature} °C",
        f"┣ CPU使用率: {cpu_usage}%",
        f"┣ メモリ使用率: {memory_usage}{memory_usage_option}",
        f"┣ ディスク使用率: {disk_usage_option}",
        f"┣ 稼働時間: {uptime_string}",
        f"┗ バッテリー残量: {battery_percent}"
    ]
    
    Environment_Status = [
        f"┣ {result}",
        f"┣ OSVersion: {os_version}",
        f"┣ PowerShell Ver {PowerShellVersion}",
        f"┗ This is bot {botversion}"
    ]

    DiscordStatus = [
        f"┗ Discord API Ping: {api_ping * 1000:.2f}ms"
    ]

    # Embed作成
    Send_embed = discord.Embed(title="PC Status", color=discord.Color.blue())
    Send_embed.add_field(name="DARUKS", value="\n".join(drkspcStatus), inline=False)
    Send_embed.add_field(name="eGPU", value=gpu_info, inline=False)
    Send_embed.add_field(name="Execution Environment Status", value="\n".join(Environment_Status), inline=False)
    Send_embed.add_field(name="discord", value="\n".join(DiscordStatus), inline=False)
    
    Send_embed.set_footer(text=botversion)

    await interaction.edit_original_response(embed=Send_embed)
    print("Sent PC Status")

# userinfo
@bot.tree.context_menu(name="View Profile")
@allowed_installs(guilds=True, users=True)
async def view_profile(interaction: discord.Interaction, user: discord.User):
    # サーバープロフィールのアイコンを取得
    display_avatar_url = user.display_avatar.url
    user_info = (
        f"Username: {user.name}\n"
        f"Display Name: {user.display_name}\n"
        f"ID: {user.id}\n"
        f"Created at: {user.created_at}\n"
        f"Avatar URL: {display_avatar_url}"
    )
    print(display_avatar_url)
    await interaction.response.send_message(user_info)

# interlaction miq
@bot.tree.context_menu(name="Quote Message")
@allowed_installs(guilds=True, users=True)
async def quote(interaction: discord.Interaction, message: discord.Message):
    # メッセージのリプライ先を取得
    if message is None:
        await interaction.response.send_message("返信するメッセージを指定してください。")
        return

    # ユーザーのアカウント名、表示名、アイコンURLを取得
    user = message.author
    user_name = user.name
    display_name = user.display_name
    display_avatar_url = user.display_avatar.url if user.display_avatar else 'https://example.com/default-avatar.png'

    # デバッグ出力
    print(f"User to send data: {display_name}")
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
        'text': message.content,  # リプライ元のメッセージ内容
        'avatar': display_avatar_url,
        'color': True
    }

    # JSONデータを指定された形式に合わせて整形
    headers = {'Content-Type': 'application/json'}
    post_response = requests.post(api_url, json=miqdata, headers=headers)
    
    if post_response.status_code == 201:
        response_data = post_response.json()
        if 'url' in response_data:
            image_url = response_data['url']
            print(f"Image URL: {image_url}")

            # 画像データを取得してリプライ
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_data = BytesIO(image_response.content)
                file = discord.File(image_data, filename="quote_image.png")
                await interaction.response.send_message(content="Quote Picture(This Command is beta.):", file=file)
            else:
                await interaction.response.send_message(f"画像の取得に失敗しました: {image_response.status_code}")
        else:
            await interaction.response.send_message("画像URLが返されませんでした。")
    else:
        await interaction.response.send_message(f"データ送信中にエラーが発生しました: {post_response.status_code}")


# 考え中のテスト
@bot.tree.command(name="thinktest")
async def thinktest(interaction: discord.Interaction):
    # 最初に「考え中...」メッセージを送信
    await interaction.response.send_message(f"{bot.user.name}が考え中...")

    # 少し待つ（例えば、2秒待機）
    await asyncio.sleep(2)

    # メッセージを更新
    await interaction.edit_original_response(content="考えがまとまりました！")

# /track
@bot.tree.command(name="track", description="Track a package")
@app_commands.describe(
    company="ヤマト運輸, 日本郵便, AliExpress, 佐川急便, 日本通運, DHL",
    tracking_id="追跡番号を入力してください。",
    hidden="True or False"
)
@allowed_installs(guilds=True, users=True)
async def track(interaction: discord.Interaction, company: str, tracking_id: str, hidden: str = None):
    await interaction.response.send_message("Please wait a Moment...")
    print("Get Track Command")
    print(f"Track detail:\nTrack ID: {tracking_id}\nShipping company: {company.lower()}")
    try:
        # メッセージの可視性を制御
        if hidden in ['有効', 'はい', 'True', None]:
            ephemeral = True  # 本人のみ閲覧可能
        elif hidden in ['無効', 'いいえ', 'False']:
            ephemeral = False  # 通常メッセージ
        else:
            await interaction.edit_original_response("Invalid input for 'Hidden'. Please enter 有効, はい, True, or leave it blank for hidden messages. Enter 無効, いいえ, False for public messages.")
            return

        # -を除去
        tracking_id = tracking_id.replace('-', '')

        if company in ['ヤマト運輸', 'Yamato', 'クロネコヤマト']:
            url = f"https://member.kms.kuronekoyamato.co.jp/parcel/detail?pno={tracking_id}"
            print(url)
            site = 'Kuroneko Yamato WebSite'
        elif company in ['日本郵便', 'Japan Post', '郵便']:
            url = f"https://trackings.post.japanpost.jp/services/srv/search?requestNo1={tracking_id}&requestNo2=&requestNo3=&requestNo4=&requestNo5=&requestNo6=&requestNo7=&requestNo8=&requestNo9=&requestNo10=&search.x=53&search.y=28&startingUrlPatten=&locale=ja"
            print(url)
            site = 'Japan Post WebSite'
        elif company in ['AliExpress', 'aliexpress', 'アリエク']:
            url = f"https://www.ship24.com/ja/tracking?p={tracking_id}"
            print(url)
            site = 'Ship24 WebSite'
        elif company in ['佐川急便', 'Sagawa Kyubin', 'Sagawa']:
            url = f"https://www.ship24.com/ja/tracking?p={tracking_id}"
            print(url)
            site = 'Ship24 Website'
        elif company in ['日本通運', 'Nippon Express', '日通', 'NX']:
            url = f"https://lp-trace.nittsu.co.jp/web/webarpaa702.srv?LANG=JP&officeselect2=&denpyoNo1={tracking_id}"
            print(url)
            site = 'Nippon Express WebSite'
        elif company in ['DHL', 'dhl']:
            url = f"https://www.dhl.com/jp-ja/home/tracking/tracking-supply-chain.html?submit=1&tracking-id={tracking_id}"
            print(url)
            site = 'DHL WebSite'
        else:
            await interaction.edit_original_response("Invalid service selected. Please choose either 'ヤマト運輸', '日本郵便', 'AliExpress' or '佐川急便'.")
            return

        # スクリーンショットの取得
        screenshot_path = await take_screenshot(url, tracking_id)
        print(screenshot_path)

        embed = discord.Embed(
                title="Tracking Detail",
                color=0x00ff00
        )
        
        fname="result.png " # アップロードするときのファイル名 自由に決めて良いですが、拡張子を忘れないように
        file = discord.File(fp=screenshot_path, filename=fname, spoiler=False) # ローカル画像からFileオブジェクトを作成
        
        # スクリーンショットを Discord チャンネルに送信
        with open(screenshot_path, 'rb') as file:
            # Make Embed
            embed.add_field(name="URL:", value=url, inline=False)
            embed.set_image(url=f"attachment://{fname}") # embedに画像を埋め込むときのURLはattachment://ファイル名
            embed.set_footer(text=f"Powered by {site}")

            await interaction.followup.send(embed=embed, file=discord.File(file, filename=screenshot_path), ephemeral=ephemeral)
            print("Send Success")

    except Exception as e:
        print(f"Error occurred: {e}")
        await interaction.followup.send("取得または送信に失敗しました。もう一度試してみてください。")
    except discord.Forbidden:
        print(f"Forbidden")
    except discord.HTTPException as e:
        print(f"Failed to send, error: {e}")
        
    finally:
        # スクリーンショットファイルを削除（ファイルが存在する場合）
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

# /site_sc
@bot.tree.command(name="site_sc", description="指定されたサイトのスクリーンショットを撮影します")
@allowed_installs(guilds=True, users=True)
@app_commands.describe(
    sc_option="fullscreen or None"
    )
async def site_sc(interaction: discord.Interaction, url: str, sc_option: str = None):
    await interaction.response.send_message("Please wait a Moment...")
    user = interaction.user
    start_time = time.time()
    print(
        f"User: {user.name}, {user.id}\n",
        f"Time at: {start_time}\n",
        f"Url: {url}\n",
        f"Option: {sc_option}"
        )
    try:
        # ヘッドレスブラウザの設定
        options = Options()
        options.headless = True
        
        # GECKODRIVER_PATH を Service で設定
        service = Service(executable_path=GECKODRIVER_PATH)
        
        # WebDriver の初期化
        driver = webdriver.Firefox(service=service, options=options)

        # ウィンドウサイズを指定
        driver.set_window_size(1920, 1080)

        # 指定されたURLにアクセス
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        except TimeoutException:
            await interaction.followup.send("ページの読み込みに失敗しました。")
            driver.quit()
            return

        # スクリーンショットのオプション処理
        screenshot_path = "screenshot.png"
        if sc_option in ['有効', 'フルスクリーン', '全画面', 'True', 'true']:
            # フルスクリーンショットを撮影
            total_height = driver.execute_script("return document.body.scrollHeight")
            driver.set_window_size(1920, total_height)
            driver.save_screenshot(screenshot_path)
        else:
            # 現在表示されている範囲のみのスクリーンショットを撮影
            driver.save_screenshot(screenshot_path)

        driver.quit()

        # Discordに画像を送信
        elapsed_time = time.time() - start_time
        await interaction.followup.send(content=f"**Result**\nRun Time: {elapsed_time:.2f} sec\nScreen Shot:", file=discord.File(screenshot_path))
        print("Sucsses.")

        # スクリーンショットファイルを削除
        os.remove(screenshot_path)
    except Exception as e:
        await interaction.followup.send(f"エラーが発生しました: {e}")
        print(f"Error:\n{e}")

     # 30秒を超える場合はタイムアウトメッセージを送信
    if time.time() - start_time > 30:
        await interaction.followup.send("Session timed out!\nReason: Execution time exceeded 30 seconds")
        print("Session Time Out")

# /yt-dlp
@bot.tree.command(name="yt-dlp", description="Running yt-dlp.exe")
@allowed_installs(guilds=True, users=True)
@app_commands.describe(url="Video URL, 値を入力せずに送信するとヘルプを見ることができます。")
async def youtube_download(interaction: discord.Interaction, url: str = None):
    if url is None:
        await HelpMessage_Embed(interaction)
        return
    
    RunningUser = interaction.user
    
    drive_path = 'E:\\'
    usage_info = await get_drive_usage(drive_path)
    
    await send_downloading_embed(interaction, usage_info)
    
    # downloader.pyの関数を呼び出す
    result = await download_video(interaction, url)
    
    if result == 'Complete':
        await send_complete_embed(interaction, url)
    else:
        await download_failure_embed(interaction, url, result, RunningUser)

@bot.tree.context_menu(name="Download Video")
@allowed_installs(guilds=True, users=True)
async def download_youtube_video(interaction: discord.Interaction, message: discord.Message):
    url = extract_first_url(message.content)  # メッセージの内容からURLを抽出
    
    if url is None:
        # 対応していないURLの場合のエラーメッセージを埋め込みで送信
        error_embed = discord.Embed(
            title="yt-dlp Help!",
            description="This Command Help!",
            color=0xffff00
        )
        error_embed.add_field(name="対応サービス",
                              value="https://twitch.tv/\nhttps://twitter.com/\nhttps://x.com/\nhttps://youtube.com/\nhttps://youtu.be/",
                              inline=False
                              )
        error_embed.add_field(name="利用しているアプリケーション",
                              value="[yt-dlp](https://github.com/yt-dlp/yt-dlp/releases)\n[ffmpeg](https://www.ffmpeg.org/download.html#build-windows)\n[Windows builds from gyan.dev](https://www.gyan.dev/ffmpeg/builds/)",
                              inline=False
                              )
        error_embed.set_footer(text="Powered by yt-dlp, ffmpeg")
        await interaction.response.send_message(embed=error_embed)
        return
    
    # Eドライブの容量処理
    drive_path = 'E:\\'
    usage_info = await get_drive_usage(drive_path)
    
    # ダウンロード開始の埋め込みメッセージ
    await send_downloading_embed(interaction, usage_info)
    
    # downloader.pyの関数を呼び出す
    result = await download_video(interaction, url)
    
    if result == 'Complete':
        await send_complete_embed(interaction, url)
    else:
        await download_failure_embed(interaction, url, result)

# /random
@bot.tree.command(name="random", description="入力された値をランダムで抽選します。")
@allowed_installs(guilds=True, users=True)
@app_commands.describe(
    items="スペース区切りを利用してください。スペースのある単語は""で囲んでください。",
    file="スペース区切りを利用してください。スペースのある単語は""で囲んでください。"
)
async def random_command(interaction: Interaction, items: Optional[str] = None, file: Optional[Attachment] = None):
    
    This_Bot_Version = botversion
    
    # 引数がNoneの場合、ヘルプを返す
    if items is None and file is None:
        await Argument_is_None_Embed(interaction, This_Bot_Version)
        return
    
    value = await None_Check_Process(interaction, items, file)
    
    if value:
        run_result, choice_embed = await Running_Random_Choice(value, This_Bot_Version)
        if run_result == "Success":
            await Success_Embed_Send(interaction, choice_embed)
            print("Random Command Run Success.")
        elif run_result == "ValueError":
            await ve_Embed(interaction, choice_embed)
            print("Value Error.")
        elif run_result == "Error":
            await Unknown_Error(interaction, choice_embed)
            print("Unknown Error...")
        else:
            await interaction.send_message("なんでこのエラーが出るんですかねぇ")
    else:
        await interaction.send_message("なんでこのエラーが出るのかまじでわからんなぁ")
        return
        



# 環境変数
token = os.getenv('bot_token')
if token is None:
    print('bot_token is not set')
else:
    bot.run(token)
