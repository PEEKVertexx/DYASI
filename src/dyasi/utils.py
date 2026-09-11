from beartype import beartype
from colorama import Fore, Style
from typing import Any
from datetime import datetime

# Logging feature
@beartype
def log(*messages: Any, type: str | None="info"):
    # Determining the log type
    if type == "info":
        type = Fore.GREEN + Style.BRIGHT + type.upper()
    elif type == "error":
        type = Fore.RED + Style.BRIGHT + type.upper()
    elif type == "warn":
        type = "warning"
        type = "\033[38;2;255;215;0m" + Style.BRIGHT + type.upper()

    # NOTE for me: cleanize the feature

    # Logging
    log_type = Fore.WHITE + "[" + type + Fore.WHITE + "]" + Style.RESET_ALL
    timestamp = Fore.WHITE + "[" + Fore.CYAN + datetime.now().strftime("%H:%M:%S") + Fore.WHITE + "]" + Style.RESET_ALL
    print(timestamp, log_type, *messages)

log("test", type="warn")