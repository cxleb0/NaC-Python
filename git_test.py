from modules.git import (get_diff,
                         get_file_at_revision,
                         list_revision_changes)
from modules.parser import get_rules



difference = get_diff("50c6d29", "26dd0e0", "configs/config2.xml")
old_revision = get_file_at_revision("50c6d29", "configs/config2.xml")
new_revision = get_file_at_revision("26dd0e0", "configs/config2.xml")
print(difference)
print("OLD CONFIG:")
print(old_revision)
print("NEW CONFIG:")
print(new_revision)


old_rules = get_rules(old_revision)
new_rules = get_rules(new_revision)
print("OLD RULES:")
print(old_rules)
print("NEW RULES:")
print(new_rules)

print("CHANGES: ")
changed_rules = list_revision_changes(old_rules, new_rules)
print(changed_rules)

