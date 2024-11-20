from datetime import datetime
import json
import sys
import os
import requests

# Read perm.json
def load_permissions():
    if not os.path.exists('perm.json'):
        return {}
    with open('perm.json', 'r', encoding='UTF-8') as f:
        data = json.load(f)
        return data
    
# Write perm.json
def save_permissions(permissions):
    with open('perm.json', 'w', encoding='UTF-8') as f:
        json.dump(permissions, f, ensure_ascii=False, indent=4)
        
# Read blacklist.json
def load_blacklist():
    try:
        with open('blacklist.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Write blacklist.json
def save_blacklist(blacklist):
    with open('blacklist.json', 'w') as f:
        json.dump(blacklist, f, indent=4)

# Read commands.json
def load_commands_json():
    if not os.path.exists('commands.json'):
        return {}
    with open('commands.json', 'r', encoding='UTF-8') as f:
        return json.load(f)
    
# convからの移植
def convert_link(original_url):
    if original_url.startswith("https://x.com/") or original_url.startswith("https://twitter.com/"):
        return original_url.replace("https://x.com/", "https://fxtwitter.com/").replace("https://twitter.com/", "https://fxtwitter.com/")
    return original_url
def log_conversion(user, original_url, converted_url):
    try:
        convtime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        with open("convlog.txt", "a") as log_file:
            log_file.write(f"User: {user.name}, {user.id}\n")
            log_file.write(f"Time at: {convtime}\n")
            log_file.write(f"From: {original_url}\n")
            log_file.write(f"To: {converted_url}\n\n")
            print(f"User: {user.name}\nTime at: {convtime}\nFrom: {original_url}\nTo: {converted_url}")
    except Exception as e:
        print(f"An error occurred while logging conversion: {e}")


def get_python_version():
    # Pythonバージョンを取得
    return sys.version
def get_current_directory():
    # カレントディレクトリを取得
    return os.getcwd()
def is_virtual_env():
    # 仮想環境かどうかを確認
    return sys.prefix != sys.base_prefix

#バージョンの情報を取得
def fetch_version_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # JSONデータの値を順に取り出し、リストに変換
        version_info_list = [data[key] for key in sorted(data.keys(), key=int)]
        
        # 改行して結合し、文字列として返す
        return "\n".join(version_info_list)

    except requests.exceptions.RequestException as e:
        print("バージョン情報の取得に失敗しました:", e)
        return None