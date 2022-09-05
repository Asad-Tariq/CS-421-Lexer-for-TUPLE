keywords = ["and", "break", "continue", "else", "false", "for", "if", "mod", "not", "or", "then", "true", "void", "while"]
datatypes = ["bool", "char", "int", "float"]
punctuators = ["{", "}", "(", ")", ";", "[", "]", "\'", "\"", ",", "."]
relational_ops_single = {"<":"LT", ">":"GT"}
realtional_op_double = {"<=":"LE", ">=":"GE", "==":"EQ", "!=":"NE"}
arithmetic_op = ["+", "-", "*", "/", "^"]
whitespaces = {" ":"blank", "\n":"newline", "\t":"tab"}
letters = "abcdefghijklmnopqrstuvwxyz"
digits = "0123456789"

class Lexer:
    def __init__(self, input) -> None:
        self.input = input + '\n'
        self.curChar = ''
        self.curPos = -1
        self.nextChar()

    # Process the next character
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.input):
            self.curChar = '\0' # EOF char
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
            elif self.curChar in arithmetic_op:
                token.append("<" + self.curChar + ">")
        elif self.curChar in letters:
            save_string = ""
            while self.curChar not in whitespaces.keys():
                save_string += self.curChar
                self.nextChar()
            if save_string in keywords:
                token.append("<" + save_string + ">")
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
        elif self.curChar in relational_ops_single:
            if self.peek() == "=":
                key = self.curChar + "="
                token.append("<rel_op, " + realtional_op_double[key] + ">")
                self.nextChar()
            else:
                key = self.curChar
                token.append("<rel_op, " + relational_ops_single[key] + ">")
        elif self.curChar == "\"":
            save_string = ""
            self.nextChar()
            while self.curChar != "\"":
                save_string += self.curChar
                self.nextChar()
            token.append("<literal, " + save_string + ">")
        elif self.curChar in punctuators:
            token.append("<punctuator, " + self.curChar + ">")    
        elif self.curChar in whitespaces.keys():
            token.append("<" + whitespaces[self.curChar] + ">")
        else:
            pass

        self.nextChar()
        return token
