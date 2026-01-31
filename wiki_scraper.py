import classes.dispatcher as dispatcher
import terminal_parsing as parser

def main():
    args = parser.parse_arguments()

    dispatch = dispatcher.Dispatcher(args)

    dispatch.run()

if __name__ == "__main__":
    main()