#!/usr/bin/env python3
import xml.etree.ElementTree as xml

def get_rules(content):
    root = xml.fromstring(content)
    entries = root.findall(".//rulebase/security/rules/entry")
    rules = []
    
    for e in entries:
        rule = {
            "name": e.get("name"),
            "source": [s.text for s in e.findall("./source/member")],
            "destination": [d.text for d in e.findall("./destination/member")],
            "application": [a.text for a in e.findall("./application/member")],
            "description": (e.findtext("description") or "").strip(),
            "disabled": (e.findtext("disabled") or "no").lower(),
            "log-end": (e.findtext("log-end") or "no").lower()
        }

        rules.append(rule)
    return rules
