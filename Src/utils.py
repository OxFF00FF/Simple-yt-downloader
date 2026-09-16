import json
import os
import shutil
import subprocess
import sys
import datetime
from yt_dlp import YoutubeDL as YoutubeDLP

from Src.colors import *
from Src.logging_config import logger


def check_ffmpeg():
    _ffmpeg_path_ = None
    try:
        _ffmpeg_path_ = shutil.which("ffmpeg")
        result = subprocess.run([_ffmpeg_path_, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logger.info(f"System FFmpeg executable: `{_ffmpeg_path_}`")
            return _ffmpeg_path_

    except:
        try:
            _ffmpeg_path_ = os.path.join(os.path.dirname(__file__), 'Bin', 'ffmpeg.exe')
            result = subprocess.run([_ffmpeg_path_, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                logger.info(f"Local FFmpeg executable: `{_ffmpeg_path_}`")
                return _ffmpeg_path_

        except:
            logger.error(f"FFmpeg не установлен в системе и не найден по пути: `{_ffmpeg_path_}`")
            logger.warning("Скачайте и установите FFmpeg с официального сайта: `https://www.ffmpeg.org/download.html` или поместите `ffmpeg.exe` в папку `Src/Bin`")
            sys.exit()


user_profile = os.path.expandvars("%userprofile%")
user_downloads_dir = os.path.join(user_profile, 'downloads')
output_dir = os.path.join(user_downloads_dir, 'YouTube')
ffmpeg_path = check_ffmpeg()


def draw_art(text):
    art = ""
    width = len(text) + 6  # Учитываем отступы и символы вокруг текста
    art += ('┎' + ' ' * (width - 3) + '┒\n')
    art += f'  {text} \n'
    art += ('┖' + ' ' * (width - 3) + '┚\n')
    return art


def check_dirs():
    if not os.path.exists(f"{output_dir.split('/')[0]}"):
        os.mkdir(f"{output_dir.split('/')[0]}")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)


def validate_url(url: str) -> str:
    pattern = re.compile(r"(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)([a-zA-Z0-9_-]{11})", re.VERBOSE)
    match = pattern.search(url)

    if match:
        video_ID = match.group(1).strip()
        return f"https://www.youtube.com/watch?v={video_ID}"


def get_file_size(bytes_count: int) -> str:
    if bytes_count:
        if bytes_count > 0:
            if bytes_count < 1024:
                return f"{bytes_count} Байт"
            elif 1024 <= bytes_count < 1024 ** 2:
                return f"{bytes_count / 1024:.2f} Кб"
            elif 1024 ** 2 <= bytes_count < 1024 ** 3:
                return f"{bytes_count / 1024 ** 2:.2f} Мб"
            elif 1024 ** 3 <= bytes_count < 1024 ** 4:
                return f"{bytes_count / 1024 ** 3:.2f} Гб"


def video_info(url: str) -> tuple:
    check_dirs()
    valid_url = validate_url(url)

    options = {'quiet': True, 'ffmpeg_location': ffmpeg_path}
    with YoutubeDLP(options) as ydl:
        info = ydl.extract_info(valid_url, download=False)

        title = info.get('title')
        webpage_url = info.get('webpage_url')
        video_id = info.get('display_id')

        duration = int(info.get('duration'))
        formatted_time = f"{duration // 60}:{duration % 60} мин. [{str(datetime.timedelta(seconds=duration)).zfill(8)}]"
        print(f"\n"
              f"🏷️  {BOLD}{title}{RESET}{WHITE} \n"
              f"🌐  {webpage_url}\n"
              f"⏳  {formatted_time}\n")

    formats = formats_list(info)
    print(f"{LIGHT_YELLOW}ℹ️  Доступные форматы для скачивания:{WHITE}")
    for n, item in enumerate(formats, start=1):
        print(item['button_text'])

    numbers = '/'.join(str(n) for n in range(1, len(formats) + 1))
    choosen_format = input(f"\n{LIGHT_BLUE}▶️  Укажите номер формата ({LIGHT_WHITE}{numbers}{LIGHT_BLUE}){WHITE}: ")

    try:
        index = int(choosen_format) - 1
        f_code = formats[index].get('format_code')
        f_note = formats[index].get('format_note')
        print(f"{LIGHT_YELLOW}ℹ️  Вы выбрали формат: {WHITE}{f_note} / {f_code}{DARK_GRAY}\n")
        return f_code, title, video_id

    except (ValueError, IndexError):
        print("🚫  Некорректный выбор! Пожалуйста, укажите номер из списка.")
        sys.exit(1)


def formats_list(info) -> list:
    if type(info) is not dict:
        info = json.loads(info)

    all_formats = {}
    for format_ in info.get('formats', []):
        ext = format_.get('ext')
        format_id = format_.get('format_id')
        V_codec = format_.get('vcodec')
        A_codec = format_.get('acodec')
        format_note = format_.get('format_note')

        if ext in {'mp4', 'm4a'}:
            filesize = get_file_size(format_.get('filesize', 0))

            if filesize:
                if V_codec == 'none':
                    all_formats['audio'] = f"🚫 🔊/audio/{filesize}/{ext}/{format_id}/audio"
                else:
                    frame_size = f"{format_.get('width')}x{format_.get('height')}"
                    if A_codec == 'none':
                        all_formats[frame_size] = f"🎬 🔇/{frame_size}/{filesize}/{ext}/{format_id}/{format_note}"
                    else:
                        all_formats[frame_size] = f"🎬 🔊/{frame_size}/{filesize}/{ext}/{format_id}/{format_note} "

    result = []
    for index, v in enumerate(all_formats.values(), start=1):
        emoji = v.split('/')[0]
        frame_size = v.split('/')[1]
        filesize = v.split('/')[2]
        ext = v.split('/')[3]
        format_code = v.split('/')[4]
        format_note = v.split('/')[5]

        filesize_text = f"💾 「{WHITE}{BOLD}{filesize}{RESET}{YELLOW} 」"
        if format_note == 'audio':
            f_code = format_code
            frame_size_text = f'🔊 「{frame_size} 」'.ljust(15).replace('🔊 「', f"{YELLOW}🔊 「{WHITE}{BOLD}").replace(' 」', f"{RESET}{YELLOW} 」")
        else:
            f_code = f"{format_code}+bestaudio[ext=m4a]"
            frame_size_text = f'🎬 「{frame_size} 」 '.ljust(15).replace('🎬 「', f"{YELLOW}🎬 「{WHITE}{BOLD}").replace(' 」', f"{RESET}{YELLOW} 」")

        text = f"{frame_size_text} · {filesize_text}"

        result.append({
            "button_text": f"{LIGHT_YELLOW}{index} | {YELLOW}{text}{WHITE}",
            "emoji": emoji,
            "frame_size": frame_size,
            "filesize": filesize,
            "ext": ext,
            "format_code": f_code,
            "format_note": format_note})

    return result
