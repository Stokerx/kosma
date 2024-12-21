import pytz
from . import Rule

class Timezone(Rule):
    def passes(self, attribute, value, parameters, validator):
        return value in pytz.all_timezones

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a valid timezone."