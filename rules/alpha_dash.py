import re
from . import Rule

class AlphaDash(Rule):
    def passes(self, attribute, value, parameters, validator):
        return bool(re.match(r'^[a-zA-Z0-9_-]+$', value))

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} may only contain letters, numbers, dashes, and underscores."