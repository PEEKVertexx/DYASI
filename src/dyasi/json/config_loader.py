from dyasi.json.loader import Load, CreateObject
import dyasi.json.checkers as checkers
from dyasi.exceptions import MissingCheckFunction, ConfigError

class DefaultsCheck:
    loaded_object: Load

    def __post__init__(self):
        LOADED_DICTIONARY: dict = self.loaded_object.get_dict()
        MODIFIED_DICTIONARY: dict = LOADED_DICTIONARY

        for key, value in LOADED_DICTIONARY:
            try:
                # Calling the checker function of by the name of the key
                MODIFIED_DICTIONARY[key] = getattr(checkers, key)(value)
            except AttributeError:
                raise MissingCheckFunction(f"You didn't define a check function for the key {key}")
            except ConfigError as e:
                raise ConfigError(f"Something went wrong while checking the key \"{key}\"'s value: {e}")

        # Adding the JSON data to the instance as an attribute
        self.__dict__.update(CreateObject(MODIFIED_DICTIONARY).__dict__)


# Imported JSON data
DEFAULTS = DefaultsCheck("config/defaults.json")