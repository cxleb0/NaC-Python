import subprocess

from modules.exceptions import FirewallGitAuditError
from modules.module import FirewallRule, RuleFieldChange


def get_file_at_revision(revision: str, file_path: str) -> str:
    """
    Retrieves a firewall configuration file from a specified Git revision.
    Args:
         revision: Git commit hash or reference containing the configuration.
         file_path: Repository-relative path to the configuration file.
    Returns:
         The contents of the configuration file as a string.
    Raises:
         FirewallGitAuditError: If Git cannot retrieve the file from the revision.
    """
    try:
        command = subprocess.run(
            ["git", "show", f"{revision}:{file_path}"],
            capture_output=True,
            text=True,
            check=True,
        )
        return command.stdout
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        raise FirewallGitAuditError(
            f"Unable to retrieve {file_path} from revision "
            f"{revision}. Git error: {error_message}"
        ) from e


def list_revision_changes(old_rules: list, new_rules: list) -> dict:
    """
    Compares two firewall rule collections and categorizes their changes.

    Rules are matched by name and classified as added, modified, unmodified,
    or deleted.
    Args:
         old_rules: Firewall rules from the previous configuration.
         new_rules: Firewall rules from the updated configuration.
    Returns:
         A dictionary containing lists of added, modified, unmodified,
         and deleted firewall rules. Modified rules are stored as
         (old_rule, new_rule) tuples.
    """
    # fw rule name will act as the key
    changes = {"added": [], "modified": [], "unmodified": [], "deleted": []}
    newrule_name = {rule.name: rule for rule in new_rules}
    oldrule_name = {rule.name: rule for rule in old_rules}
    for rule in new_rules:
        if rule.name not in oldrule_name:
            # check for added
            changes["added"].append(rule)
        else:
            old_rule = oldrule_name[rule.name]
            # existed before
            if rule == old_rule:
                # unmodifie
                changes["unmodified"].append(rule)
            else:
                # modified
                changes["modified"].append((old_rule, rule))
    for rule in old_rules:
        if rule.name not in newrule_name:
            # check for deleted
            changes["deleted"].append(rule)
    return changes



def compare_findings(old_findings, new_findings) -> dict:
    """
    Compares security findings between two firewall configurations.

    Findings are matched using their rule name and issue identifier, then
    categorized as new, resolved, or persistent.
    Args:
         old_findings: Security findings from the previous configuration.
         new_findings: Security findings from the updated configuration.
    Returns:
         A dictionary containing lists of new, resolved, and persistent findings.
    """
    results = {"new": [], "resolved": [], "persistent": []}
    for finding in new_findings:
        for old_finding in old_findings:
            if finding.rule == old_finding.rule and finding.issue == old_finding.issue:
                results["persistent"].append(finding)
                break
        else:
            results["new"].append(finding)

    for old_finding in old_findings:
        for finding in new_findings:
            if old_finding.rule == finding.rule and old_finding.issue == finding.issue:
                break
        else:
            results["resolved"].append(old_finding)

    return results



def get_field_changes(old_rule: FirewallRule, new_rule: FirewallRule) -> list[RuleFieldChange]:
    """
    Identifies individual field changes between two versions of a firewall rule.

    Compares source, destination, application, description, disabled status,
    and logging configuration.

    Args:
        old_rule: The firewall rule from the previous configuration.
        new_rule: The corresponding firewall rule from the updated configuration.

    Returns:
        A list of RuleFieldChange objects describing each modified field.
    """
    changes = []
    if old_rule.source != new_rule.source:
        changes.append(
            RuleFieldChange(old_rule.name, "source", old_rule.source, new_rule.source)
        )
    if old_rule.destination != new_rule.destination:
        changes.append(
            RuleFieldChange(
                old_rule.name, "destination", old_rule.destination, new_rule.destination
            )
        )
    if old_rule.application != new_rule.application:
        changes.append(
            RuleFieldChange(
                old_rule.name, "application", old_rule.application, new_rule.application
            )
        )
    if old_rule.description != new_rule.description:
        changes.append(
            RuleFieldChange(
                old_rule.name, "description", old_rule.description, new_rule.description
            )
        )
    if old_rule.disabled != new_rule.disabled:
        changes.append(
            RuleFieldChange(
                old_rule.name, "disabled", old_rule.disabled, new_rule.disabled
            )
        )
    if old_rule.log_end != new_rule.log_end:
        changes.append(
            RuleFieldChange(
                old_rule.name, "logging", old_rule.log_end, new_rule.log_end
            )
        )
    return changes


def list_changed_rules(changed_rules):
    """
    Displays firewall rule changes between two configurations.

    Prints modified rules with their individual field changes, followed by
    the details of added and deleted rules.

    Args:
         changed_rules: Dictionary containing categorized firewall rule changes.
    """
    all_fw_modified = []
    for old_rule, new_rule in changed_rules["modified"]:

        fwchanges = get_field_changes(old_rule, new_rule)
        all_fw_modified.extend(fwchanges)

    print(f"modified rules ({len(changed_rules['modified'])}):")
    for change in all_fw_modified:
        print(
            f"{change.name}: "
            f"{change.field}: "
            f"{change.old_value} -> {change.new_value}"
        )

    # listing added rule
    all_fw_added = list(changed_rules["added"])

    print(f"\nadded rules ({len(all_fw_added)}): ")
    for change in all_fw_added:
        print(
            f" {change.name}\n"
            f"   source: {change.source}\n"
            f"   destination: {change.destination}\n"
            f"   application: {change.application}\n"
            f"   description: {change.description}\n"
            f"   disabled: {change.disabled}\n"
            f"   logging: {change.log_end}"
        )

    # listing deleted rules
    all_fw_deleted = list(changed_rules["deleted"])

    print(f"\ndeleted rules ({len(all_fw_deleted)}): ")
    for change in all_fw_deleted:
        print(
            f" {change.name}\n"
            f"   source: {change.source}\n"
            f"   destination: {change.destination}\n"
            f"   application: {change.application}\n"
            f"   description: {change.description}\n"
            f"   disabled: {change.disabled}\n"
            f"   logging: {change.log_end}"
        )


def display_findings(results):
   """
   Displays the results of a security finding comparison.

   Prints new, resolved, and persistent findings, including their rule names,
   issue identifiers, severity levels, and descriptions.

   Args:
      results: Dictionary containing categorized finding comparison results.
   """ 
   print("\nFINDING COMPARISON")
   print("------------------------------")

   for category, findings in results.items():
       print(f"\n{category.upper()} ({len(findings)}):")

       if not findings:
           print("  None")
           continue

       for finding in findings:
           print(
               f"  Rule: {finding.rule}\n"
               f"  Issue: {finding.issue}\n"
               f"  Severity: {finding.severity}\n"
               f"  Message: {finding.message}\n"
            )


