from decimal import Decimal, InvalidOperation
from . import Rule

class Decimal(Rule):
    def __init__(self, min_decimals, max_decimals=None):
        self.min_decimals = int(min_decimals)
        self.max_decimals = int(max_decimals) if max_decimals is not None else None

    def passes(self, attribute, value, parameters, validator):
        try:
            decimal_value = Decimal(value)
            decimals = abs(decimal_value.as_tuple().exponent)
            if self.max_decimals is None:
                return decimals == self.min_decimals
            else:
                return self.min_decimals <= decimals <= self.max_decimals
        except InvalidOperation:
            return False

    def message(self, attribute, value, parameters, validator):
        if self.max_decimals is None:
            return f"The {attribute} must have exactly {self.min_decimals} decimal places."
        else:
            return f"The {attribute} must have between {self.min_decimals} and {self.max_decimals} decimal places."