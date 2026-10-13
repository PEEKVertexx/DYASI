from beartype import beartype
from dyasi.exceptions import ConfigError

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

    return MODIFIED_VERSION

@beartype
def scope(value: dict) -> dict:
    MODIFIED_VERSION: dict = {}

    # Checking enabled key
    if "enabled" not in value:
        raise ConfigError("You must provide the key \"enabled\" with a boolean (true/false) value to help the software to determine that wheter it should use the functions related to the scope or not.")

    # Checking the value of enabled key
    if not isinstance(value["enabled"], bool):
        raise ConfigError("the value of key \"enabled\" must be a boolean (true/false).")

    # Checking if atleast in scope or out scope assets are provided in the case that the scope feature is enabled
    if value["enabled"]:
        if not ("in_scope_assets" in value or "out_scope_assets" in value):
            raise ConfigError("You enabled the scope feature , then you must proivde atleast in or out scope assets")
    
    def check_assets(assets: list | None) -> list:
        MODIFIED_ASSETS: list = []

        # Checking if it's None
        if not assets and (assets is not None) and not isinstance(assets, list):
            raise ConfigError("assets must be a list or None , it could be even an empty list but you must provide a dictionary if you wish to add something in/out scope. The first key of it is what type of asset you want to specify (we currently support \"subdomain\" and \"path\") and the value of the firts key is the asset you want to specify")

        # Checking if it consists of non-empty dictionaries
        if not all(map(lambda asset: isinstance(asset, dict) and bool(asset), assets)):
            raise ConfigError("The entire items of the in scope and out of scope value must be dictionary and they couldn't be empty.")

        ## Checking the dictionaries
        ## NOTE: we currently support subdomains and paths
        for asset in assets:
            # Checking if the length of items are more than one
            if len(asset.items()) > 1:
                raise ConfigError("dictionaries cannot have more than one pair!")

            first_key = next(iter(asset))

            # Checking if the first key is an string
            if not isinstance(first_key, str):
                raise ConfigError("The first key of one of your assets is not an string!")

            # Making first key lowercase and stripped
            first_key = first_key.lower().strip()

            # Checking if it's a subdomain or path
            if first_key not in ["subdomain", "path"]:
                raise ConfigError("The first key of the assets must be either \"subdomain\" or \"path\"")

            # Checking the value
            elif not isinstance(asset[first_key], str):
                raise ConfigError("The value of the first key of the assets cannot be empty!")
            
            elif not asset[first_key].strip():
                raise ConfigError("The value of the first key of the assets cannot be empty!")

            # Adding the asset to the modified assets
            MODIFIED_ASSETS.append({
                first_key: asset[first_key].strip()
            })
        
        return MODIFIED_ASSETS
    
    # Checking in scope assets
    if "in_scope_assets" in value:
        try:
            MODIFIED_VERSION["in_scope_assets"] = check_assets(value["in_scope_assets"])
            MODIFIED_VERSION["in_scope_subdomains"] = [asset["subdomain"] for asset in MODIFIED_VERSION["in_scope_assets"] if "subdomain" in asset]
            MODIFIED_VERSION["in_scope_paths"] = [asset["path"] for asset in MODIFIED_VERSION["in_scope_assets"] if "path" in asset]
        except ConfigError as e:
            raise ConfigError(f"Error while check in scope assets: {e}")
    else:
        MODIFIED_VERSION["in_scope_assets"] = []

    # Checking out scope assets
    if "out_scope_assets" in value:
        try:
            # Adding the returned value of check_assets function to the modified version
            MODIFIED_VERSION["out_scope_assets"] = check_assets(value["out_scope_assets"])
            MODIFIED_VERSION["out_scope_subdomains"] = [asset["subdomain"] for asset in MODIFIED_VERSION["out_scope_assets"] if "subdomain" in asset]
            MODIFIED_VERSION["out_scope_paths"] = [asset["path"] for asset in MODIFIED_VERSION["out_scope_assets"] if "path" in asset]
        except ConfigError as e:
            raise ConfigError(f"Error while check out scope assets: {e}")
    else:
        MODIFIED_VERSION["out_scope_assets"] = []

    # Adding the enabled key to modified version ( I didn't implement it before , because we might raise some exceptions or some exceptions occur while checking the value of both in scope and out scope assets , so why should we assign a key to a dictionary that we couldn't use? )
    MODIFIED_VERSION["enabled"] = value["enabled"]

    # Checking if user provided atleast in or out scope assets if the scope feature is enabled
    if value["enabled"]:
        if not MODIFIED_VERSION["in_scope_assets"] and not MODIFIED_VERSION["out_scope_assets"]:
            raise ConfigError("You enabled the scope feature , but you didn't proivde any assets")

    return MODIFIED_VERSION