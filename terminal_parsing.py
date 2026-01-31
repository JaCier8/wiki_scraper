import argparse
import classes.page as Page
import wiki_scraper_functions as wsf

def parse_arguments():

    # Main args parsing
    parser = argparse.ArgumentParser(description='Wiki Scraper Tool')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--summary', type=str, help='--summary "article name",'
                                                   '  gives summary from page'
                       )
    group.add_argument('--table', type=str, help='--table "article name" --number n [--first-row-is-header]'
                                                 ',  gives n-th table from page'
                       )
    group.add_argument(
                        '--analyze-relative-word-frequency',
                        action='store_true',
                        dest='analyze',
                        help='--analyze-relative-word-frequency --mode mode --count n [--chart "path/to/file.png"]'
    )
    group.add_argument('--count-words',
                       type=str,
                       help='--count-words "szukana fraza"')
    group.add_argument(
                        '--auto-count-words',
                        type=str,
                        help='--auto-count-words "starting article name" --depth n --wait t,  '
                             'does bfs of count_words form'
    )
    # Summary args NONE

    # Table args
    parser.add_argument('--number',
                        type=int,
                        help='number of table to show'
                        )
    parser.add_argument('--first-row-is-header',
                        action='store_true',
                        help='Add this to make first row a header')

    # Graph args

    parser.add_argument(
                        '--mode',
                        type=str,
                        choices=['article', 'language'],
                        help='Choose to show comparison type'
    )
    parser.add_argument(
                        '--count',
                        type=int,
                        help='Choose to show number of words on chart'
    )
    parser.add_argument(
                        '--chart',
                        type=str,
                        default=None,
                        help='Add path for creating a chart',
    )
    # Auto count words

    parser.add_argument(
                        '--depth',
                        type=int,
                        help='Choose depth of web scrapping'
    )
    parser.add_argument(
                        '--wait',
                        type=float,
                        help='Choose waiting time between individual scrapes '
                             'to avoid getting blocked by website'
    )


    args = parser.parse_args()

    if args.summary:
        if args.number or args.depth or args.wait or args.mode or args.count:
            parser.error("Summary has no attributes")
        return args

    if args.table:
        if args.number is None:
            parser.error("Number not given")
        if args.mode or args.count or args.depth or args.wait:
            parser.error("Can't use: --mode, --count, --depth, any other")
        return args

    if args.count_words:
        if args.mode or args.depth or args.wait or args.count or args.number:
            parser.error("Count words has no attributes")
        return args

    if args.analyze:
        if not args.mode or not args.count:
            parser.error("Count and mode not given")
        if args.number or args.depth or args.wait:
            parser.error("Can't use: --number, --depth, --wait, any other")
        return args

    if args.auto_count_words:
        if args.depth is None or args.wait is None:
            parser.error("Wait or depth not given")
        if args.number or args.mode or args.count:
            parser.error("Can't use: --number, --mode, --count, any other")
        return args

    return args


