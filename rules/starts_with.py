from . import Rule

class StartsWith(Rule):
    def __init__(self, *prefixes):
        self.prefixes = prefixes

    def passes(self, attribute, value, parameters, validator):
        return any(str(value).startswith(prefix) for prefix in self.prefixes)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must start with one of the following: {', '.join(self.prefixes)}."