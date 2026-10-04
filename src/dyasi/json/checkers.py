from beartype import beartype
from src.dyasi.exceptions import ConfigError

@beartype
def version(value: str) -> str:
    # Checking if it's a truthy
    if not value:
        raise ConfigError("value is empty!")

    # Returning the value
    return value.strip()
    
@beartype
def uninteresting_headers(value: dict) -> dict:
    MODIFIED_VERSION= value.copy()

    # Checking if it's a truthy
    if not value:
        raise ConfigError("value is empty!")

    # Checking its content

    ## Checking remove
    if "remove" in value:
        # Checking if it's a boolean
        if not isinstance(value["remove"], bool):
            raise ConfigError("remove key's value must be a boolean (true or false)")
    else:
        raise ConfigError("you didn't provide the remove key!")

    ## Checking the uninteresting request & response headers if the feature being enabled
    if value["remove"]:
        ## Checking request headers
        if "request_headers" in value:
            # Adding the key to the modified version
            MODIFIED_VERSION["request_headers"] = []

            # Checking if it's a list
            if isinstance(value["request_headers"], list):
                # Checking if it's a truthy
                if value["request_headers"]:
                    # Adding the request_headers to the modified version
                    MODIFIED_VERSION["request_headers"] = []

                    for header in value["request_headers"]:
                        header = header.strip()

                        # Checking if it's an string
                        if not isinstance(header, str):
                            raise ConfigError("request_headers contains an item which is not an string!")

                        # Checking if it's a truthy
                        elif not header:
                            raise ConfigError("request_headers contains an empty string!")
            else:
                raise ConfigError("request_headers is not a list.")
        else:
            raise ConfigError("You didn't provide the request_headers key!")

        ## Checking response headers
        if "response_headers" in value:
            # Checking if it's a list
            if isinstance(value["response_headers", list]):
                # Checking if it's a truthy
                if value["response_headers"]:
                    # Adding the key to the modified version
                    MODIFIED_VERSION["response_headers"] = []

                    # Checking its items
                    for header in value["response_headers"]:
                        header = header.strip()

                        # Checking if the header is an string
                        if not isinstance(header, str):
                            raise ConfigError("response_headers contains an item which is not an string!")
                        
                        # Checking if it's truthy
                        elif not header:
                            raise ConfigError("response_headers contains an empty string!")

                        # Adding the response header to the modified version
                        MODIFIED_VERSION["response_headers"].append(header)
                else:
                    raise ConfigError("the key response_headers is empty!")
            else:
                raise ConfigError("response_headers is not a list.")
        else:
            raise ConfigError("You didn't provide the response_headers key!")

    # Returning the modified version
    return MODIFIED_VERSION

@beartype
def custom_header(value: dict) -> dict:
    MODIFIED_VERSION = value.copy()

    # Checking if it's a truthy
    if not value:
        raise ConfigError("value is empty!")

    # Checking enabled key
    if "enabled" in value:
        # Checking if its value is a boolean
        if not isinstance(value["enabled"], bool):
            raise ConfigError("The key enabled's value must be a boolean(true or false)!")
    else:
        raise ConfigError("The key enabled doesn't exist!")

    # Checking the headers is the feature is enabled
    if value["enabled"]:
        # Validating the headers
        pass
