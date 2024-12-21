from . import Rule

class Required(Rule):
    def passes(self, attribute, value, parameters, validator):
        if value is None:
            return False
        if isinstance(value, str) and value.strip() == '':
            return False
        if isinstance(value, list) and len(value) == 0:
            return False
        if isinstance(value, dict) and len(value) == 0:
            return False
        if isinstance(value, object) and not hasattr(value, '__len__'):
            return True  
        if hasattr(value, '__len__') and len(value) == 0:
            return False
        return True

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field is required."