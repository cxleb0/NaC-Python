class FirewallAuditError(Exception):
    """Base exception for audit tool."""


class ConfigLoadError(FirewallAuditError):
    """Raise error when config file cannot be loaded."""


class ConfigParseError(FirewallAuditError):
    """Raise error when XML parcing fails."""


class PolicyLoadError(FirewallAuditError):
    """Raise error when policy loading fails"""
