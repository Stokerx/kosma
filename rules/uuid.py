import re
from . import Rule

class UUID(Rule):
    def passes(self, attribute, value, parameters, validator):
        return bool(re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", str(value), re.IGNORECASE))

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a valid UUID."