import re
from . import Rule

class HexColor(Rule):
    def passes(self, attribute, value, parameters, validator):
        return bool(re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value))

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a valid hexadecimal color code."