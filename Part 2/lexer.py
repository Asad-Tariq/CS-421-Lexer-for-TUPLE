from tuple_spec import *


class Lexer:
    def __init__(self, input_stream, symbol_table, symbol_count) -> None:
        self.input = input_stream + '\n'
        self.curChar = ''
        self.curPos = -1
        self.symbol_table = symbol_table
        self.symbol_count = symbol_count
        self.error = ""
        self.nextChar()

    # Process the next character
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.input):
            self.curChar = '\0'  # EOF char
        else:
            self.curChar = self.input[self.curPos]

    # Return the lookahead character
    def peek(self):
        if self.curPos + 1 >= len(self.input):
            return '\0'
        return self.input[self.curPos + 1]

    # Detect comment
    def checkComment(self):
        tok = ""
        if self.peek() == "$":
            self.nextChar()
            self.nextChar()
            while self.curChar != "$":
                self.nextChar()
            if self.peek() == "/":
                tok = "<Comment>"
                self.nextChar()
                self.nextChar()
            elif self.peek() == "\n":
                tok = "<Invalid Comment>"
                self.error = "Comment not closed properly!"
                while self.curChar != "\n":
                    self.nextChar()
            elif self.peek() == "$":
                while self.peek() != "/":
                    self.nextChar()
                if self.peek() == "/":
                    tok = "<comment>"
                    self.nextChar()
                    self.nextChar()
        elif self.curChar in arithmetic_op:
            tok = "<" + self.curChar + ">"
            self.nextChar()

        return tok

    # Detect keyword, datatype, identifier
    def checkKeyDtId(self):
        save_string = ""
        tok = ""
        while self.curChar in letters or self.curChar in digits or self.curChar in underscore:
            save_string += self.curChar
            self.nextChar()
        if self.curChar == ".":
            tok = "<Invalid identifier!>"
            self.error = f'{save_string}{self.curChar} (Invalid Identifier!)'
            self.nextChar()
        elif self.curChar not in whitespaces.keys() and self.curChar not in punctuation\
                and self.curChar not in arithmetic_op:
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
            while self.curChar != "\n":
                save_string += self.curChar
                self.nextChar()
            return save_string, False
        else:
            save_string += self.curChar
            self.nextChar()
            if self.curChar in digits:
                if self.peek() in [punc for punc in punctuation if punc != "."]\
                        or self.peek() in whitespaces.keys():
                    save_string += self.curChar
                    self.nextChar()
                    return save_string, True
                if self.peek() == "E":
                    save_string += self.curChar
                    self.nextChar()
                    if self.peek() in digits or self.peek() in letters:
                        while self.curChar != "\n":
                            save_string += self.curChar
                            self.nextChar()
                        return save_string, False
                    else:
                        save_string += self.curChar
                        self.nextChar()
                        return save_string, True 
                elif self.peek() in digits:
                    while self.curChar in digits:
                        save_string += self.curChar
                        self.nextChar()
                    if self.curChar in [punc for punc in punctuation if punc != "."]\
                            or self.curChar in whitespaces.keys():
                        return save_string, True
                    if self.curChar not in digits:
                        if self.curChar == "E":
                            if self.peek() not in digits:
                                while self.curChar not in [punc for punc in punctuation if punc != "."]\
                                        and self.curChar not in whitespaces.keys():
                                    save_string += self.curChar
                                    self.nextChar()
                                return save_string, True
                        while self.curChar != "\n":
                            save_string += self.curChar
                            self.nextChar()
                        return save_string, False
                    if self.peek() == "E":
                        save_string += self.curChar
                        self.nextChar()
                        if self.peek() in digits or self.peek() in letters:
                            while self.curChar != "\n":
                                save_string += self.curChar
                                self.nextChar()
                            return save_string, False
                        else:
                            save_string += self.curChar
                            self.nextChar()
                            return save_string, True
                    else:
                        return save_string, True
                else:
                    while self.curChar not in [punc for punc in punctuation if punc != "."]\
                            and self.curChar not in whitespaces.keys():
                        save_string += self.curChar
                        self.nextChar()
                    return save_string, False 
            else:
                while self.curChar != "\n":
                    save_string += self.curChar
                    self.nextChar()
                return save_string, False

    # Detect digits
    def checkDigit(self):
        save_string = ""
        tok = ""
        if self.peek() in letters:
            tok = "<Unsupported character>"
            self.error = f'{save_string} (Unsupported character found with digit!)'
        else:
            while self.curChar in digits:
                save_string += self.curChar
                self.nextChar()
            if self.curChar == ".":
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
    def checkArithOp(self):
        save_string = ""
        if self.curChar == "-" and self.peek() in digits:
            save_string += self.curChar
            self.nextChar()
            while self.curChar in digits:
                save_string += self.curChar
                self.nextChar()
            tok = f'<num, {save_string}>'
        else:
            tok = f'<{self.curChar}>'
            self.nextChar()
        return tok

    # Detect assignment operator
    def checkAssignOp(self):
        if self.peek() != "=":
            tok = f'<assign, {self.curChar}>'
            self.nextChar()
            return tok
        else:
            tok = self.checkRelOp()
            self.nextChar()

        return tok

    # Detect relational operator
    def checkRelOp(self):
        if self.peek() == "=":
            key = self.curChar + "="
            tok = f'<rel_op, {relational_op_double[key]}>'
            self.nextChar()
            self.nextChar()
        else:
            key = self.curChar
            tok = f'<rel_op, {relational_ops_single[key]}>'
            self.nextChar()

        return tok

    # Detect string literal
    def checkStringLiteral(self):
        save_string = ""
        self.nextChar()
        while self.curChar != "\"":
            save_string += self.curChar
            self.nextChar()
        tok = f'<literal, {save_string}>'
        self.nextChar()

        return tok

    # Detect character constant
    def checkCharConstant(self):
        save_string = self.curChar
        self.nextChar()
        while self.curChar != "'" and self.curChar != "\n" and self.curChar not in punctuation:
            save_string += self.curChar
            self.nextChar()
        if len(save_string) == 1:
            tok = f'<char_constant, {save_string}>'
        else:
            tok = f'<Invalid char constant!, {save_string}>'
            self.error = f'{save_string} (Invalid char constant!)'
        if self.peek() != "\0":
            self.nextChar()

        return tok

    # Detect punctutation
    def checkPunctuation(self):
        tok = f'<punctuator, {self.curChar}>'
        self.nextChar()
        return tok

    # Detect whitespaces
    def checkWhitespaces(self):
        tok = f'<{whitespaces[self.curChar]}>'
        self.nextChar()
        return tok

    # Return the next token
    def getToken(self):
        token = ""
        if self.curChar == "/":
            token = self.checkComment()
        elif self.curChar in letters:
            token = self.checkKeyDtId()
        elif self.curChar in digits:
            token = self.checkDigit() 
        elif self.curChar in arithmetic_op:
            token = self.checkArithOp()
        elif self.curChar in assignment:
            token = self.checkAssignOp()
        elif self.curChar in relational_ops_single:
            token = self.checkRelOp()
        elif self.curChar == "\"":
            token = self.checkStringLiteral()
        elif self.curChar == "'":
            token = self.checkCharConstant()
        elif self.curChar in punctuation:
            token = self.checkPunctuation()
        elif self.curChar in whitespaces.keys():
            token = self.checkWhitespaces()
        else:
            token = self.error = "<Character not recognised!>"

        # reset error string for next token
        err_cpy = self.error
        self.error = ""

        return token, self.symbol_table, self.symbol_count, err_cpy
