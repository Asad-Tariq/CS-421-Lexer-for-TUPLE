from lexer import *


def main():
    # open test file

    file_num = input("Enter the file number: ")

    with open("Tests\\test0" + file_num + ".tpl") as custom_test:
        lines = custom_test.readlines()

    # Save token stream
    token_stream = {}

    # Save the symbol table
    symbol_table = {}
    symbol_count = 1

    # Save the error stream
    error_stream = {}

    for i in range(len(lines)):
        token_stream[i] = ""

    # pass the input stream line by line
    for i in range(len(lines)):
        # initialize Lexer for the given portion of the stream
        lexer = Lexer(lines[i], symbol_table, symbol_count)
        while lexer.peek() != '\0':
            # tokenize the given line
            token = lexer.getToken()
            token_stream[i] += token[0]
            symbol_table = token[1]
            symbol_count = token[2]
            if len(token[3]) > 0:
                error_stream[i] = token[3]

    with open("TokenStream\\stream0" + file_num + ".out", "w") as stream:
        stream.write(''.join(token_stream.values()))

    with open("SymbolTable\\table0" + file_num + ".sym", "w") as table:
        table.write("{:<8} {:<15}".format('Key','Symbol'))
        table.write('\n')
        for k, v in symbol_table.items():
            table.write("{:<8} {:<15}".format(k,v))
            table.write('\n')

    with open("ErrorStream\\error0" + file_num + ".err", "w") as error:
        error.write("{:<8} {:<15}".format('<line#>','<error_found>'))
        error.write('\n')
        for k, v in error_stream.items():
            error.write("{:<8} {:<15}".format(k + 1,v))
            error.write('\n')


# driver code
if __name__ == "__main__":
    main()
