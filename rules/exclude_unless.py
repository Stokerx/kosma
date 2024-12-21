from . import Rule

class ExcludeUnless(Rule):
    def __init__(self, other, value):
        self.other = other
        self.value = value

    def passes(self, attribute, value, parameters, validator):
        if validator.data.get(self.other) != self.value:
            return False
        return True

    def message(self, attribute, value, parameters, validator):
        return ""  # ExcludeUnless no añade mensajes de error