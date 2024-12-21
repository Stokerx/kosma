import re
from . import Rule

class AlphaNum(Rule):
    def passes(self, attribute, value, parameters, validator):
        return bool(re.match(r'^[a-zA-Z0-9]+$', value))

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} may only contain letters and numbers."