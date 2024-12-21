from . import Rule

class RequiredIf(Rule):
    def __init__(self, another_field, *values):
        self.another_field = another_field
        self.values = values

    def passes(self, attribute, value, parameters, validator):
        if validator.data.get(self.another_field) in self.values:
            if value is None:
                return False
            if isinstance(value, str) and value.strip() == '':
                return False
            if isinstance(value, list) and len(value) == 0:
                return False
            if isinstance(value, dict) and len(value) == 0:
                return False
            return True
        return True

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field is required when {self.another_field} is one of {', '.join(self.values)}."