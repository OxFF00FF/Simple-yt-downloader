from pyfiglet import parse_color, figlet_format

from colors import *


def get_figlet_text(text, font=None, colors=":", **kwargs):
    ansi_colors = parse_color(colors)
    figlet_text = figlet_format(text, font, **kwargs)

    RESET_COLORS = b'\033[0m'
    if ansi_colors:
        figlet_text = ansi_colors + figlet_text + RESET_COLORS.decode('UTF-8', 'replace')

    return figlet_text


def create_banner(words_and_colors, font='standard', show=False):
    # Список, который будет содержать строки для каждого текста, с добавленными цветами.
    lines = []
    result = ""

    for (text, color) in words_and_colors:
        # Создание ASCII арта для каждого слова из переданного списка
        ascii_art_word = get_figlet_text(text, font=font, width=200)

        # Разделение арта на список линий
        word_lines = ascii_art_word.splitlines()

        # Красим каждую линию и добавляем в список
        lines.append([
            color + word_line
            for word_line
            in word_lines
        ])

    # Объединяем каждую строку из каждой группы (из разных артов) в одну строку
    for line_group in zip(*lines):
        result += "  ".join(line_group) + "\n"

    if show:
        print(f"\n{result}{RESET}{WHITE}")

    return result
