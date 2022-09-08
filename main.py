from lexer import *


def main():
    # open test file
    with open("Tests\\test03.tpl") as custom_test:
        lines = custom_test.readlines()

    # Save token stream
    token_stream = {}

    # Save the symbol table
    symbol_table = {}
    symbol_count = 1

    for i in range(len(lines)):
        token_stream[i] = ""

    # pass the input stream line by line
    for i in range(len(lines)):
        # initialize Lexer for the given portion of the stream
        lexer = Lexer(lines[i], symbol_table, symbol_count)
        while lexer.peek() != '\0':
            # tokenize the given line
            token = lexer.getToken()
            token_stream[i] += token[0][0]
            symbol_table = token[1]
            symbol_count = token[2]

    with open("TokenStream\\stream03.out", "w") as stream:
        stream.write('\n'.join(token_stream.values()))

    with open("SymbolTable\\table03.sym", "w") as table:
        table.write("{:<8} {:<15}".format('Key','Symbol'))
        table.write('\n')
        for k, v in symbol_table.items():
            table.write("{:<8} {:<15}".format(k,v))
            table.write('\n')

if __name__ == "__main__":
    main()
