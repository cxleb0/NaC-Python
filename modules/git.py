import subprocess


command = subprocess.run (
    [
        "git",
        "diff",
        "50c6d29",
        "26dd0e0",
        "--",
        "../configs/config2.xml"
    ],
    capture_output=True,
    text=True,
    check=True
)
print(command.stdout)
