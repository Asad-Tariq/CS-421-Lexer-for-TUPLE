from tuple_spec import *


class Lexer:
    def __init__(self, input_stream, symbol_table, symbol_count) -> None:
        self.input = input_stream + '\n'
        self.curChar = ''
        self.curPos = -1
        self.symbol_table = symbol_table
        self.symbol_count = symbol_count
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
        if self.peek() == "$":
            self.nextChar()
            self.nextChar()
            while self.curChar != "$":
                self.nextChar()
            if self.peek() == "/":
                tok = "<comment>"
                self.nextChar()
                self.nextChar()
            elif self.peek() == "\n":
                tok = "<comment not closed properly!>"
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
            tok = "<Invalid Identifier!>"
        elif self.curChar not in whitespaces.keys() and self.curChar not in punctuation and self.curChar not in arithmetic_op:
            tok = "<Invalid Identifier!>"
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
                self.nextChar()
            return save_string, False
        else:
            save_string += self.curChar
            self.nextChar()
            while self.curChar in digits or self.curChar == "E":
                save_string += self.curChar
                self.nextChar()
            return save_string, True

    # Detect digits
    def checkDigit(self):
        save_string = ""
        tok = ""
        if self.peek() in letters:
            print("<Unsupported!>")
        else:
            while self.curChar in digits:
                save_string += self.curChar
                self.nextChar()
            if self.curChar == ".":
                floatString, isFloat = self.checkFloat()
                if isFloat:
                    tok = "<float, " + save_string + floatString + ">"
                else:
                    tok = "<Invalid Float!>"
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
            tok = "<num, " + save_string + ">" 
        else:
            tok = "<" + self.curChar + ">"
            self.nextChar()
        return tok

    # Detect assignment operator
    def checkAssignOp(self):
        if self.peek() != "=":
            tok = "<assign, " + self.curChar + ">"
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
            tok = "<rel_op, " + relational_op_double[key] + ">"
            self.nextChar()
            self.nextChar()
        else:
            key = self.curChar
            tok = "<rel_op, " + relational_ops_single[key] + ">"
            self.nextChar()

        return tok

    # Detect string literal
    def checkStringLiteral(self):
        save_string = ""
        self.nextChar()
        while self.curChar != "\"":
            save_string += self.curChar
            self.nextChar()
        tok = "<literal, " + save_string + ">"
        self.nextChar()

        return tok

    # Detect character constant
    def checkCharConstant(self):
        save_string = ""
        self.nextChar()
        while self.curChar != "'" and self.curChar != "\n":
            save_string += self.curChar
            self.nextChar()
        if len(save_string) == 1:
            tok = "<char_constant, " + save_string + ">"
        else:
            tok = "<Invalid char constant!>"
        if self.peek() != "\0":
            self.nextChar()

        return tok

    # Detect punctutation
    def checkPunctuation(self):
        tok = "<punctuator, " + self.curChar + ">"
        self.nextChar()
        return tok

    # Detect whitespaces
    def checkWhitespaces(self):
        tok = "<" + whitespaces[self.curChar] + ">"
        self.nextChar()
        return tok

    # Return the next token
    def getToken(self):
        token = []
        # print("Current char", self.curChar)
        if self.curChar == "/":
            token.append(self.checkComment())
        elif self.curChar in letters:
            token.append(self.checkKeyDtId())
        elif self.curChar in digits:
            token.append(self.checkDigit()) 
        elif self.curChar in arithmetic_op:
            token.append(self.checkArithOp())
        elif self.curChar in assignment:
            token.append(self.checkAssignOp())
        elif self.curChar in relational_ops_single:
            token.append(self.checkRelOp())
        elif self.curChar == "\"":
            token.append(self.checkStringLiteral())
        elif self.curChar == "'":
            token.append(self.checkCharConstant())
        elif self.curChar in punctuation:
            token.append(self.checkPunctuation())
        elif self.curChar in whitespaces.keys():
            token.append(self.checkWhitespaces())
        else:
            pass

        return token, self.symbol_table, self.symbol_count
