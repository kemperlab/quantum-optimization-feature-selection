from .problem.parser import get_main_parser

if __name__ == "__main__":
    parser = get_main_parser()
    arguments = parser.parse_args()

    func = arguments.func
    delattr(arguments, "func")

    func(arguments)
