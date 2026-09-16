import sys
from os import getenv
from pathlib import Path
from shutil import which, copy2
from subprocess import Popen
from tempfile import mkdtemp
from typing import Literal


def run_in_terminal(
        title: str = 'PythonApp',
        terminal_type: Literal['cmd', 'ps'] = 'ps',
        launch_type: Literal['wt', 'pyi'] | None = 'wt',
        profile_name=None
):
    """
    Запускает текущий скрипт Python в отдельной сессии Windows Terminal

    Если launch_type не указан и скрипт не заморожен через PyInstaller — функция ничего не делает.

    :param title: Заголовок вкладки терминала. По умолчанию 'PythonApp'.
    :param terminal_type: Тип терминала. Команданая строка ('cmd') или Powershell ('ps').
    :param launch_type: Тип запуска. При сборке exe файла указать 'pyi', чтобы при запуске exe файла открывался WT.
    :param profile_name: Название профиля WT
    """
    if not launch_type:
        # обычный режим: WT не нужен
        # if not getattr(sys, 'frozen', False):
        #     return
        return

    if getenv("WT_SESSION"):
        # Если уже в wt, то выходим
        return

    wt_path = which("wt.exe")
    if not wt_path:
        raise RuntimeError("Windows Terminal not found")

    interpreter_path = str(Path(sys.executable).resolve())
    script_path = str(Path(sys.argv[0]).resolve())

    profile = (
            profile_name
            or {
                'cmd': 'Командная строка',
                'ps': 'Windows PowerShell',
            }.get(terminal_type)
    )

    tab_title = f'{title} ({profile_name})' if profile_name else title

    if launch_type == 'pyi':
        temp_dir = mkdtemp(prefix="PythonApp_")
        temp_exe = Path(temp_dir) / Path(sys.executable).name
        copy2(interpreter_path, temp_exe)
        interpreter_path = temp_exe

    command = [wt_path, '-w', '0', 'new-tab', '-p', profile, '--title', tab_title, interpreter_path, script_path]
    Popen(command)
    raise SystemExit(0)
