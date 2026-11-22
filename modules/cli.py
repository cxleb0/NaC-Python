import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Firewall Policy Engine")


def cli():
    parser.add_argument(
        "--config", required=True, help="Directory where XML configurations reside."
    )
    parser.add_argument(
        "--policy", required=True, help="Directory where yaml policies reside."
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("reports"),
        help="Where to save generated reports,",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "xml", "all"],
        default="all",
        help="Format to generate reports.",
    )
    parser.add_argument(
        "--git", action="store_true", help="Enable Git-based configuration auditing."
    )
    parser.add_argument(
        "--old_config", help="Git revision containing the older firewall configuration."
    )
    parser.add_argument(
        "--new_config", help="Git revsion containing the newer firewall configuration."
    )
    args = parser.parse_args()

    if args.git:
        if not args.old_config or not args.new_config:
            parser.error("--git requires both old configuration and new configuration.")
    elif args.old_config or args.new_config:
        parser.error("--old_config and --new_config require --git.")

    return args
