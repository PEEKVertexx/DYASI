from beartype import beartype
from colorama import Fore, Style
from typing import Any
from datetime import datetime
from dyasi.exceptions import InvalidLogLevelError

# Logging feature
@beartype
def log(*messages: Any, level: str | None="info") -> None:
    # Defining the level aliases
    INFO_ALIASES = ["INFO", "I"]
    ERROR_ALIASES = ["ERROR", "ERR", "E"]
    WARNING_ALIASES = ["WARN", "WARNING", "W"]

    # Space trippig the level
    level = level.strip().upper()

    # Determining the log type
    if level in INFO_ALIASES:
        level = "INFO" if level != "INFO" else level
        
        level = Fore.GREEN + Style.BRIGHT + level
    elif level in ERROR_ALIASES:
        level = "ERROR" if level != "ERROR" else level

        level = Fore.RED + Style.BRIGHT + level
    elif level in WARNING_ALIASES:
        level = "WARNING" if level != "WARNING" else level

        level = "\033[38;2;255;215;0m" + Style.BRIGHT + level
    else:
        raise InvalidLogLevelError("Log level is invalid.")

    # Logging
    log_level = Fore.WHITE + "[" + level + Fore.WHITE + "]" + Style.RESET_ALL
    timestamp = Fore.WHITE + "[" + Fore.CYAN + datetime.now().strftime("%H:%M:%S") + Fore.WHITE + "]" + Style.RESET_ALL
    print(timestamp, log_level, *messages)