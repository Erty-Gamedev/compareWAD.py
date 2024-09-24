from typing import Final
import os

os.system('color')


RESET: Final[str] =         '\033[0m'
BOLD: Final[str] =          '\033[1m'
DIM: Final[str] =           '\033[2m'
ITALIC: Final[str] =        '\033[3m'
UNDERLINE: Final[str] =     '\033[4m'
BLINKING: Final[str] =      '\033[5m'
REVERSE: Final[str] =       '\033[7m'
HIDDEN: Final[str] =        '\033[8m'
STRIKETHROUGH: Final[str] = '\033[9m'

FGBLACK: Final[str] =           '\033[30m'
FGRED: Final[str] =             '\033[31m'
FGGREEN: Final[str] =           '\033[32m'
FGYELLOW: Final[str] =          '\033[33m'
FGBLUE: Final[str] =            '\033[34m'
FGMAGENTA: Final[str] =         '\033[35m'
FGCYAN: Final[str] =            '\033[36m'
FGWHITE: Final[str] =           '\033[37m'
FGBRIGHT_BLACK: Final[str] =    '\033[90m'
FGBRIGHT_RED: Final[str] =      '\033[91m'
FGBRIGHT_GREEN: Final[str] =    '\033[92m'
FGBRIGHT_YELLOW: Final[str] =   '\033[93m'
FGBRIGHT_BLUE: Final[str] =     '\033[94m'
FGBRIGHT_MAGENTA: Final[str] =  '\033[95m'
FGBRIGHT_CYAN: Final[str] =     '\033[96m'
FGBRIGHT_WHITE: Final[str] =    '\033[97m'

BGBLACK: Final[str] =            '\033[40m'
BGRED: Final[str] =              '\033[41m'
BGGREEN: Final[str] =            '\033[42m'
BGYELLOW: Final[str] =           '\033[43m'
BGBLUE: Final[str] =             '\033[44m'
BGMAGENTA: Final[str] =          '\033[45m'
BGCYAN: Final[str] =             '\033[46m'
BGWHITE: Final[str] =            '\033[47m'
BGBRIGHT_BLACK: Final[str] =    '\033[100m'
BGBRIGHT_RED: Final[str] =      '\033[101m'
BGBRIGHT_GREEN: Final[str] =    '\033[102m'
BGBRIGHT_YELLOW: Final[str] =   '\033[103m'
BGBRIGHT_BLUE: Final[str] =     '\033[104m'
BGBRIGHT_MAGENTA: Final[str] =  '\033[105m'
BGBRIGHT_CYAN: Final[str] =     '\033[106m'
BGBRIGHT_WHITE: Final[str] =    '\033[107m'


def styleError(s: str, bold: bool = True) -> str:
    return f"{BOLD if bold else ''}{FGRED}{s}{RESET}"

def styleWarning(s: str, bold: bool = False) -> str:
    return f"{BOLD if bold else ''}{FGYELLOW}{s}{RESET}"

def styleInfo(s: str, bold: bool = False) -> str:
    return f"{BOLD if bold else ''}{FGCYAN}{s}{RESET}"

def styleSuccess(s: str, bold: bool = True) -> str:
    return f"{BOLD if bold else ''}{FGGREEN}{s}{RESET}"

def styleMuted(s: str) -> str:
    return f"{FGBRIGHT_BLACK}{s}{RESET}"

def styleAdded(s: str, strikethrough=False) -> str:
    return f"{STRIKETHROUGH if strikethrough else ''}{FGGREEN}{s}{RESET}"

def styleRemoved(s: str, strikethrough=False) -> str:
    return f"{STRIKETHROUGH if strikethrough else ''}{FGRED}{s}{RESET}"

def styleModified(s: str) -> str:
    return f"{FGYELLOW}{s}{RESET}"
