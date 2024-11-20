import discord
from discord.ext import commands
import io
import contextlib
import os
import asyncio
from datetime import datetime

class PythonRunner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def py(self, ctx, *, code_or_file: str = None):
        daruks = [973782871963762698]
        if ctx.author.id not in daruks:
            await ctx.send('このコマンドを実行する権限がありません。')
            return

        code = None

        if len(ctx.message.attachments) > 0:
            # 添付ファイルがある場合
            attachment = ctx.message.attachments[0]
            try:
                file_content = await attachment.read()
                code = file_content.decode('utf-8')
            except UnicodeDecodeError:
                await ctx.send('ファイルのエンコーディングに問題があります。')
                return
            except Exception as e:
                await ctx.send(f'ファイルの読み込み中にエラーが発生しました: {e}')
                return
        elif code_or_file:
            # トリプルバッククオートで囲まれた部分を取り出す
            if code_or_file.startswith('```') and code_or_file.endswith('```'):
                # トリプルバッククオートとその中の言語指定部分を削除
                code = code_or_file.strip('```').split('\n', 1)[-1]
            else:
                code = code_or_file

        if code is None:
            await ctx.send('コードまたはファイルを指定してください。')
            return

        # 実行結果をキャプチャするための出力ストリームを準備
        f = io.StringIO()
        now = datetime.now()
        timestamp = now.strftime('%Y/%m/%d %H:%M')
        log_message = f"Sent Time: {timestamp}\nRun Code: {code}\n"

        # 非同期にコードを実行するタスクを定義
        async def run_code():
            with contextlib.redirect_stdout(f):
                try:
                    # execを使ってコードを実行
                    exec(code, globals())
                except Exception as e:
                    output = f'エラー: {e}'
                    log_message += f'Py Output: {output}\n-----'
                    await ctx.send(f'Python Output:\n{output}')
                    return

        # 非同期タスクを実行
        try:
            await asyncio.wait_for(run_code(), timeout=5.0)  # タイムアウトを設定
        except asyncio.TimeoutError:
            await ctx.send('コードの実行がタイムアウトしました。')

        # 実行結果を取得し、リプライする
        output = f.getvalue()
        log_message += f'Py Output: {output}\n-----'
        print(log_message)

        if len(output) > 100:
            # pylog フォルダを作成する
            pylog_dir = 'C:/Users/user/vsc/fullcode/pylog'  # 絶対パスに変更
            if not os.path.exists(pylog_dir):
                os.makedirs(pylog_dir)

            # 現在の日付と時刻を取得
            now = datetime.now()
            timestamp = now.strftime('%Y%m%d_%H%M%S')
            log_filename = os.path.join(pylog_dir, f'{timestamp}.txt')  # 絶対パスを指定

            # ログファイルに出力を保存
            try:
                with open(log_filename, 'w', encoding='utf-8') as log_file:
                    log_file.write(output)

                # ログファイルを添付
                with open(log_filename, 'rb') as log_file:
                    await ctx.send('出力が長すぎるため、ログファイルを添付します。', file=discord.File(log_file, log_filename))
            except Exception as e:
                await ctx.send(f'ログファイルの保存中にエラーが発生しました: {e}')
        else:
            await ctx.send(f'Python Output:\n{output}')

async def setup(bot):
    await bot.add_cog(PythonRunner(bot))
