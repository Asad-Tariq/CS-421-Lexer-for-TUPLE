from lexer import *


def write_token_stream(token_stream, file_num):
    # write the file
    with open(f'TokenStream\\test0{file_num}.out', "w") as stream:
        stream.write(''.join(token_stream.values()))


def write_symb_tbl(symbol_table, file_num):
    # write the file
    with open(f'SymbolTable\\test0{file_num}.sym', "w") as table:
        table.write("{:<8} {:<15}".format('Key', 'Symbol'))
        table.write('\n')
        for k, v in symbol_table.items():
            table.write("{:<8} {:<15}\n".format(k, v))


def write_error_stream(error_stream, file_num):
    # write the file
    with open(f'ErrorStream\\test0{file_num}.err', "w") as error:
        error.write("{:<8} {:<15}".format('<line#>', '<error_found>'))
        error.write('\n')
        for k, v in error_stream.items():
            for i in v:
                error.write("{:<8} {:<15}\n".format(k + 1, i))


def tokenize(lexer, symbol_table, symbol_count, error_stream, token_stream, line_num):
    # keep tokenizing till EOF encountered
    while lexer.peek() != '\0':
        # tokenize the given line
        token, new_symbl_tbl, new_symb_count, error = lexer.get_token()

        # add the new token to the current line's stream
        try:
            token_stream[line_num] += token
        except KeyError:
            token_stream[line_num] = token

        # update the symbol table
        symbol_table = new_symbl_tbl
        symbol_count = new_symb_count

        # update record of errors
        if error != "":
            try:
                error_stream[line_num].append(error)
            except KeyError:
                error_stream[line_num] = [error]

    return symbol_count, symbol_table


def main():
    # ask user for file number
    file_num = input("Enter the file number: ")

    # open the test file and read it
    with open(f'Tests\\test0{file_num}.tpl') as custom_test:
        lines = custom_test.readlines()

    # initialize all streams
    symbol_count = 1
    symbol_table = {}
    error_stream = {}
    token_stream = {}

    # pass the input stream line by line
    for i in range(len(lines)):
        # initialize Lexer for the given portion of the stream
        lexer = Lexer(lines[i], symbol_table, symbol_count)

        # tokenize the line
        symbol_count, symbol_table = tokenize(lexer, symbol_table, symbol_count,
                                              error_stream, token_stream, i)

    # output the token stream to file
    write_token_stream(token_stream, file_num)

    # output the symbol table
    write_symb_tbl(symbol_table, file_num)

    # output the error stream
    write_error_stream(error_stream, file_num)


# driver code
if __name__ == "__main__":
    main()
