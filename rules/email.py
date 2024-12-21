import re
from email_validator import validate_email, EmailNotValidError

from . import Rule

class Email(Rule):
    def passes(self, attribute, value, parameters, validator):
        try:
            valid = validate_email(value, check_deliverability=False)
            return True
        except EmailNotValidError as e:
            self.set_error_message(str(e))
            return False

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a valid email address."