import json
from . import Rule

class JSON(Rule):
    def passes(self, attribute, value, parameters, validator):
        try:
            json.loads(value)
            return True
        except (ValueError, TypeError):
            return False

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a valid JSON string."