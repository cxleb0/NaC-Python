import argparse
from pathlib import Path
parser = argparse.ArgumentParser(description="Firewall Policy Engine")
def cli():
    parser.add_argument(
        "--config",
        required=True,
        help="Directory where XML configurations reside."
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("reports"),
        required=True,
        help="Where to save generated reports,"
    )
    parser.add_argument(
        "--format",
        choices=["csv","json","xml","all"],
        default="all",
        help="Format to generate reports."
    )
    return parser.parse_args()
