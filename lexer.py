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

    # Return the next token
    def getToken(self):
        token = []
        # print("Current char", self.curChar)
        if self.curChar == "/":
            if self.peek() == "$":
                self.nextChar()
                self.nextChar()
                while self.curChar != "$":
                    self.nextChar()
                if self.peek() == "/":
                    token.append("<comment>")
                    self.nextChar()
                else:
                    token.append("<comment not closed properly!>")
                    self.nextChar()
            elif self.curChar in arithmetic_op:
                token.append("<" + self.curChar + ">")
                self.nextChar()
        elif self.curChar in letters:
            save_string = ""
            while self.curChar in letters:
                save_string += self.curChar
                self.nextChar()
            if save_string in keywords:
                token.append("<" + save_string + ">")
            elif save_string in data_types:
                token.append("<dt, " + save_string + ">")
            else:
                token.append("<id, " + save_string + ">")
        elif self.curChar in digits:
            save_string = ""
            if self.peek() in letters:
                print("<unsupported!>")
            else:
                while self.curChar in digits:
                    save_string += self.curChar
                    self.nextChar()
                token.append("<num, " + save_string + ">")   
        elif self.curChar in arithmetic_op:
            token.append("<" + self.curChar + ">")
            self.nextChar()
        elif self.curChar in assignment:
            token.append("<assign, " + self.curChar + ">")
            self.nextChar()
        elif self.curChar in relational_ops_single:
            if self.peek() == "=":
                key = self.curChar + "="
                token.append("<rel_op, " + relational_op_double[key] + ">")
                self.nextChar()
            else:
                key = self.curChar
                token.append("<rel_op, " + relational_ops_single[key] + ">")
                self.nextChar()
        elif self.curChar == "\"":
            save_string = ""
            self.nextChar()
            while self.curChar != "\"":
                save_string += self.curChar
                self.nextChar()
            token.append("<literal, " + save_string + ">")
            self.nextChar()
        elif self.curChar in punctuation:
            token.append("<punctuator, " + self.curChar + ">")
            self.nextChar()   
        elif self.curChar in whitespaces.keys():
            token.append("<" + whitespaces[self.curChar] + ">")
            self.nextChar()
        else:
            pass

        # self.nextChar()
        return token
