import socket
from . import Rule
from urllib.parse import urlparse

class ActiveURL(Rule):
    def passes(self, attribute, value, parameters, validator):
        try:
            url = urlparse(value)
            if not url.netloc:
                return False
            socket.gethostbyname(url.netloc)
            return True
        except Exception:
            return False

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} is not a valid active URL."