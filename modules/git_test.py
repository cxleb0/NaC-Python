from modules.git import get_diff




difference = get_diff("50c6d29", "26dd0e0", "configs/config2.xml")
print(difference)
