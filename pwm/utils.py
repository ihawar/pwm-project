import sys
import os
import platform
from pathlib import Path


if sys.platform.startswith('win'):
    import msvcrt

    def getch():
        return msvcrt.getch()

else:
    import tty
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.buffer.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def get_data_path(app_name="pwm"):
    system = platform.system()

    if system == "Windows":
        base_dir = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA")
    elif system == "Darwin":
        base_dir = os.path.expanduser("~/Library/Application Support")
    else: 
        base_dir = os.path.expanduser("~/.local/share")

    full_path = Path(base_dir) / app_name
    full_path.mkdir(parents=True, exist_ok=True)
    return full_path
