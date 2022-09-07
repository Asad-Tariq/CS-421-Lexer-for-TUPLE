from tuple_spec import *


class Lexer:
    def __init__(self, input_stream) -> None:
        self.input = input_stream + '\n'
        self.curChar = ''
        self.curPos = -1
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
        while self.curChar in letters:
            save_string += self.curChar
            self.nextChar()
        if save_string in keywords:
            tok = "<keyword, " + save_string + ">"
        elif save_string in data_types:
            tok = "<dt, " + save_string + ">"
        else:
            tok = "<id, " + save_string + ">"

        return tok

    # Detect digits
    def checkDigit(self):
        save_string = ""
        tok = ""
        if self.peek() in letters:
            print("<unsupported!>")
        else:
            while self.curChar in digits:
                save_string += self.curChar
                self.nextChar()
            tok = "<num, " + save_string + ">"

        return tok

    # Detect arithmetic operator
    def checkArithOp(self):
        tok = "<" + self.curChar + ">"
        self.nextChar()
        return tok

    # Detect assignment operator
    def checkAssignOp(self):
        tok = "<assign, " + self.curChar + ">"
        self.nextChar()
        return tok

    # Detect relational operator
    def checkRelOp(self):
        if self.peek() == "=":
            key = self.curChar + "="
            tok = "<rel_op, " + relational_op_double[key] + ">"
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
        elif self.curChar in punctuation:
            token.append(self.checkPunctuation())
        elif self.curChar in whitespaces.keys():
            token.append(self.checkWhitespaces())
        else:
            pass

        return token
