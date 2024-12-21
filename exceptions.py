class ValidationException(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__("Validación fallida.")

class RuleNotFoundException(Exception):
    def __init__(self, rule_name):
        self.rule_name = rule_name
        super().__init__(f"Regla de validación no encontrada: {rule_name}")