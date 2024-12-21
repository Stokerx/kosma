from . import Rule

class RequiredUnless(Rule):
    def __init__(self, another_field, value):
        self.another_field = another_field
        self.value = value

    def passes(self, attribute, value, parameters, validator):
        if validator.data.get(self.another_field) != self.value:
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
        return f"The {attribute} field is required unless {self.another_field} is {self.value}."