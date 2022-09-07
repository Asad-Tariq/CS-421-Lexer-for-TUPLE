from lexer import *


def main():
    # open test file
    with open("Tests\\test02.tpl") as custom_test:
        lines = custom_test.readlines()

    # pass the input stream line by line
    for line in lines:
        # initialize Lexer for the given portion of the stream
        lexer = Lexer(line)
        while lexer.peek() != '\0':
            # tokenize the given line
            print(lexer.getToken())


if __name__ == "__main__":
    main()
