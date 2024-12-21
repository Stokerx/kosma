from . import Rule

class ExcludeWithout(Rule):
    def __init__(self, other):
        self.other = other

    def passes(self, attribute, value, parameters, validator):
        if self.other not in validator.data:
            return False
        return True

    def message(self, attribute, value, parameters, validator):
        return ""  # ExcludeWithout no añade mensajes de error