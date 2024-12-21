from . import Rule

class RequiredWithAll(Rule):
    def __init__(self, *fields):
        self.fields = fields

    def passes(self, attribute, value, parameters, validator):
        if all(validator.data.get(field) is not None for field in self.fields):
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
        return f"The {attribute} field is required when all of {', '.join(self.fields)} are present."