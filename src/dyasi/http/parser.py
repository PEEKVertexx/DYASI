import json
from pathlib import Path
from dataclasses import dataclass
from beartype import beartype
from dyasi.exceptions import InvalidPathError, InvalidRequestError
from dyasi.http.models import Request, HTTPExchange

    
@dataclass
class Parse:
    file_path: str

    @beartype
    def __post__init__(self):
        # Checking if it's a truthy
        if self.file_path:
            path = Path(self.file_path)

            # Checking if the file exists
            if path.exists():
                # Checking if the path is a file
                if path.is_file():
                    self.__REQUESTS: list[Request] = []

                    with path.open(mode="r", encoding="UTF-8") as file:
                        # Converting JSON data to a python object
                        REQUESTS = json.load(file)

                        # Checking if it's a dictionary
                        if isinstance(REQUESTS, dict):
                            # Adding requests to the instance
                            for key, value in REQUESTS.items():
                                # Creating an object from the request
                                try:
                                    self.__REQUESTS.append(Request(value))
                                except TypeError:
                                    raise TypeError(f"The value of request with id {key} is not a dictionary!")
                                except InvalidRequestError as reason:
                                    raise InvalidRequestError(f"Request with id \"{key}\" is not a valid request: {reason}")
                        # Checking if it's a list
                        elif isinstance(REQUESTS, list):
                            for index, request in enumerate(REQUESTS):
                                try:
                                    self.__REQUESTS.append(Request(request))
                                except TypeError:
                                    raise TypeError(f"The value of request #{index} is not a dictionary")
                                except InvalidRequestError as reason:
                                    raise InvalidRequestError(f"Request #{key} is not a valid request: {reason}")

                    self.iteration_number = 0
                    
                else:
                    raise IsADirectoryError(f"\"{self.file_path}\" is a directory.")
            else:
                raise FileNotFoundError(f"\"{self.file_path}\" doesn't exist.")
        else:
            raise InvalidPathError("The value you provided as the file path is falsy.")

    def __iter__(self):
        for request in self.__REQUESTS:
            yield request