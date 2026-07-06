from dataclasses import dataclass

@dataclass
class FirewallRules:
    name:str
    source:list[str]
    destination:list[str]
    application:list[str]
    description: str
    disabled: bool
    log_end: bool

class Findings:
    rule: str
    issue: str
    message: str
    severity: str 

    
