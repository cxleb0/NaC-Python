from modules.module import Finding, FirewallRule, Policy


def check_any_any(rule:FirewallRule,policy:Policy):
    if not policy.enabled:
        return None
    if ("any".lower() in rule.source and "any".lower() in rule.destination and "any".lower() in rule.application):
        return Finding( 
            rule = rule.name,
            issue = "Any Any rule found",
            severity= policy.severity,
            message= policy.message
        )
    return None

def check_missing_description(rule:FirewallRule,policy:Policy):
    if not policy.enabled:
        return None
    if not rule.description:
        return Finding(
            rule =  rule.name,
            issue = "Missing Description",
            severity = policy.severity,
            message = policy.message
        )
    return None

def check_logging(rule:FirewallRule,policy:Policy):
    if not policy.enabled:
        return None
    if not rule.log_end:
        return Finding(
            rule = rule.name,
            issue = "Logging Disabled",
            severity = policy.severity,
            message = policy.message
        )
    return None

def check_disabled(rule:FirewallRule,policy:Policy):
    if not policy.enabled:
        return None
    if rule.disabled:
        return Finding(
            rule = rule.name,
            issue = "Disabled rule",
            severity = policy.severity,
            message = policy.message
        )
    return None 
