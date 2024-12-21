from . import Rule

class Prohibits(Rule):
    def __init__(self, *others):
        self.others = others

    def passes(self, attribute, value, parameters, validator):
        if attribute in validator.data:
            for other in self.others:
                if other in validator.data:
                    return False
        return True

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field prohibits {', '.join(self.others)} from being present."