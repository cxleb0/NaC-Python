import xml.etree.ElementTree as xml

from modules.exceptions import ConfigParseError
from modules.module import FirewallRule


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
        raise ConfigParseError("Error in parsing xml configuration.") from e
    entries = root.findall(".//rulebase/security/rules/entry")
    rules: list[FirewallRule] = []

    for entry in entries:
        name = entry.get("name")
        if name is None:
            raise ValueError("Missing Name Attribute")
        rule = FirewallRule(
            name=name,
            source=[s.text for s in entry.findall("./source/member") if s.text],
            destination=[d.text for d in entry.findall("./destination/member") if d.text],
            application=[a.text for a in entry.findall("./application/member") if a.text],
            description=(entry.findtext("description") or "").strip(),
            disabled=((entry.findtext("disabled") or "no").lower() == "yes"),
            log_end=((entry.findtext("log-end") or "no").lower() == "yes"),
        )

        rules.append(rule)
    return rules
