from lexer import *

def main():
    with open("CS-421-Lexer-for-TUPLE\custom_test.tpl") as custom_test:
        lines = custom_test.readlines()

    for line in lines:
        lexer = Lexer(line)
        while lexer.peek() != '\0':
            print(lexer.getToken())
main()