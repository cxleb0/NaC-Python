#!/usr/bin/env python3
import xml.etree.ElementTree as xml
from modules.module import FirewallRule

def get_rules(content: str) -> list[FirewallRule]:
    root = xml.fromstring(content)
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
