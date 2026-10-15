from beartype import beartype
from dataclasses import dataclass
from dyasi.exceptions import ScopeEngineError
from dyasi.utils import log
# NOTE: We're importing the defaults class , not the defaults variable.
from dyasi.json.config_loader import DEFAULTS
import dyasi.http.models as models

@beartype
@dataclass
class Scope:
    # NOTE: this option is for raising exceptions if a request being out of scope in requests, the class would raise exceptions for other cases
    requests: list[models.Request]
    raise_error: bool | None = False

    def __post_init__(self):
        self.good_requests: list[models.Request] = []

        # Checking if user enabled the scope feature
        if not DEFAULTS.scope.enabled:
            raise ScopeEngineError("The scope feature is not enabled!")

        # Checking requests
        if not all(map(lambda request: isinstance(request, models.Request))):
            raise ScopeEngineError("You must provide a list that contains only request object!")

        DEFAULTS_JSON = DEFAULTS.get_json()

        if DEFAULTS_JSON["in_scope_assets"]:
            if DEFAULTS["in_scope_subdomains"]:
                for request in self.requests:
                    if request.subdomain in DEFAULTS["in_scope_subdomains"]:
                        self.good_requests.append(request)
            if DEFAULTS["in_scope_paths"]:
                for request in self.requests:
                    if request.path in DEFAULTS["in_scope_paths"]:
                        self.good_requests.append(request)
        elif DEFAULTS_JSON["out_scope_assets"]:
            if DEFAULTS["out_scope_subdomains"]:
                for request in self.requests:
                    if request.subdomain not in DEFAULTS["out_scope_subdomains"]:
                        self.good_requests.append(request)
            if DEFAULTS["out_scope_paths"]:
                for request in self.requests:
                    if request.path not in DEFAULTS["out_scope_paths"]:
                        self.good_requests.append(request)

        # Checking if the user provided both in and out scope assets
        if DEFAULTS["in_scope_assets"] and DEFAULTS["out_scope_assets"]:
            log("You provided both in and out scope assets , note that we only consider the in scope assets you provided", level="warn")