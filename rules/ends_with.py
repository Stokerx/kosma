from . import Rule

class EndsWith(Rule):
    def __init__(self, *endings):
        self.endings = endings

    def passes(self, attribute, value, parameters, validator):
        return any(str(value).endswith(end) for end in self.endings)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must end with one of the following: {', '.join(self.endings)}."