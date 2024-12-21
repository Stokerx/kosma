import socket
from . import Rule

class IP(Rule):
    def passes(self, attribute, value, parameters, validator):
        try:
            socket.inet_aton(value)
            return True
        except socket.error:
            try:
                socket.inet_pton(socket.AF_INET6, value)
                return True
            except socket.error:
                return False

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a valid IP address."