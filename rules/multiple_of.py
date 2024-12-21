from decimal import Decimal, InvalidOperation
from . import Rule

class MultipleOf(Rule):
    def __init__(self, number):
        self.number = number

    def passes(self, attribute, value, parameters, validator):
        try:
            return Decimal(value) % Decimal(self.number) == 0
        except (InvalidOperation, TypeError, ValueError):
            return False

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a multiple of {self.number}."