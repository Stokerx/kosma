from . import Rule

class RequiredArrayKeys(Rule):
    def __init__(self, *keys):
        self.keys = keys

    def passes(self, attribute, value, parameters, validator):
        if not isinstance(value, dict):
            return False
        for key in self.keys:
            if key not in value:
                return False
        return True

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field must contain all of the following keys: {', '.join(self.keys)}."