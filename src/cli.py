from constants import APPLICATION_OUTPUT_OPTIONS, PUBMED_SORT_OPTIONS
import argparse


def ParseArgs():
    parser = argparse.ArgumentParser(prog="PubMedSearch")
    parser.add_argument("searchterm", help="Topic you want to search")
    parser.add_argument(
        "-m",
        "--mode",
        choices=APPLICATION_OUTPUT_OPTIONS,
        default="overview",
        help="Chooses the output type for the application",
    )
    parser.add_argument("-e", "--email", type=str, default="")
    parser.add_argument(
        "-n", "--searchnumber", type=int, default=10, help="Number of results you want"
    )
    parser.add_argument(
        "-s",
        "--sortby",
        choices=PUBMED_SORT_OPTIONS,
        default="relevance",
        help="Sort order for Pubmed Search",
    )
    return parser.parse_args()