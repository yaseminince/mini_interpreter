from token_class import Token
import TokenType as tt
from error import IllegalCharError, InvalidNumberError, MissingQuoteError

#lexer: converts source code into tokens
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1

#current char: returns current character
    def current_char(self):
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None

#advance: moves to next character
#updates line and column
    def advance(self):
        if self.current_char() == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1

#tokenize:scans input and creates tokens
    def tokenize(self):
        tokens = []
        while self.current_char() is not None:
            c = self.current_char()

            #Skips whitespace
            if c in (' ', '\t', '\n'):
                self.advance()
                continue

            #Skips comments starting with #
            if c == '#':
                while self.current_char() is not None and self.current_char() != '\n':
                    self.advance()
                continue

            # Numbers : handles integers and decimals
            if c.isdigit():
                num = ''
                dots = 0
                while self.current_char() is not None and (self.current_char().isdigit() or self.current_char() == '.'):
                    if self.current_char() == '.':
                        dots += 1
                        if dots > 1:
                            raise InvalidNumberError("Too many dots in number", self.line, self.column)
                    num += self.current_char()
                    self.advance()
                tokens.append(Token(tt.TokenType.NUMBER, num, self.line, self.column))
                continue

            #Strings: reads text between double quotes
            if c == '"':
                string_val = ''
                self.advance()  #skip opening quote
                while self.current_char() is not None and self.current_char() != '"':
                    if self.current_char() == '\n':
                        raise MissingQuoteError("Unclosed string before newline", self.line, self.column)
                    string_val += self.current_char()
                    self.advance()
                if self.current_char() is None:
                    raise MissingQuoteError("Unclosed string at end of file", self.line, self.column)
                self.advance()  #skip closing quote
                tokens.append(Token(tt.TokenType.STRING, string_val, self.line, self.column))
                continue

            #Identifiers and keywords
            if c.isalpha() or c == '_':
                word = ''
                start_col = self.column
                while self.current_char() is not None and (self.current_char().isalnum() or self.current_char() == '_'):
                    word += self.current_char()
                    self.advance()
                #checks print keyword
                if word == 'print':
                    tokens.append(Token(tt.TokenType.PRINT, word, self.line, start_col))
                else: #otherwise it is a variable
                    tokens.append(Token(tt.TokenType.IDENTIFIER, word, self.line, start_col))
                continue

            # Operators and parentheses
            if c == '+':
                tokens.append(Token(tt.TokenType.PLUS, '+', self.line, self.column))

            elif c == '-':
                tokens.append(Token(tt.TokenType.MINUS, '-', self.line, self.column))

            elif c == '*':
                tokens.append(Token(tt.TokenType.MULTIPLY, '*', self.line, self.column))

            #Power operator : handles exponent symbol ^
            elif c == '^':
                tokens.append(Token(tt.TokenType.POWER, '^', self.line, self.column))

            elif c == '/':
                tokens.append(Token(tt.TokenType.DIVIDE, '/', self.line, self.column))

            elif c == '=':
                tokens.append(Token(tt.TokenType.ASSIGN, '=', self.line, self.column))

            elif c == '<':
                tokens.append(Token(tt.TokenType.LESS, '<', self.line, self.column))

            elif c == '>':
                tokens.append(Token(tt.TokenType.GREATER, '>', self.line, self.column))

            elif c == '(':
                tokens.append(Token(tt.TokenType.LPAREN, '(', self.line, self.column))

            elif c == ')':
                tokens.append(Token(tt.TokenType.RPAREN, ')', self.line, self.column))

            #invalid character check
            else:
                raise IllegalCharError(f"Unexpected '{c}'", self.line, self.column)

            self.advance()

#add EOF token at end of input
        tokens.append(Token(tt.TokenType.EOF, "EOF", self.line, self.column))
        return tokens

#input handling for lexer testing
if __name__ == "__main__":
    code = input("Enter code: ")
    lexer = Lexer(code)

    try:
        tokens = lexer.tokenize()

        for t in tokens:
            print(t)

    except (IllegalCharError, InvalidNumberError, MissingQuoteError) as e:
        print(e)
