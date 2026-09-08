import json
from json import JSONDecodeError
from pathlib import Path
from dataclasses import dataclass
from dyasi.exceptions import InvalidPathError, InvalidKeyError
from beartype import beartype
import keyword

@dataclass
class GetJSON:
    @beartype
    def __init__(self, python_object: dict) -> None:
            for key, value in python_object.items():
                if not isinstance(key, str):
                    raise InvalidKeyError(f"The key \"{value}\" must be an string!")
                elif not key.isidentifier():
                    raise InvalidKeyError(f"The key \"{value}\" is not a valid python identifier!")
                elif keyword.iskeyword(key):
                    raise InvalidKeyError(f"The key \"{value}\" is a reserved python keyword")
                else:
                    if isinstance(value, dict):
                        setattr(self, key, GetJSON(value))
                    else:
                        setattr(self, key, value)

@dataclass
class Load:
    @beartype
    def __init__(self, file_path: str) -> None:
        # Checking if it's a truthy
        if file_path:
            path = Path(file_path)

            if path.exists():
                if path.is_file():
                    try:
                        with path.open(mode="r", encoding="UTF-8") as file:
                            self.__dict__.update(GetJSON(json.load(file)).__dict__)
                    except PermissionError:
                        raise PermissionError(f"The user that you're executing this program with doesn't have permission to read \"{file_path}\". Try to add read permission to your current user through this command: chmod u+r {file_path}")
                    except JSONDecodeError:
                        raise JSONDecodeError(f"Invalid JSON found in \"{file_path}\"")
                else:
                    raise IsADirectoryError(f"\"{file_path}\" is a directory.")
            else:
                raise FileNotFoundError(f"\"{file_path}\" doesn't exist.")
        else:
            raise InvalidPathError("The value you provided as the file path is falsy.")