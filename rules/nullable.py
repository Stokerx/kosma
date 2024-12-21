from . import Rule

class Nullable(Rule):
    def passes(self, attribute, value, parameters, validator):
        return True  # Siempre pasa, ya que permite valores nulos

    def message(self, attribute, value, parameters, validator):
        return ""  # Nullable no añade mensajes de error