from dataclasses import dataclass


@dataclass
class FirewallRule:
    name:str
    source:list[str]
    destination:list[str]
    application:list[str]
    description: str
    disabled: bool
    log_end: bool
    
@dataclass
class Finding:
    rule: str
    issue: str
    message: str
    severity: str

@dataclass
class Policy:
   name: str
   enabled: bool
   severity: str
   message: str

    
