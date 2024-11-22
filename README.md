# This is bot Source Codes!
<br>
気分で消します。ははは<br>
Releasesは編集しながらコード一部編集を行っているのでLatestが上に来ることはあんまないです。<br>
確認をお願いしますね
<br>


## 目次
- [概要](#概要)
- [インストール方法](#インストール方法)
- [使い方](#使い方)
- [設定](#設定)
- [機能一覧](#機能一覧)
- [ライセンス](#ライセンス)
- [問い合わせ](#問い合わせ)
- [関連ファイル](#関連ファイル)
- [最終更新日](#最終更新日)

<br>

## 概要
このボットはPython Runnerや絶対パスを指定して実行するなど、多様な用途をWindows上で実行可能です。<br>
macOSには一部対応していない可能性がありますので、開発環境の問題についてご了承ください。<br><br>

## インストール方法
以下のリンクを参照して、venvを利用してください。<br>
[venvのダウンロード](https://github.com/darui3018823/Thisisbot/releases/download/2.3.2/venv_3.12.7.zip)<br>
<br>
venvを使わない場合は以下をコマンドプロンプトにて実行してください。<br>
確実に可能だとわかっているのはPython [3.12.7](https://www.python.org/downloads/release/python-3127/)です。<br>
`pip install discord httpcore ipinfo pytz requests googletrans psutil wmi Pillow GPUtil selenium`<br>

## 使い方
コードは私自身の使用を目的としているため、至らない点がございましたらご指摘いただけると幸いです。<br>
特にユーザーIDや絶対パスはご自身の環境に合わせて編集してご利用ください。<br>

`Drivers`フォルダには以下のファイルが含まれていますので、こちらをご利用ください：
- `geckodriver.exe`
- `yt-dlp.exe`

`ffmpeg`も必要ですが、こちらについては以下のリンクをご参照ください：
[ffmpegのダウンロード](https://bot.daruks.com/thisisbot/ffmpeg/)

## 設定
必要な箇所（UserIDやドライバー等の絶対・相対パスなど）を適宜編集してご利用ください。

## 機能一覧
Discord上で以下のコマンドを実行していただければと思います：
- `/cmdlist all`

## ライセンス
このプロジェクトは [GNU General Public License v3](https://github.com/darui3018823/Thisisbot/blob/main/LICENSE) の下で提供されています。  
GPLv3に基づき、以下の条件が適用されます。

1. **改変について**  
   - このソフトウェアは自由に改変することができますが、改変箇所によっては予期しない動作や不具合が発生する可能性があります。特に、以下のファイルや設定を改変する場合は十分にご注意ください:
     - その他重要な内部設定
   - 推奨される改変箇所:
     - バッチファイル (`.bat`)
     - ボットのプレフィックス設定
     - ユーザーIDやドライバーの絶対・相対パス

2. **再配布について**  
   - 再配布時は、GPLv3の条項に基づきソースコードを含めて公開してください。
   - 変更を加えた場合は、その旨を明記し、変更後のソースコードを公開する必要があります。

3. **クレジットの表記**  
   - 著作者である「darui3018823」のクレジットを削除しないでください。
   - プロジェクトの公式GitHubリポジトリ（[このリンク](https://github.com/darui3018823/Thisisbot)）を共有してください。

4. **注意事項**  
   - 改変したコードや設定によって生じた問題について、作者は一切の責任を負いません。
   - 詳細な使用条件や免責事項については、[Terms-of-Service.md](./Terms-of-Service.md) をご確認ください。

## 問い合わせ
ご意見やご質問、その他すべてのお問い合わせについては、以下のいずれかの方法でご連絡ください：
- メール: contact@daruks.com
- ホームページ: [https://daruks.com/contact](https://daruks.com/contact)
- Twitter: [@darui3018823](https://twitter.com/darui3018823)
- Discord:
  - This is botに`daruks!contact`を送信し、手順に沿ってお進みください。
  - @darui3018823まで直接お問い合わせください。

サポートは全てのバージョンで行いますが、2.0以前のバージョンに関するIssueは一切受け付けることができません。<br>
最大限受けられるためにも、2.3.1以上のバージョンのご利用を推奨いたします。<br>
<br>
MITライセンスなどの特定の記載がある場合を除き、README.mdの最終更新日より効力が発生します。<br>
<br>

## 関連ファイル
- [利用規約](https://github.com/darui3018823/Thisisbot/blob/main/Terms-of-Service.md)
- [プライバシーポリシー](https://github.com/darui3018823/Thisisbot/blob/main/Privacy-Policy.md)
- [GNU General Public License v3.0](https://github.com/darui3018823/Thisisbot/blob/main/LICENSE)
- [サポートバージョン](https://github.com/darui3018823/Thisisbot/blob/main/Support-Status.md)
<br>

## 最終更新日
2024/11/22 10:50
