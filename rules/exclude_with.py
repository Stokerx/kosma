from . import Rule

class ExcludeWith(Rule):
    def __init__(self, other):
        self.other = other

    def passes(self, attribute, value, parameters, validator):
        if self.other in validator.data:
            return False
        return True

    def message(self, attribute, value, parameters, validator):
        return ""  # ExcludeWith no añade mensajes de error