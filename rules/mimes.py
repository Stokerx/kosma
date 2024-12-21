from . import Rule

class Mimes(Rule):
    def __init__(self, *allowed_extensions):
        self.allowed_extensions = allowed_extensions

    def passes(self, attribute, value, parameters, validator):
        if not hasattr(value, 'extension'):
            return False
        return value.extension.lower() in [ext.lower() for ext in self.allowed_extensions]

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a file of type: {', '.join(self.allowed_extensions)}."