import subprocess
from modules.module import (FirewallRule, RuleFieldChange)
import argparse

def get_diff(old_version: str, new_version:str, file_path:str):
    command = subprocess.run(
        [
            "git",
            "diff",
            old_version,
            new_version,
            "--",
            file_path
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return command.stdout

def get_file_at_revision(revision: str, file_path:str) -> str:
    command = subprocess.run(
        [
            "git",
            "show",
            f"{revision}:{file_path}"
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return command.stdout

def list_revision_changes(old_rules:list, new_rules:list) -> dict:
    #fw rule name will act as the key
    changes = {
        "added": [],
        "modified": [],
        "unmodified": [],
        "deleted": []
    }
    newrule_name = {rule.name: rule for rule in new_rules}
    oldrule_name = {rule.name: rule for rule in old_rules}
    for rule in new_rules:
        if rule.name not in oldrule_name:
            #check for added
            changes["added"].append(rule)
        else:
            old_rule = oldrule_name[rule.name]
            #existed before
            if rule == old_rule:
                #unmodified
                changes["unmodified"].append(rule)
            else:
                #modified
                changes["modified"].append((old_rule, rule))
    for rule in old_rules:
        if rule.name not in newrule_name:
            #check for deleted
            changes["deleted"].append(rule)
    return changes

def get_field_changes(old_rule:FirewallRule, new_rule:FirewallRule) -> list:
    changes = []
    if old_rule.source != new_rule.source:
        changes.append(RuleFieldChange(old_rule.name, "source", old_rule.source, new_rule.source))
    if old_rule.destination != new_rule.destination:
        changes.append(RuleFieldChange(old_rule.name, "destination", old_rule.destination, new_rule.destination))
    if (old_rule.application != new_rule.application):
        changes.append(RuleFieldChange(old_rule.name, "application", old_rule.application, new_rule.application))
    if old_rule.description != new_rule.description:
        changes.append(RuleFieldChange(old_rule.name, "description", old_rule.description, new_rule.description))
    if old_rule.disabled != new_rule.disabled:
        changes.append(RuleFieldChange(old_rule.name, "disabled", old_rule.disabled, new_rule.disabled))
    if old_rule.log_end != new_rule.log_end:
        changes.append(RuleFieldChange(old_rule.name, "logging", old_rule.log_end, new_rule.log_end))
    return changes

parser=argparse.ArgumentParser(description="Arguments")
def gitcli():
    parser.add_argument(
        "--old_config",
        required=True,
    )
    parser.add_argument(
        "--new_config",
        required=True,
    )
    parser.add_argument(
        "--policy",
        required=True,
        help="Directory where yaml policies reside."
    )
    return parser.parse_args()

