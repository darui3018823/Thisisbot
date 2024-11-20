import asyncio
import random
import string
import discord
import os
import subprocess

# 音楽キューとボイスチャンネル接続のグローバル変数
music_queue = []
vc = None
DOWNLOAD_DIR = "./vc/audios/"


