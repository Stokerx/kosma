import re
from . import Rule

class Alpha(Rule):
    def passes(self, attribute, value, parameters, validator):
        return bool(re.match(r'^[a-zA-Z]+$', value))

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} may only contain letters."