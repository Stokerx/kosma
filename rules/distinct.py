from . import Rule

class Distinct(Rule):
    def passes(self, attribute, value, parameters, validator):
        if not isinstance(value, list):
            return False

        if 'strict' in parameters:
            return len(value) == len(set(value))
        else:
            return len(value) == len({str(x).lower() if isinstance(x, str) else x for x in value})

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field has duplicate values."