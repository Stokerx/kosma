from . import Rule

class File(Rule):
    def passes(self, attribute, value, parameters, validator):
        return hasattr(value, 'read') and callable(value.read)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a file."