import os
import subprocess
import sys
from datetime import datetime

import humanize as humanize

from colors import *
from logging_config import logger


def download_partial_video(url: str, format_code, input_crop: str = None, output_crop: str = None, title: str = None, video_id=None):
    """
    Скачивает часть видео с YouTube с помощью yt-dlp и ffmpeg.
    Принимает URL видео (https://www.youtube.com/watch?v=<video_id>)
    И временные метки в формате hh:mm:ss

    :param title:
    :param video_id:
    :param format_code:
    :param input_crop: Начальная метка
    :param output_crop: Конечная метка
    :param url: Ссылка на видео на YouTube.
    """
    i, o = input_crop.replace(':', '-'), output_crop.replace(':', '-')

    try:
        time_format = "%H:%M:%S"
        input_time = datetime.strptime(input_crop, time_format)
        output_time = datetime.strptime(output_crop, time_format)

        delta_time = output_time - input_time

        start_time = str(input_time).split()[-1]
        end_time = str(output_time).split()[-1]

        humanize.i18n.activate("ru_RU")
        duration = humanize.precisedelta(delta_time)
        humanize.i18n.deactivate()

        if output_time < input_time:
            logger.error("Ошибка указания времени. Начальная метка времени должна быть меньше конечной!")
            sys.exit()

        if output_time == input_time:
            logger.error("Ошибка указания времени. Начальная и конечная метка времени не могут быть равны!")
            sys.exit()

    except Exception as e:
        logger.error(f'Не удалось преобразовать временные метки в дату: {LIGHT_RED}{e}{WHITE}!')
        sys.exit()

    user_profile = os.path.expandvars("%userprofile%")
    user_downloads_dir = os.path.join(user_profile, 'downloads')
    output_dir = os.path.join(user_downloads_dir, 'YouTube')

    # yt_dlp_command = [
    #     "yt-dlp",
    #     "--quiet",                      # Отключает логи yt-dlp
    #     "--print", "%(title)s",         # Вывод названия
    #     "--print", "%(display_id)s",    # Вывод идентификатора
    #     url
    # ]
    # result = subprocess.run(yt_dlp_command, capture_output=True, text=True, encoding="utf-8")
    # title, video_id = result.stdout.splitlines()

    filename = f"[{i}__{o}] {title} ({video_id}).mp4"
    translation_table = str.maketrans('', '', '/\\:*?"<>|')
    valid_filename = filename.translate(translation_table)

    output = f'"{os.path.join(output_dir, valid_filename)}"'
    try:
        logger.info(f"Информация о видео получена. Скачиваем отрывок {LIGHT_YELLOW}{duration}{WHITE} [{CYAN}{start_time} - {end_time}{WHITE}]")

        yt_dlp_ffmpeg_command = [
            "yt-dlp",
            "--quiet",              # Отключает логи yt-dlp
            "-f", format_code,      # Выбор формата (format_id Видео + лучшее аудио в формате m4a)
            url,                    # Ссылка на видео
            "-o", "-",              # Вывод видео в stdout
            "|",                    # Перенаправлят вывод из stdout в ffmpeg
            "ffmpeg",               # ffmpeg читает эти данные с помощью параметра -i -
            "-hide_banner",         # Скрывает информационное сообщение
            "-loglevel", "quiet",   # Отключает логи ffmpeg
            # "-hwaccel", "auto",     # Использование аппаратного ускорения
            "-ss", input_crop,      # Начало обрезки
            "-to", output_crop,     # Конец обрезки
            "-i", "-",              # Входной поток из yt-dlp
            "-map", "0:v",          # Выбирает видеопоток из первого входного файла.
            "-map", "0:a",          # Выбирает аудиопоток из первого входного файла.
            "-c:v", "libx264",      # Перекодируем видео в H.264
            "-crf", "23",           # Качества видео для кодека H.264 (0-51). Лучшее соотношение размера и сжатия (28/23/18)
            "-c:a", "aac",          # Перекодируем звук в aac
            "-y", output            # Куда сохраняется обрезанный файл
        ]
        subprocess.run(" ".join(yt_dlp_ffmpeg_command), shell=True, check=True)
        logger.info(f"{LIGHT_GREEN}Видео сохранено по пути: {output}{WHITE}")

    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка при выполнении команды: {e}")
