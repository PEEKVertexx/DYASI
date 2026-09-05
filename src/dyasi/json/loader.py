import json
from json import JSONDecodeError
from pathlib import Path
from dataclasses import dataclass
from dyasi.exceptions import *

@dataclass
class GetJSON:
    def __init__(self, python_object: dict) -> None:
        # Checking if it's a dictionary
        if isinstance(python_object, dict):
            for key, value in python_object.items():
                if isinstance(value, dict):
                    setattr(self, key, GetJSON(value))
                else:
                    setattr(self, key, value)
        else:
            raise TypeError("You must enter a dictionary as python_object")

@dataclass
class Load:
    def __init__(self, file_path: str) -> None:
        # Checking if it's an string
        if isinstance(file_path, str):
            # Checking if it's a truthy
            if file_path:
                path = Path(file_path)

                if path.exists():
                    if path.is_file():
                        with open(file=file_path, mode="r", encoding="UTF-8") as file:
                            try:
                                self.__dict__.update(GetJSON(json.load(file)).__dict__)
                            except JSONDecodeError:
                                raise JSONDecodeError(f"Invalid JSON found in \"{file_path}\"")
                    else:
                        raise IsADirectoryError(f"\"{file_path}\" is a directory.")
                else:
                    raise FileNotFoundError(f"\"{file_path}\" doesn't exist.")
            else:
                raise InvalidPathError("The value you provided as the file path is falsy.")
        else:
            raise InvalidPathError("The path you provided is not an instance of string!")

