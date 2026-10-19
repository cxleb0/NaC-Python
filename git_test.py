from modules.git import (get_diff,
                         get_file_at_revision,
                         list_revision_changes,
                         get_field_changes,
                         gitcli)

from modules.parser import get_rules
from modules.policy_loader import load_policies
from modules.audit_engine import generate_findings
 
args = gitcli()
difference = get_diff(args.old_config, args.new_config, "configs/config2.xml")
old_revision = get_file_at_revision(args.old_config, "configs/config2.xml")
new_revision = get_file_at_revision(args.new_config, "configs/config2.xml")
old_rules = get_rules(old_revision)
new_rules = get_rules(new_revision)
changed_rules = list_revision_changes(old_rules, new_rules)



#listing modified rules
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


#listing added rules
all_fw_added = []
for rule in changed_rules["added"]:
    all_fw_added.append(rule)

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
    
#listing deleted rules
all_fw_deleted = []
for rule in changed_rules["deleted"]:
    all_fw_deleted.append(rule)

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

policies = load_policies(args.policy)
old_findings = generate_findings(old_rules, policies)
new_findings = generate_findings(new_rules, policies)
print(old_findings)
print(new_findings)
