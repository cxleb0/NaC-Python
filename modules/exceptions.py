class FirewallAuditError(Exception):
    """Base exception for audit tool."""
    pass

class ConfigLoadError(FirewallAuditError):
    "Raise error when config file cannot be loaded."
    pass

class ConfigParseError(FirewallAuditError):
    """Raise error when XML parcing fails."""
    pass

class PolicyLoadFail(FirewallAuditError):
    """Raise error when policy loading fails"""
    pass
