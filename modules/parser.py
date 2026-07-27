#!/usr/bin/env python3
import xml.etree.ElementTree as xml
from modules.module import FirewallRule
from modules.exceptions import ConfigParseError

def get_rules(content: str) -> list[FirewallRule]:
    """
    Parses a Firewall XML configuration file and extract firewall rules.
    Args:
         Content: The XML configuration as a string
    Returns:
         A list of FirewallRule dataclass objects.
    Raises:
         ConfigParseError: If xml is invalid or malformed.
    """
    
    try:
        root = xml.fromstring(content)
    except xml.ParseError as e:
        raise ConfigParseError(f"Error in parsing xml configuration.") from e
    entries = root.findall(".//rulebase/security/rules/entry")
    rules: list[FirewallRule] = []
    
    for e in entries:
        name = e.get("name")
        if name is None:
            raise ValueError("Missing Name Attribute")
        rule = FirewallRule(
            name=name,
            source=[s.text for s in e.findall("./source/member") if s.text],
            destination=[d.text for d in e.findall("./destination/member") if d.text],
            application=[a.text for a in e.findall("./application/member") if a.text],
            description=(e.findtext("description") or "").strip(),
            disabled=((e.findtext("disabled") or "no").lower() == "yes"),
            log_end=((e.findtext("log-end") or "no").lower() == "yes")
        )


        rules.append(rule)
    return rules
