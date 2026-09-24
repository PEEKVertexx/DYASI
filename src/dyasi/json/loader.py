import json
from json import JSONDecodeError
from pathlib import Path
from dataclasses import dataclass
from dyasi.exceptions import InvalidPathError, InvalidKeyError
from beartype import beartype
import keyword

@beartype
@dataclass
class GetJSON:
    python_object: dict

    def __post_init__(self) -> None:
            for key, value in self.python_object.items():
                # If key is not an string
                if not isinstance(key, str):
                    raise InvalidKeyError(f"The key \"{value}\" must be an string!")
                # If the key is not a valid python identifier
                elif not key.isidentifier():
                    raise InvalidKeyError(f"The key \"{value}\" is not a valid python identifier!")
                # If the key is a reserved python keyword
                elif keyword.iskeyword(key):
                    raise InvalidKeyError(f"The key \"{value}\" is a reserved python keyword")
                else:
                    if isinstance(value, dict):
                        setattr(self, key, GetJSON(value))
                    else:
                        setattr(self, key, value)

@beartype
@dataclass
class Load:
    file_path: str

    def __post_init__(self) -> None:
        # Checking if it's a truthy
        if self.file_path:
            path = Path(self.file_path)

            if path.exists():
                if path.is_file():
                    try:
                        with path.open(mode="r", encoding="UTF-8") as file:
                            self.__dict__.update(GetJSON(json.load(file)).__dict__)
                    except PermissionError:
                        raise PermissionError(f"The user that you're executing this program with doesn't have permission to read \"{self.file_path}\". Try to add read permission to your current user through this command: chmod u+r {self.file_path}")
                    except JSONDecodeError:
                        raise JSONDecodeError(f"Invalid JSON found in \"{self.file_path}\"")
                else:
                    raise IsADirectoryError(f"\"{self.file_path}\" is a directory.")
            else:
                raise FileNotFoundError(f"\"{self.file_path}\" doesn't exist.")
        else:
            raise InvalidPathError("The value you provided as the file path is falsy.")