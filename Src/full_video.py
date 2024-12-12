import os

from yt_dlp import YoutubeDL as YoutubeDLP

from colors import *
from logging_config import logger
from utils import output_dir, ffmpeg_path, check_dirs, validate_url

os.system("")


def download_full_video(url: str, format_code=None) -> str:
    """
    :param url: Ссылка на видео на YouTube
    :param format_code: Код формата video+audio
    :return: Возвращает путь до скачанного файла
    """
    check_dirs()
    url = validate_url(url)

    options = {
        'outtmpl': f'{output_dir}/%(title)s [%(display_id)s].%(ext)s',
        'noplaylist': True,
        'format': format_code,
        'ffmpeg_location': ffmpeg_path
    }

    with YoutubeDLP(options) as ydl:
        ydl.download([url])

        files = os.listdir(output_dir)
        if files:
            translation_table = str.maketrans('', '', '/\\:*?"<>|')
            valid_filename = files[0].translate(translation_table)

            output = os.path.join(output_dir, valid_filename)
            os.startfile(output_dir)

        logger.info(f"{WHITE}File saved to: `{output}` ")
        return output
