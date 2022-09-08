from lexer import *


def main():
    # open test file
    with open("Tests\\test02.tpl") as custom_test:
        lines = custom_test.readlines()

    # Save token stream
    token_stream = {}

    for i in range(len(lines)):
        token_stream[i] = ""

    # pass the input stream line by line
    for i in range(len(lines)):
        # initialize Lexer for the given portion of the stream
        lexer = Lexer(lines[i])
        while lexer.peek() != '\0':
            # tokenize the given line
            token_stream[i] += lexer.getToken()[0]

    with open("TokenStream\\stream02.out", "w") as stream:
        stream.write('\n'.join(token_stream.values()))

if __name__ == "__main__":
    main()
