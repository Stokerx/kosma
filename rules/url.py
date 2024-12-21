import re
from . import Rule

class URL(Rule):
    def passes(self, attribute, value, parameters, validator):
        pattern = re.compile(
            r"^(https?://)"  # http or https
            r"(?:www\.)?"  # optional www
            r"([-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6})"  # domain
            r"(/([-a-zA-Z0-9()@:%_\+.~#?&//=]*))?"  # path and parameters
            , re.IGNORECASE)
        return bool(re.match(pattern, value))

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} format is invalid."