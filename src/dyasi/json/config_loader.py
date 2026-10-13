from dyasi.json.loader import Load, CreateObject
import dyasi.json.checkers as checkers
from dyasi.exceptions import ConfigError
from dyasi.utils import log
from dataclasses import dataclass
from beartype import beartype

@beartype
@dataclass
class Defaults:
    loaded_object: Load

    def __post_init__(self):
        self.MODIFIED_DICTIONARY: dict = self.loaded_object.json_data.copy()

        for key, value in self.loaded_object.json_data.items():
            try:
                # Calling the checker function of by the name of the key
                self.MODIFIED_DICTIONARY[key] = getattr(checkers, key)(value)
            except AttributeError:
                log(f"You should provide a checker function for the key \"{key}\" at json/checkers.py. If you don't know what is it , Please contact the owner", level="warn")
            except ConfigError as e:
                raise ConfigError(f"Something went wrong while checking the key \"{key}\"'s value: {e}")
            except TypeError:
                raise ConfigError(f"Something went wrong while checking the key \"{key}\"'s value: value's datatype is not appropriate")
            
        # Adding the JSON data to the instance as an attribute
        # NOTE: we set ignore_headers to true to stop recursion for headers
        self.__dict__.update(CreateObject(self.MODIFIED_DICTIONARY, keys_to_ignore=["headers", "in_scope_assets", "out_scope_assets"]).__dict__)

    def __iter__(self):
        for key, value in self.loaded_object.json_data.items():
            yield {key: value}

    def get_json(self) -> dict:
        return self.MODIFIED_DICTIONARY
            


# Imported JSON data
DEFAULTS = Defaults(Load("config/defaults.json"))