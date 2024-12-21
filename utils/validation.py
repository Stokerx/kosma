from kosma import rules
from kosma.exceptions import RuleNotFoundException

def parse_rule(rule):
    if isinstance(rule, str):
        if ':' in rule:
            rule_name, parameters = rule.split(':', 1)
            parameters = parameters.split(',')
        else:
            rule_name = rule
            parameters = []
        return rule_name.strip(), parameters
    elif isinstance(rule, tuple):
        return rule[0], list(rule[1:])
    else:
        return rule, []

def resolve_rule(rule_name):
    rule_class_name = rule_name
    try:
        rule_class = getattr(rules, rule_class_name)
        return rule_class()
    except AttributeError:
        raise RuleNotFoundException(rule_class_name)

def get_error_message(attribute, rule_name, rule_instance, parameters, validator):
    custom_message = validator.messages.get(f"{attribute}.{rule_name}")
    if custom_message:
        return custom_message

    if hasattr(rule_instance, 'message'):
        if callable(rule_instance.message):
            return rule_instance.message(attribute, validator.data.get(attribute), parameters, validator)
        else:
            return rule_instance.message
    else:
        return f"The {attribute} field is invalid."