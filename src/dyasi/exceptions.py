class InvalidPathError(Exception):
    pass

class InvalidRequestError(Exception):
    pass

class InvalidKeyError(Exception):
    pass

class InvalidLogLevelError(Exception):
    pass

class InvalidJSONError(Exception):
    pass

class MissingCheckFunction(Exception):
    pass

class ConfigError(Exception):
    pass

class ClientRequestError(Exception):
    pass

class ScopeEngineError(Exception):
    pass

class FeatureDisabledError(Exception):
    pass

class MissingRequirementError(Exception):
    pass

class MissingPropertyError(Exception):
    pass

class InappropiratePropertyError(Exception):
    pass

class InvalidTaskError(Exception):
    pass