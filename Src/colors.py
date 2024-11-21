import re

DEFAULT = '\x1b[39m'
BLACK = '\x1b[30m'
RED = '\x1b[31m'
LIGHT_RED = '\x1b[91m'
GREEN = '\x1b[32m'
LIGHT_GREEN = '\x1b[92m'
YELLOW = '\x1b[33m'
LIGHT_YELLOW = '\x1b[93m'
BLUE = '\x1b[34m'
LIGHT_BLUE = '\x1b[94m'
MAGENTA = '\x1b[35m'
LIGHT_MAGENTA = '\x1b[95m'
CYAN = '\x1b[36m'
LIGHT_CYAN = '\x1b[96m'
WHITE = '\x1b[38;2;%d;%d;%dm' % (200, 200, 200)
LIGHT_WHITE = '\x1b[97m'
LIGHT_GRAY = '\x1b[37m'
DARK_GRAY = '\x1b[90m'
RESET = '\x1b[0m'

BOLD = '\033[1m'
UNDERLINED = '\033[4m'
STRIKETHROUGH = '\033[9m'
REVERSED = '\033[7m'


def colors_test():
    print(f"{DEFAULT}DEFAULT{RESET}\n"
          f"{BLACK}BLACK{RESET}\n"
          f"{RED}RED{RESET} · "
          f"{LIGHT_RED}LIGHT_RED{RESET}\n"
          f"{GREEN}GREEN{RESET} · "
          f"{LIGHT_GREEN}LIGHT_GREEN{RESET}\n"
          f"{YELLOW}YELLOW{RESET} · "
          f"{LIGHT_YELLOW}LIGHT_YELLOW{RESET}\n"
          f"{BLUE}BLUE{RESET} · "
          f"{LIGHT_BLUE}LIGHT_BLUE{RESET}\n"
          f"{MAGENTA}MAGENTA{RESET} · "
          f"{LIGHT_MAGENTA}LIGHT_MAGENTA{RESET}\n"
          f"{CYAN}CYAN{RESET} · "
          f"{LIGHT_CYAN}LIGHT_CYAN{RESET}\n"
          f"{WHITE}WHITE{RESET} · "
          f"{LIGHT_WHITE}LIGHT_WHITE{RESET}\n"
          f"{LIGHT_GRAY}LIGHT_GRAY{RESET} · "
          f"{DARK_GRAY}DARK_GRAY{RESET}\n"
          f"{BOLD}BOLD{RESET} NOTBOLD\n"
          f"{UNDERLINED}UNDERLINED{RESET}\n"
          f"{REVERSED}REVERSED{RESET}\n"
          f"{STRIKETHROUGH}STRIKETHROUGH{RESET}")


def remove_colors(text):
    pattern = re.compile(
        r'(\x1b\[39m|\x1b\[30m|\x1b\[31m|\x1b\[91m|\x1b\[32m|\x1b\[92m|'
        r'\x1b\[33m|\x1b\[93m|\x1b\[34m|\x1b\[94m|\x1b\[35m|\x1b\[95m|'
        r'\x1b\[36m|\x1b\[96m|\x1b\[38;2;\d+;\d+;\d+m|\x1b\[97m|'
        r'\x1b\[37m|\x1b\[90m|\x1b\[0m|\033\[1m|\033\[4m|\033\[9m|\033\[7m)'
    )

    return pattern.sub('', text)

def print_all_colors(text="Hello, colorful world!", step=10):
    for r in range(0, 256, step):  # Красный канал
        for g in range(0, 256, step):  # Зеленый канал
            for b in range(0, 256, step):  # Синий канал
                color_code = '\x1b[38;2;%d;%d;%dm' % (r, g, b)

                # Формируем строку с текстом и значениями цвета
                color_info = f"RGB ({r}, {g}, {b})"

                # Выводим текст с цветом и информацией о цвете
                print(f"{color_info.ljust(20)} {color_code} {text}{WHITE}")
