import re
from . import Rule

class MacAddress(Rule):
    def passes(self, attribute, value, parameters, validator):
        return bool(re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", value))

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a valid MAC address."