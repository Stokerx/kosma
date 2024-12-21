from . import Rule

class Bail(Rule):
    def passes(self, attribute, value, parameters, validator):
        if attribute in validator.errors:
            raise StopValidation  # Detiene la validación del atributo
        return True

    def message(self, attribute, value, parameters, validator):
        return ""

class StopValidation(Exception):
    pass