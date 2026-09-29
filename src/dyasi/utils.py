from beartype import beartype
from colorama import Fore, Style
from typing import Any
from datetime import datetime
from dyasi.exceptions import InvalidLogLevelError

# Logging feature
@beartype
def log(*messages: Any, level: str | None="info") -> None:
    # Determining the log type
    if level.lower() == "info":
        level = Fore.GREEN + Style.BRIGHT + level.upper()
    elif level.lower() == "error":
        level = Fore.RED + Style.BRIGHT + level.upper()
    elif level.lower() == "warn":
        level = "warning"
        level = "\033[38;2;255;215;0m" + Style.BRIGHT + level.upper()
    else:
        raise InvalidLogLevelError("Log level is invalid.")

    # Logging
    log_level = Fore.WHITE + "[" + level + Fore.WHITE + "]" + Style.RESET_ALL
    timestamp = Fore.WHITE + "[" + Fore.CYAN + datetime.now().strftime("%H:%M:%S") + Fore.WHITE + "]" + Style.RESET_ALL
    print(timestamp, log_level, *messages)