import argparse
import json
import sys
import statsapi


def main():
    parser = argparse.ArgumentParser(description="PowerShell wrapper for statsapi")
    parser.add_argument("function", help="Function name from statsapi to call")
    parser.add_argument("--params", default="{}", help="JSON string of parameters")
    args = parser.parse_args()

    try:
        params = json.loads(args.params)
    except json.JSONDecodeError as exc:
        print(f"Failed to parse parameters: {exc}", file=sys.stderr)
        return 1

    try:
        func = getattr(statsapi, args.function)
    except AttributeError:
        print(f"Function '{args.function}' not found in statsapi", file=sys.stderr)
        return 1

    result = func(**params)
    json.dump(result, sys.stdout, default=str)
    return 0


if __name__ == "__main__":
    sys.exit(main())
