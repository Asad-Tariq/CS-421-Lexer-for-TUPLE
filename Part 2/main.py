from lexer import *
from typing import List, Dict, Tuple


def write_token_stream(token_stream: Dict[int, str], file_num: int) -> None:
    """Writes the generated token stream from the lexical analysis to a file
    of the same name as the input file with the .out extension.

    Args:
    - token_stream: all the tokenized lexemes.
    - file_num: the test number of the file that was read.

    Returns:
    None.
    """

    # write the file
    with open(f'TokenStream\\test0{file_num}.out', "w") as stream:
        # the entire stream is written in a single line
        stream.write(''.join(token_stream.values()))


def write_symb_tbl(symbol_table: Dict[int, str], file_num: int) -> None:
    """Writes the symbol table generated from the lexical analysis to a file
    of the same name as the input with the .sym extension.

    Args:
    - symbol_table: all recorded entries in the symbol table.
    - file_num: the test number of the file that was read.

    Returns:
    None.
    """

    # write the file
    with open(f'SymbolTable\\test0{file_num}.sym', "w") as table:
        table.write("{:<8} {:<15}\n".format('Key', 'Symbol'))
        for ix, entry in symbol_table.items():
            table.write("{:<8} {:<15}\n".format(ix, entry))


def write_error_stream(error_stream: Dict[int, List[str]], file_num: int) -> None:
    """Writes the error stream generated from the lexical analysis to a file
    of the same name as the input with the .err extension.

    Args:
    - error_stream: all errors recorded during the lexical analysis.
    - file_num: the test number of the file that was read.

    Returns:
    None.
    """

    # write the file
    with open(f'ErrorStream\\test0{file_num}.err', "w") as error:
        error.write("{:<8} {:<15}\n".format('<line#>', '<error_found>'))
        for line, errors in error_stream.items():
            for err in errors:
                error.write("{:<8} {:<15}\n".format(line + 1, err))


def tokenize(lexer: Lexer, symbol_table: Dict[int, str], symbol_count: int,
             error_stream: Dict[int, List[str]], token_stream: Dict[int, str],
             line_num: int) -> Tuple[int, Dict[int, str]]:
    """Tokenizes the given portion of the input stream - the line being
    read.

    Args:
    - lexer: object reference for the lexer instantiated with the current
    portion of the input stream.
    - symbol_table: the symbol table maintained for the lexical analysis.
    - symbol_count: an integer corresponding to the number of entries in
    the symbol table.
    - error_stream: a dictionary recording errors encountered (by line).
    - token_stream: a dictionary recording the tokenized lexemes (by line).
    - line_num: the number of the line/portion of the input stream that is
    being processed.

    Returns:
    updated values for the symbol count and table.
    """

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


def main() -> None:
    """Program entry point. Reads the indicated test file line by line, passing
    each line to the lexer which tokenizes the given stream in addition to,
    recording any errors and populating the symbol table.

    After completion of the lexical analysis, all the streams - i.e., token, symbol
    and error are written to their respective files.

    Args:
    None.

    Returns:
    None.
    """

    # ask user for file number
    file_num = int(input("Enter the file number: "))

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
