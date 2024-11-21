import sys

from banner import create_banner

from colors import *
from crop_video import download_partial_video
from full_video import video_info, download_video
from logging_config import logger

if __name__ == '__main__':
    # standard, slant, pepper, cybermedium, ansi_shadow
    create_banner([['Yt', f"{BOLD}{LIGHT_RED}"], ['DL', f"{BOLD}{WHITE}"]], font='standard', show=True)

    try:
        input_url = input(f"{LIGHT_BLUE}▶️  Вставьте ссылку на YouTube видео: {WHITE}")
        _format, title, video_id = video_info(input_url)

        print(f'{LIGHT_YELLOW}ℹ️  Как нужно скачать видео? ({BOLD}{WHITE}1 - полностью / 2 - отрывок{RESET}{LIGHT_YELLOW}){WHITE}')
        choose_type = input(f"{LIGHT_BLUE}▶️  Выберите вариант ({WHITE}1/2{LIGHT_BLUE}): {WHITE}")

        if choose_type == '1':
            download_video(input_url, _format)

        elif choose_type == '2':
            print(f'\n{LIGHT_YELLOW}ℹ️  Выберите начало и конец обрезки в формате: hh:mm:ss. Например: 00:01:20, 01:25:02, 00:00:05{WHITE}')
            input_crop = input(f"{LIGHT_BLUE}▶️  Начало обрезки: {WHITE}")
            output_crop = input(f"{LIGHT_BLUE}▶️  Конец обрезки:  {WHITE}\n")
            download_partial_video(input_url, _format, input_crop, output_crop, title, video_id)

        else:
            logger.warning('Такого варианта ответа нет!')
            sys.exit()

    except Exception as e:
        logger.error(e)
