from cli import ParseArgs
from services import getEmails, getSummary
import sys



def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError, TypeError):
        # sys.stdout may not support reconfigure (e.g., when redirected or on some Python versions)
        pass
    args = ParseArgs()
    if args.mode == "overview":
        summary = getSummary(args.searchterm, args.sortby, args.email, args.searchnumber)
        print(summary)
        return summary
    else:  # emails mode
        emails = getEmails(args.searchterm, args.sortby, args.email, args.searchnumber)
        print(emails)
        return emails








if __name__ == "__main__":
    main()

