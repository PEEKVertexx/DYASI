from beartype import beartype
from dataclasses import dataclass
from dyasi.exceptions import ScopeEngineError
from dyasi.utils import log
from dyasi.json.config_loader import DEFAULTS
import dyasi.http.models as models

@beartype
@dataclass
class Scope:
    # NOTE: this option is for raising exceptions if a request being out of scope in requests, the class would raise exceptions for other cases
    requests: list[models.Request]
    raise_error: bool | None = False

    def __post_init__(self):
        self.__good_requests: list[models.Request] = []

        # Checking if user enabled the scope feature
        if not DEFAULTS.scope.enabled:
            raise ScopeEngineError("The scope feature is not enabled!")

        # Checking requests
        if not all(map(lambda request: isinstance(request, models.Request))):
            raise ScopeEngineError("You must provide a list that contains only request object!")

        # Checking in scope assets
        if DEFAULTS.in_scope_assets:
            # Checking subdomains
            if DEFAULTS.in_scope_subdomains:
                for request in self.requests:
                    if request.subdomain in DEFAULTS.in_scope_subdomains:
                        self.__good_requests.append(request)

            # Checking paths
            if DEFAULTS.in_scope_paths:
                for request in self.requests:
                    if request.path in DEFAULTS.in_scope_paths:
                        self.__good_requests.append(request)

            # Checking tlds
            if DEFAULTS.in_scope_tlds:
                for request in self.requests:
                    if request.hostname.split(".")[-1] in DEFAULTS.in_scope_tlds:
                        self.__good_requests.append(request)

            # Checking slds
            if DEFAULTS.in_scope_slds:
                for request in self.requests:
                    if request.hostname.split(".")[:-2] in DEFAULTS.in_scope_slds:
                        self.__good_requests.append(request)

        # Checking out scope assets
        elif DEFAULTS.out_scope_assets:
            # Checking subdomains
            if DEFAULTS.out_scope_subdomains:
                for request in self.requests:
                    if ".".join(request.hostname.split(".")[:-2]) not in DEFAULTS.out_scope_subdomains:
                        self.__good_requests.append(request)

            # Checking paths
            if DEFAULTS.out_scope_paths:
                for request in self.requests:
                    if request.path not in DEFAULTS.out_scope_paths:
                        self.__good_requests.append(request)

            # Checking tlds                        
            if DEFAULTS.out_scope_tlds:
                for request in self.requests:
                    if request.hostname.split(".")[-1] not in DEFAULTS.out_scope_tlds:
                        self.__good_requests.append(request)

            # Checking slds
            if DEFAULTS.out_scope_slds:
                for request.hostname.split(".")[-2] in self.requests:
                    self.__good_requests.append(request)

        # Checking if the user provided both in and out scope assets
        if DEFAULTS["in_scope_assets"] and DEFAULTS["out_scope_assets"]:
            log("You provided both in and out scope assets , note that we only consider the in scope assets you provided", level="warn")

    def __iter__(self):
        for request in self.__good_requests:
            yield request

    def get_requests(self) -> list[models.Request]:
        return self.__good_requests