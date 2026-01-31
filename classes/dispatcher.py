import terminal_parsing as tpr
import wiki_scraper_functions as wsf
import classes.page as Page

"""
Class responsible for dispatching tasks based on given arguements
"""

class Dispatcher:
    def __init__(self, args):
        self.args = args

    def run(self):
        args = self.args

        if args.summary:
            current_page = Page.Page(args.summary)
            wsf.get_summary(current_page)


        elif args.table:
            current_page = Page.Page(args.table)

            wsf.nth_table(
                n=args.number,
                page=current_page,
                csv_name=args.table,
                first_row_is_header=args.first_row_is_header
            )


        elif args.analyze:
            by_wiki_bool = (args.mode == 'article')

            wsf.analyze_ferquency(
                by_wiki=by_wiki_bool,
                n=args.count,
                file_name=args.chart
            )

        elif args.count_words:

            current_page = Page.Page(args.count_words)

            wsf.word_counter(current_page)

        elif args.auto_count_words:

            wsf.auto_count(args.auto_count_words,
                           wait=args.wait,
                           depth=args.depth)


