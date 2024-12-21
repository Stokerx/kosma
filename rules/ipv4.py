import socket
from . import Rule

class IPv4(Rule):
    def passes(self, attribute, value, parameters, validator):
        try:
            socket.inet_aton(value)
            return True
        except socket.error:
            return False

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a valid IPv4 address."