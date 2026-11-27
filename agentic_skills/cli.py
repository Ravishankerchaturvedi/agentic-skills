"""CLI for the agentic-skills checker.

    agentic-skills check [path] [--banned-file FILE] [--no-private] [--json]

Exit codes: 0 = pass, 1 = problems found, 2 = bad input.
"""

import argparse
import sys

from . import __version__
from . import core


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="agentic-skills",
        description="Check a library of agent skills (SKILL.md files) against "
                    "the house rules: frontmatter, names, descriptions, "
                    "references and private-data markers.")
    parser.add_argument("--version", action="version",
                        version="agentic-skills %s" % __version__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check", help="check a skill library (default: .)")
    p.add_argument("path", nargs="?", default=".",
                   help="library root to check (default: current directory)")
    p.add_argument("--banned-file", dest="banned_file", default=None,
                   help="file of extra private-marker regexes, one per line")
    p.add_argument("--no-private", action="store_true", dest="no_private",
                   help="skip the private-marker scan")
    p.add_argument("--json", action="store_true", dest="as_json",
                   help="print one JSON object")

    args = parser.parse_args(argv)

    if args.cmd == "check":
        try:
            report = core.check_library(args.path,
                                        banned_file=args.banned_file,
                                        no_private=args.no_private)
        except OSError as e:
            print("ERROR: %s" % e, file=sys.stderr)
            return 2
        if args.as_json:
            print(core.report_json(report))
        else:
            print(core.report_text(report))
        if report.get("code") == "BAD_INPUT":
            return 2
        return 0 if report["ok"] else 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
