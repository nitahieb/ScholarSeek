

from cli import ParseArgs
from services import getEmails, getSummary



def main():
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

