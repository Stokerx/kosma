from . import Rule

class Exclude(Rule):
    def passes(self, attribute, value, parameters, validator):
        return False

    def message(self, attribute, value, parameters, validator):
        return ""  # Exclude no añade mensajes de error