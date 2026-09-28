import subprocess


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

def list_revision_changes(old_rules:list, new_rules:list):
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
                changes["modified"].append(rule)
    for rule in old_rules:
        if rule.name not in newrule_name:
            #check for deleted
                changes["deleted"].append(rule)
    return changes
    
