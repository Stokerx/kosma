from . import Rule

class Numeric(Rule):
    def passes(self, attribute, value, parameters, validator):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a number."