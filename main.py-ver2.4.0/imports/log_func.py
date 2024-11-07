# Log.txt
from datetime import datetime


def log_command(user, keyword=None, full_path=None, channel_id=None):
    with open('log.txt', 'a', encoding='UTF-8') as f:
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_info = f"User: {user.name}, {user.id}"
        if keyword:
            running_info = f"Running Path: {keyword}"
        elif full_path:
            running_info = f"Running Path: {full_path}"
        else:
            running_info = "Running Path: None"

        # チャンネルIDが提供されていればそれを使用し、提供されていなければ "dm" とする
        if channel_id:
            run_place = f"Run place: {channel_id}"
        else:
            run_place = "Run place: dm"

        f.write(f"RunTime: {log_time}\n{user_info}\n{running_info}\n{run_place}\n\n")