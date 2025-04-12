Copyright (C) 2024-2025 darui3018823

All programs in this repository are licensed under the GPL-3.0 license.

Please see [GPL-3.0 License](https://github.com/darui3018823/Thisisbot?tab=GPL-3.0-1-ov-file)

for details on the license.

<br>

## 📚 Libraries Used / 使用ライブラリ一覧
<details>
<summary>🇯🇵 日本語版（クリックで展開）</summary>
  
本Botは主に `discord.py` ライブラリを利用して構築されています。  
また、以下のライブラリも機能実現のために使用しています。

### 🔧 基本ライブラリ
- `discord.py` – Discord Bot フレームワーク
- `asyncio` – 非同期処理用ライブラリ
- `os`, `subprocess`, `datetime`, `time`, `logging`, `random`, `json`, `typing`, `io` – Python 標準ライブラリ

### 🌐 通信・API関連
- `httpcore` – 低レベルのHTTP通信ライブラリ
- `ipinfo` – IPジオロケーション情報取得API
- `requests` – APIとのHTTP通信

### 🕒 時刻・タイムゾーン関連
- `pytz` – タイムゾーン対応の日時処理

### ⚙️ システム・ハードウェア情報
- `psutil` – CPU・メモリ・プロセスの監視
- `GPUtil` – GPU使用状況の取得
- `wmi` – Windows専用のシステム情報取得（WMI）

### 🧪 開発者向けユーティリティ
- [`jishaku`](https://github.com/scarletcafe/jishaku) – Discord Bot向けのデバッグ支援ライブラリ

### 🌐 ブラウザ操作
- `selenium` – ブラウザ自動操作ライブラリ（Firefox/WebDriver対応）

> 上記のライブラリは、システム監視、コマンド実行、VC操作などの各種機能を支えています。

各ライブラリの著作権および関連する権利は、それぞれの作者・関係者に帰属します。

</details>

<details>
<summary>🇬🇧 English Version (Click to expand)</summary>
  
This bot primarily utilizes the `discord.py` library, along with the following libraries:

### 🔧 Core Libraries
- `discord.py` – Discord bot framework
- `asyncio` – Asynchronous programming
- `os`, `subprocess`, `datetime`, `time`, `logging`, `random`, `json`, `typing`, `io` – Python standard libraries

### 🌐 Networking & API Communication
- `httpcore` – Low-level HTTP networking
- `ipinfo` – IP geolocation and info API
- `requests` – General HTTP request handling

### 🕒 Time and Localization
- `pytz` – Timezone handling for datetime

### ⚙️ System & Hardware Information
- `psutil` – CPU, memory, and process monitoring
- `GPUtil` – GPU utilization tracking
- `wmi` – Windows Management Instrumentation (Windows only)

### 🧪 Developer Utilities
- [`jishaku`](https://github.com/scarletcafe/jishaku) – Developer/debugging tools for Discord bots

### 🌐 Browser Automation
- `selenium` – Web browser automation (Firefox/WebDriver support)

> These libraries support features such as system monitoring, command execution, voice channel interaction, and more.

All copyrights and rights related to these libraries belong to their respective authors and stakeholders.
</details>
<br>

## 🧰 Required Tools & Runtime / 必須ツール・実行環境
<details>
<summary>🇯🇵 日本語版（クリックで展開）</summary>

以下のツールは本プロジェクトにおいて使用されています。  
それぞれの著作権およびライセンスは、各制作者または団体に帰属します。  
これらのツールのライセンスと本ソースコード（GPL-3.0）のライセンスに矛盾がある場合は、  
**各ツールのライセンスが許容する範囲内で**本ソースコードのライセンスが優先されます。

| ツール名       | 用途                                       | 制作者・団体名                       |
|----------------|--------------------------------------------|--------------------------------------|
| [Python 3.12.7](https://www.python.org/)  | 実行環境の基盤となるPython本体               | Python Software Foundation          |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp)         | 動画等の取得に使用するダウンローダー | yt-dlp contributors                 |
| [ffmpeg](https://www.ffmpeg.org/)         | 音声・映像の変換・処理                       | FFmpeg team                         |
| [ffmpeg Windows builds from gyan.dev](https://www.gyan.dev/ffmpeg/builds/)     | ffmpegのWindows向け配布バイナリ                 | Gyan Doshi |
| [GeckoDriver](https://github.com/mozilla/geckodriver)    | FirefoxブラウザをSeleniumで操作するためのWebDriver | Mozilla Foundation                  |

</details>
<details>
<summary>🇬🇧 English Version (Click to expand)</summary>

The following tools are used as part of this project.  
All rights and associated licenses belong to the respective authors or organizations.  
If there are any conflicts between their licenses and the license of this source code (GPL-3.0),  
this source's license will apply **only to the extent permitted by each tool's own license**.

| Tool          | Purpose                                      | Author / Organization               |
|---------------|----------------------------------------------|--------------------------------------|
| Python 3.12.7 | Main runtime environment                     | Python Software Foundation          |
| yt-dlp        | Media downloader for handling online content | yt-dlp contributors                 |
| ffmpeg        | Media processing and conversion              | FFmpeg team                         |
| [ffmpeg Windows builds from gyan.dev](https://www.gyan.dev/ffmpeg/builds/) | Prebuilt binaries for Windows (ffmpeg)       | Gyan Doshi |
| GeckoDriver   | Firefox WebDriver used by Selenium           | Mozilla Foundation                  |

</details>
