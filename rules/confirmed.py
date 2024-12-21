from . import Rule

class Confirmed(Rule):
    def passes(self, attribute, value, parameters, validator):
        confirmation_attribute = f"{attribute}_confirmation"
        return value == validator.data.get(confirmation_attribute)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} confirmation does not match."