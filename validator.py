import re

from exceptions import ValidationException, RuleNotFoundException
import utils
from rules import *

class Validator:
    def __init__(self, data, rules, messages=None):
        self.data = data
        self.rules = self._explode_rules(rules)
        self.messages = messages if messages is not None else {}
        self.errors = {}
        self.validated_data = {}
        self.implicit_attributes = utils.implicit_attributes.expand_implicit_attributes(data, self.rules)

    def _explode_rules(self, rules):
        exploded_rules = {}
        for attribute, rules in rules.items():
            if isinstance(rules, str):
                rules = rules.split('|')
            exploded_rules[attribute] = []

            for rule in rules:
                if isinstance(rule, str):
                    rule_name, parameters = utils.validation.parse_rule(rule)
                    exploded_rules[attribute].append((rule_name, parameters))
                else:
                    exploded_rules[attribute].append((rule, []))

        return exploded_rules

    def validate(self):
        for attribute, rules in self.rules.items():
            for rule in rules:
                self.validate_attribute(attribute, rule)
        if self.errors:
            raise ValidationException(self.errors)
        return self.validated_data

    def validate_attribute(self, attribute, rule_info):
        from rules import Rule as BaseRule

        if isinstance(rule_info, tuple):
            rule_name, parameters = rule_info
            if isinstance(rule_name, str):
                rule_instance = utils.validation.resolve_rule(rule_name)
            else:
                rule_instance = rule_name
                parameters = []
        else:
            rule_instance = rule_info
            parameters = []

        if not isinstance(rule_instance, BaseRule):
            raise ValueError(f"Rule '{rule_instance}' is not a valid rule")

        if rule_instance.passes(attribute, self.data.get(attribute), parameters, self):
            self.validated_data[attribute] = self.data.get(attribute)
        else:
            self.add_error(attribute, rule_instance, parameters)

    def add_error(self, attribute, rule_instance, parameters):
        rule_name = rule_instance.__class__.__name__ if not isinstance(rule_instance, str) else rule_instance
        error_message = utils.validation.get_error_message(attribute, rule_name, rule_instance, parameters, self)
        if attribute not in self.errors:
            self.errors[attribute] = []
        self.errors[attribute].append(error_message)

    def passes(self):
        try:
            self.validate()
            return True
        except ValidationException:
            return False

    def fails(self):
        return not self.passes()

    def errors(self):
        return self.errors

    def validated(self):
        if not hasattr(self, '_validated'):
            self._validated = self.validate()
        return self._validated