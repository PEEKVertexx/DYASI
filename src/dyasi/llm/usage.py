from beartype import beartype
from dataclasses import dataclass
from dyasi.utils import log
from pathlib import Path
import json

## Log file's name ##
LOG_FILE = "llm_usage_records.json"
LOG_FILE_ENCODING = "UTF-8"

@beartype
@dataclass
class RecordUsage:
    load_previous_usages: bool | None = True
    create_file: bool | None = True
    auto_refresh: bool | None = True
    LOG_FILE: str | None = LOG_FILE

    def __post_init__(self):
        self.__total_tasks = set()

        path = Path(LOG_FILE)

        if path.exists():
            with path.open(encoding=LOG_FILE_ENCODING) as file:
                self.__loaded_json = json.load(file)

                for key, value in self.__loaded_json.items():
                    self.__total_tasks.add(value)
        else:
            # Reading the JSON file
            try:
                if self.load_previous_usages:
                    if self.create_file:
                        log(f"LLM records file ({LOG_FILE}) doesn't exist, creating a new one...")

                        with path.open(encoding=LOG_FILE_ENCODING, mode="x") as file:
                            log(f"LLM records file created successfully!")
                else:
                    log("", level="warn")
            except PermissionError:
                pass

    def record(self, usage: str):
        pass