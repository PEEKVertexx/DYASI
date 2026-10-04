from dyasi.json.loader import Load, CreateObject
import dyasi.json.checkers as checkers
from dyasi.exceptions import MissingCheckFunction, ConfigError
from dyasi.utils import log
from dataclasses import dataclass

@dataclass
class DefaultsCheck:
    loaded_object: Load

    def __post__init__(self):
        LOADED_DICTIONARY: dict = self.loaded_object.json_data
        MODIFIED_DICTIONARY: dict = LOADED_DICTIONARY.copy()

        for key, value in LOADED_DICTIONARY:
            try:
                # Calling the checker function of by the name of the key
                MODIFIED_DICTIONARY[key] = getattr(checkers, key)(value)
            except AttributeError:
                log(f"You should provide a checker function for the key {key} at json/checkers.py. If you don't know what is it , Please contact the owner", level="warn")
            except ConfigError as e:
                raise ConfigError(f"Something went wrong while checking the key \"{key}\"'s value: {e}")
            except TypeError:
                raise ConfigError(f"Something went wrong while checking the key \"{key}\"'s value: value's datatype is not appropriate")

        # Adding the JSON data to the instance as an attribute
        self.__dict__.update(CreateObject(MODIFIED_DICTIONARY).__dict__)


# Imported JSON data
DEFAULTS = DefaultsCheck(Load("config/defaults.json"))