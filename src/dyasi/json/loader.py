import json
from json import JSONDecodeError
from pathlib import Path
from dataclasses import dataclass
from dyasi.exceptions import InvalidPathError, InvalidKeyError, InvalidJSONError
from beartype import beartype
import keyword

@beartype
@dataclass
class CreateObject:
    python_object: dict
    recursive: bool | None = True
    # NOTE: use ignore headers feature only when you want recursion and don't want the values of headers key ( as it might be a dictionary )
    keys_to_ignore: list | set | tuple | None

    def __post_init__(self) -> None:
            for key, value in self.python_object.items():
                # Checking the key

                ## If key is not an string
                if not isinstance(key, str):
                    raise InvalidKeyError(f"The key \"{key}\" must be an string!")
                ## If the key is not a valid python identifier
                elif not key.isidentifier():
                    raise InvalidKeyError(f"The key \"{key}\" is not a valid python identifier!")
                ## If the key is a reserved python keyword
                elif keyword.iskeyword(key):
                    raise InvalidKeyError(f"The key \"{key}\" is a reserved python keyword")               

                # Checking the value
                if isinstance(value, dict):
                    if self.ignore_headers:
                        # Checking if the recursion is allowed
                        if self.recursive:
                            # Ignoring the headers if the key being headers
                            if key in self.keys_to_ignore:
                                pass
                            else:
                                setattr(self, key, CreateObject(value))
                                continue
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
                            self.json_data = json.load(file)

                            # Checking if JSON data is a dictionary
                            if not isinstance(self.json_data, dict):
                                raise InvalidJSONError("JSON must be a dictionary-like data!")
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

    def create_object(self):
        self.__dict__.update(CreateObject(self.json_data).__dict__)
        return self