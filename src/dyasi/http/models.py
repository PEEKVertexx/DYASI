from beartype import beartype
from dyasi.exceptions import InvalidRequestError, ClientRequestError
from dyasi.utils import log
from urllib.parse import urlparse
from dataclasses import dataclass
import dyasi.http.client as client
from dyasi.json.config_loader import DEFAULTS

default_http_version: str = "HTTP/1.1"

@beartype
@dataclass
class Request:
    request: dict

    def __post_init__(self):
        MODIFIED_REQUEST = self.request.copy()

        # Checking the the existense of the keys of each self.request. I think necessary parts are:
        # 1. self.request method
        # 2. URL

        ## Checking if the url key exists
        if not "url" in self.request:
            raise InvalidRequestError("URL not found.")
        ## Checking if the method exists
        elif not "method" in self.request:
            raise InvalidRequestError("Method not found.")


        # Checking the values of each key

        ## Checking method
        ### Checking if method's value is an string
        if not isinstance(self.request["method"], str):
            raise InvalidRequestError("Method is not an string.")

        ### Checking if method's value is a truthy
        if not self.request["method"].strip():
            raise InvalidRequestError("The method you provided is empty")

        ### Checking if the method is a valid HTTP method   
        elif self.request["method"].strip().upper() not in ["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "TRACE", "PATCH", "CONNECT"]:
            raise InvalidRequestError("The method you provided is not an HTTP method.")

        # Adding the method to the modified version of self.request if everything's okay about it
        MODIFIED_REQUEST["method"] = self.request["method"].strip().upper()

        # Checking URL

        parsed = urlparse(self.request["url"].strip())

        ## Checking the existence of necessary parts
        # I think necessary parts are:
        # 1. Scheme ( It must be http or https )
        # 2. Hostname
        # 3. Path

        ### Checking scheme
        if not parsed.scheme:
            raise InvalidRequestError("Your provided URL doesn't have scheme part (The first part of the url that specifies the protocol)")
        elif not parsed.scheme in ["http", "https"]:
            raise InvalidRequestError("Your provided URL's scheme is not HTTP or HTTPS")
        elif not parsed.path:
            parsed.path = "/"
            log("One of your provided requests hasn't a path , I'll consider the path as /", level="warn")
        elif not parsed.hostname:
            raise InvalidRequestError("Your provided URL doesn't have hostname part!")

        # Checking hostname
        hostname_components = parsed.hostname.split(".")

        if len(hostname_components) < 3 and not all(hostname_components):
            raise InvalidRequestError("Your provided hostname is invalid!")

        # Adding URL to the modified version of the self.request
        MODIFIED_REQUEST["url"] = self.request["url"].strip()
        MODIFIED_REQUEST["path"] = parsed.path

        MODIFIED_REQUEST["hostname"] = parsed.hostname

        # Checking other parts

        ## Checking query string
        if "query" in self.request:
            # Checking if it's a dictionary
            if isinstance(self.request["query"], dict):
                # Checking if it's a truthy
                if not self.request["query"]:
                    raise InvalidRequestError("You provided a falsy value as the query string")
                        
            # Checking if it's an string
            elif isinstance(self.request["query"], str):
                if not self.request["query"]:
                    raise InvalidRequestError("You provided a falsy value as the query string")
                else:
                    log("You provided an string as the query string in one of your provided self.requests, it works but it's recommended to enter a dictionary as the query string", level="warn")
            # Checking if it's a list
            elif isinstance(self.request["query"], list):
                # Checking if it's a trthy
                if not self.request["query"]:
                    raise InvalidRequestError("You provided a falsy value as the query string")
                else:
                    # Checking its values
                    for item in self.request["query"]:
                        # Checking if it's a tuple
                        if not isinstance(item, tuple):
                            raise InvalidRequestError("self.request contains a query string with a list that doesn't contain a tuple")
            else:
                raise InvalidRequestError("The self.request contains a query string, But its value is not a dictionary, list or string")
        else:
            MODIFIED_REQUEST["query"] = None

        # Checking self.request body
        if "body" in self.request:
            # Checking if it's a dictionary
            if isinstance(self.request["body"], dict):
                # Checking if it's a truthy
                if not self.request["body"]:
                    raise InvalidRequestError("The self.request contains a self.request body with a falsy value")
            # Checking if it's a list
            elif isinstance(self.request["body"], list):
                # Checking if it's a truthy
                if self.request["body"]:
                    pass
                else:
                    raise InvalidRequestError("You provided an empty list as the self.request body")
                for item in self.request["body"]:
                    # Checking if it's a tuple
                    if not isinstance(item, tuple):
                        raise InvalidRequestError("The self.request contains a self.request body with a list value that has a non-tuple item")
            # Checking if it's an string
            elif isinstance(self.request["body"], str):
                # Checking if it's a truthy
                if self.request["body"]:
                    pass
                else:
                    raise InvalidRequestError("You provided an empty string as the self.request body")
            else:
                raise InvalidRequestError("self.request body is not a dictionary, string or list")
        else:
            MODIFIED_REQUEST["body"] = None

        # Checking self.request headers
        if "headers" in self.request:
            # Checking if it's a dictioanry
            if isinstance(self.request["headers"], dict):
                # Checking if it's a truthy
                if not self.request["headers"]:
                    raise InvalidRequestError("You provided a falsy as self.request headers")
            # Adding custom header to the request

            ## Checking if user allows us to
            if DEFAULTS.custom_header is True:
                for hname, hvalue in DEFAULTS.custom_header.headers.items():
                    MODIFIED_REQUEST.headers[hname] = hvalue
            else:
                raise InvalidRequestError("The self.request contains a self.request headers part, But its value is not a dictionary or none")

        else:
            MODIFIED_REQUEST["headers"] = None

        # Checking HTTP version
        if "http_version" in self.request:
            # Checking if it's a valid http version
            if self.request['http_version'].upper() in ["HTTP/0.9", "HTTP/1.0", "HTTP/1.1", "HTTP/2", "HTTP/3"]:
                if self.request['http_version'].upper() != "HTTP/1.1":
                    self.request["http_version"] = "HTTP/1.1"
                    log("We solely support HTTP/1.1 http version currently, but we'll add support for other versions soon.", level="warn")
            else:
                raise InvalidRequestError("Your provided HTTP version is invalid.")

            # Adding http version to the modified version of original self.request
            MODIFIED_REQUEST["http_version"] = self.request["http_version"].upper()
        else:
            # Setting http version to HTTP/1.1 if no http version is provided
            MODIFIED_REQUEST["http_version"] = default_http_version

        # Initializing the keys and values of the modified self.request into the current instance of the class if everything is fine
        for key, value in MODIFIED_REQUEST.items():
            setattr(self, key, value)

@beartype
@dataclass
class HTTPExchange:
    request: Request

    def __post_init__(self):
        self.response = client.send(self.request)