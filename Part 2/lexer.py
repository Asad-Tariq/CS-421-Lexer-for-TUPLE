from tuple_spec import *


class Lexer:
    def __init__(self, input_stream, symbol_table, symbol_count) -> None:
        self.input = input_stream + '\n'
        self.cur_char = ''
        self.cur_pos = -1
        self.symbol_table = symbol_table
        self.symbol_count = symbol_count
        self.error = ""
        self.next_char()

    # Process the next character
    def next_char(self):
        self.cur_pos += 1
        if self.cur_pos >= len(self.input):
            self.cur_char = '\0'  # EOF char
        else:
            self.cur_char = self.input[self.cur_pos]

    # Return the lookahead character
    def peek(self):
        if self.cur_pos + 1 >= len(self.input):
            return '\0'
        return self.input[self.cur_pos + 1]

    # Detect comment
    def check_comment(self):
        tok = ""
        if self.peek() == "$":
            self.next_char()
            self.next_char()
            while self.cur_char != "$":
                self.next_char()
            if self.peek() == "/":
                tok = "<Comment>"
                self.next_char()
                self.next_char()
            elif self.peek() == "\n":
                tok = "<Invalid Comment>"
                self.error = "Comment not closed properly!"
                while self.cur_char != "\n":
                    self.next_char()
            elif self.peek() == "$":
                while self.peek() != "/":
                    self.next_char()
                if self.peek() == "/":
                    tok = "<comment>"
                    self.next_char()
                    self.next_char()
        elif self.cur_char in arithmetic_op:
            tok = "<" + self.cur_char + ">"
            self.next_char()

        return tok

    # Detect keyword, datatype, identifier
    def check_key_dt_id(self):
        save_string = ""
        tok = ""
        while self.cur_char in letters or self.cur_char in digits or self.cur_char in underscore:
            save_string += self.cur_char
            self.next_char()
        if self.cur_char == ".":
            tok = "<Invalid identifier!>"
            self.error = f'{save_string}{self.cur_char} (Invalid Identifier!)'
            self.next_char()
        elif self.cur_char not in whitespaces.keys() and self.cur_char not in punctuation\
                and self.cur_char not in arithmetic_op:
            tok = "<Invalid Identifier!>"
            self.error = f'{save_string} (Invalid Identifier!)'
        elif save_string in keywords:
            tok = "<keyword, " + save_string + ">"
        elif save_string in data_types:
            tok = "<dt, " + save_string + ">"
        else:
            tok = "<id, " + save_string + ">"
            if save_string + ", id" not in self.symbol_table.values():
                self.symbol_table[self.symbol_count] = save_string + ", id"
                self.symbol_count += 1
        return tok

    # Detect float numbers
    def checkFloat(self):
        save_string = ""
        if self.peek() not in digits and self.peek() != "E":
            while self.cur_char != "\n":
                save_string += self.cur_char
                self.next_char()
            return save_string, False
        else:
            save_string += self.cur_char
            self.next_char()
            if self.cur_char in digits:
                if self.peek() in [punc for punc in punctuation if punc != "."]\
                        or self.peek() in whitespaces.keys():
                    save_string += self.cur_char
                    self.next_char()
                    return save_string, True
                if self.peek() == "E":
                    save_string += self.cur_char
                    self.next_char()
                    if self.peek() in digits or self.peek() in letters:
                        while self.cur_char != "\n":
                            save_string += self.cur_char
                            self.next_char()
                        return save_string, False
                    else:
                        save_string += self.cur_char
                        self.next_char()
                        return save_string, True 
                elif self.peek() in digits:
                    while self.cur_char in digits:
                        save_string += self.cur_char
                        self.next_char()
                    if self.cur_char in [punc for punc in punctuation if punc != "."]\
                            or self.cur_char in whitespaces.keys():
                        return save_string, True
                    if self.cur_char not in digits:
                        if self.cur_char == "E":
                            if self.peek() not in digits:
                                while self.cur_char not in [punc for punc in punctuation if punc != "."]\
                                        and self.cur_char not in whitespaces.keys():
                                    save_string += self.cur_char
                                    self.next_char()
                                return save_string, True
                        while self.cur_char != "\n":
                            save_string += self.cur_char
                            self.next_char()
                        return save_string, False
                    if self.peek() == "E":
                        save_string += self.cur_char
                        self.next_char()
                        if self.peek() in digits or self.peek() in letters:
                            while self.cur_char != "\n":
                                save_string += self.cur_char
                                self.next_char()
                            return save_string, False
                        else:
                            save_string += self.cur_char
                            self.next_char()
                            return save_string, True
                    else:
                        return save_string, True
                else:
                    while self.cur_char not in [punc for punc in punctuation if punc != "."]\
                            and self.cur_char not in whitespaces.keys():
                        save_string += self.cur_char
                        self.next_char()
                    return save_string, False 
            else:
                while self.cur_char != "\n":
                    save_string += self.cur_char
                    self.next_char()
                return save_string, False

    # Detect digits
    def check_digit(self):
        save_string = ""
        tok = ""
        if self.peek() in letters:
            tok = "<Unsupported character>"
            self.error = f'{save_string} (Unsupported character found with digit!)'
        else:
            while self.cur_char in digits:
                save_string += self.cur_char
                self.next_char()
            if self.cur_char == ".":
                floatString, isFloat = self.checkFloat()
                if isFloat:
                    tok = f'<float, {save_string}{floatString}>'
                else:
                    tok = "<Invalid Float!>"
                    self.error = f'{save_string}{floatString} (Invalid Float!)'
            else:
                tok = "<num, " + save_string + ">"

        return tok

    # Detect arithmetic operator
    def check_arith_op(self):
        save_string = ""
        if self.cur_char == "-" and self.peek() in digits:
            save_string += self.cur_char
            self.next_char()
            while self.cur_char in digits:
                save_string += self.cur_char
                self.next_char()
            tok = f'<num, {save_string}>'
        else:
            tok = f'<{self.cur_char}>'
            self.next_char()
        return tok

    # Detect assignment operator
    def check_assign_op(self):
        if self.peek() != "=":
            tok = f'<assign, {self.cur_char}>'
            self.next_char()
            return tok
        else:
            tok = self.check_rel_op()
            self.next_char()

        return tok

    # Detect relational operator
    def check_rel_op(self):
        if self.peek() == "=":
            key = self.cur_char + "="
            tok = f'<rel_op, {relational_op_double[key]}>'
            self.next_char()
            self.next_char()
        else:
            key = self.cur_char
            tok = f'<rel_op, {relational_ops_single[key]}>'
            self.next_char()

        return tok

    # Detect string literal
    def check_string_literal(self):
        save_string = ""
        self.next_char()
        while self.cur_char != "\"":
            save_string += self.cur_char
            self.next_char()
        tok = f'<literal, {save_string}>'
        self.next_char()

        return tok

    # Detect character constant
    def check_char_const(self):
        save_string = self.cur_char
        self.next_char()
        while self.cur_char != "'" and self.cur_char != "\n" and self.cur_char not in punctuation:
            save_string += self.cur_char
            self.next_char()
        if len(save_string) == 1:
            tok = f'<char_constant, {save_string}>'
        else:
            tok = f'<Invalid char constant!, {save_string}>'
            self.error = f'{save_string} (Invalid char constant!)'
        if self.peek() != "\0":
            self.next_char()

        return tok

    # Detect punctuation
    def check_punctuation(self):
        tok = f'<punctuator, {self.cur_char}>'
        self.next_char()
        return tok

    # Detect whitespaces
    def check_whitespaces(self):
        tok = f'<{whitespaces[self.cur_char]}>'
        self.next_char()
        return tok

    # Return the next token
    def get_token(self):
        token = ""
        if self.cur_char == "/":
            token = self.check_comment()
        elif self.cur_char in letters:
            token = self.check_key_dt_id()
        elif self.cur_char in digits:
            token = self.check_digit()
        elif self.cur_char in arithmetic_op:
            token = self.check_arith_op()
        elif self.cur_char in assignment:
            token = self.check_assign_op()
        elif self.cur_char in relational_ops_single:
            token = self.check_rel_op()
        elif self.cur_char == "\"":
            token = self.check_string_literal()
        elif self.cur_char == "'":
            token = self.check_char_const()
        elif self.cur_char in punctuation:
            token = self.check_punctuation()
        elif self.cur_char in whitespaces.keys():
            token = self.check_whitespaces()
        else:
            token = self.error = "<Character not recognised!>"

        # reset error string for next token
        err_cpy = self.error
        self.error = ""

        return token, self.symbol_table, self.symbol_count, err_cpy
