def check_any_any(rule,policy):
    if not policy["enabled"]:
        return None
    if ("any" in rule["source"] and "any" in rule["destination"] and "any" in rule["application"]):
        return {
            "rule": rule["name"],
            "issue": "Any Any rule found",
            "severity": policy["severity"],
            "message": policy["message"]
        }
    return None

def check_missing_description(rule,policy):
    if not rule["description"]:
        return {
            "rule": rule["name"],
            "issue": "Missing Description",
            "severity": policy["severity"],
            "message": policy["message"]
        }
    return None

def check_logging(rule,policy):
    if rule["log-end"] != "yes":
        return {
            "rule": rule["name"],
            "issue": "Logging Disabled",
            "severity": policy["severity"],
            "message": policy["message"]
        }

def check_disabled(rule,policy):
    if rule["disabled"] == "yes":
        return {
            "rule": rule["name"],
            "issue": "Disabled rule",
            "severity": policy["severity"],
            "message": policy["message"]
        }
