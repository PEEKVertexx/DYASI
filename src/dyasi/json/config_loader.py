from dyasi.json.loader import Load, CreateObject
import dyasi.json.checkers as checkers
from dyasi.exceptions import MissingCheckFunction, ConfigError

class DefaultsCheck:
    loaded_object: Load

    def __post__init__(self):
        LOADED_DICTIONARY: dict = self.loaded_object.json_data
        MODIFIED_DICTIONARY: dict = LOADED_DICTIONARY
        REQUIRED_KEYS: list = [
            "version",
            "uninteresting_headers",
            "custom_header"
        ]

        # Checking if the required keys are inside the loaded dictionary
        INAVAILABLE_REQUIRED_KEYS: list = []

        for key in REQUIRED_KEYS:
            if key not in LOADED_DICTIONARY:
                INAVAILABLE_REQUIRED_KEYS.append(key)

        # Checking if there's any inavaiable required key
        if INAVAILABLE_REQUIRED_KEYS:
            raise ConfigError(f"Your provided JSON config misses those required keys: {" + ".join(INAVAILABLE_REQUIRED_KEYS)}")

        for key, value in LOADED_DICTIONARY:
            try:
                # Calling the checker function of by the name of the key
                MODIFIED_DICTIONARY[key] = getattr(checkers, key)(value)
            except AttributeError:
                raise MissingCheckFunction(f"You didn't define a check function for the key {key}")
            except ConfigError as e:
                raise ConfigError(f"Something went wrong while checking the key \"{key}\"'s value: {e}")
            except TypeError:
                raise ConfigError(f"Something went wrong while checking the key \"{key}\"'s value: value's datatype is not appropriate")

        # Adding the JSON data to the instance as an attribute
        self.__dict__.update(CreateObject(MODIFIED_DICTIONARY).__dict__)


# Imported JSON data
DEFAULTS = DefaultsCheck(Load("config/defaults.json"))