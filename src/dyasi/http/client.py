import requests
from beartype import beartype
import dyasi.http.models as models
from dyasi.json.config_loader import DEFAULTS
from dyasi.exceptions import ClientRequestError

@beartype
def send(request: models.Request):
    try:
        method = getattr(requests, request.method.lower())
        response = method(url=request.url + request.path, params=request.query, data=request.body, headers=request.headers)
        return response
    except AttributeError as e:
        # raise ClientRequestError("The method could not be found at requests library. As we validate the method in the models , make sure that you or anyone else didn't manipulate the request models and you're using the models.Request object. If everything is okay about it, try to install the official version of requests library by executing this command: \"pip install requests\" or try to check it through: \"pip show requests\"")
        raise e