import random
import re
import shlex
import discord
import random


async def Argument_is_None_Embed(interaction, This_Bot_Version):
    
    Text_Help_Message = [
        "itemsの中に選択したいものを半角スペースで区切って入れてください。",
        "`/random items: aa bb c ddd`",
        "もし、入れるものにスペースが含まれている場合はダブルクォーテーションを使い囲んでください。",
        '`/random items: aa bb c "dd d"`'
    ]
    
    File_Help_Message = [
        "fileに必要なファイルを添付して送信してください。",
        "`/random file: YourFile`",
        "拡張子が`.txt`のみ対応しています。",
        "`.json`には今後対応予定です。",
        "アイテムの区切り等はitemsと同じです。"
    ]
    
    detail_Need_Help = [
        "上記で解決できない場合、または詳細なサポートが必要な場合は",
        "botとのdmチャンネルで`daruks!contact`を送信してください。"
    ]
    
    # Make Embed
    embed = discord.Embed(
        color=0xffff00,
        title="Random Command Help!",
        description="コマンドのヘルプです。"
    )
    
    embed.add_field(name="テキスト入力の場合", value="\n".join(Text_Help_Message), inline=False)
    embed.add_field(name="ファイルの場合", value="\n".join(File_Help_Message), inline=False)
    embed.add_field(name="詳細なヘルプ", value="\n".join(detail_Need_Help), inline=False)
    embed.set_footer(text=This_Bot_Version)
    
    await interaction.response.send_message(embed=embed)
    
async def None_Check_Process(interaction, items, file):
    
    choices = []

    if file is not None:
        # ファイルを非同期で読み込む
        content = await file.read()
        
        # UTF-8でデコード
        content_str = content.decode('utf-8')

        # 正規表現で単語を取得
        # ダブルクォーテーションで囲まれた単語と、スペースで区切られた単語を認識
        choices = re.findall(r'"([^"]+)"|(\S+)', content_str)

        # choicesをフラットにし、空の要素を除外する
        choices = [item for sublist in choices for item in sublist if item]
        print(choices)
    elif items is not None:
        # Text Type
        choices = shlex.split(items)
    
    return choices

async def Running_Random_Choice(value, This_Bot_Version):
    try:
        Items = value
        if not Items:
            raise ValueError("アイテムリストが空です。") #以降の処理をすっ飛ばす
        
        Choice_Result = random.choice(Items)

        embed = discord.Embed(
            title="Random Choice",
            color=0x696969
        )
        
        embed.add_field(name="Choice Result", value=Choice_Result, inline=False)
        embed.set_footer(text=This_Bot_Version)
        
        return "Success", embed

    except ValueError as ve:
        # ValueErrorが発生した場合の処理
        embed = discord.Embed(
            title="エラー",
            color=0xff0000
        )
        embed.add_field(name="Item_List_Error", value=str(ve), inline=False)
        embed.set_footer(text=This_Bot_Version)
        return "ValueError", embed
    except Exception as e:
        embed = discord.Embed(
            title="エラー",
            color=0xff0000
        )
        embed.add_field(name="予期しないエラー", value=str(e), inline=False)
        embed.set_footer(text=This_Bot_Version)
        return "Error", embed

async def Success_Embed_Send(interaction, choice_embed):
    await interaction.response.send_message(embed=choice_embed)
    
async def ve_Embed(interaction, choice_embed):
    await interaction.responce.send_message(embed=choice_embed)
    
async def Unknown_Error(interaction, choice_embed):
    await interaction.responce.send_message(embed=choice_embed)