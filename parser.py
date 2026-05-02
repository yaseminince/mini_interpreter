from ast_nodes import Number,Variable,BinaryOp,UnaryOp,Assign,Print,Compound
from TokenType import TokenType
from error import ParserError

#readable name map for user friendly error names
TOKEN_NAMES = {
    TokenType.LPAREN: "left parenthesis '('",
    TokenType.RPAREN: "right parenthesis ')'",
    TokenType.PLUS: "plus '+'",
    TokenType.MINUS: "minus '-'",
    TokenType.MULTIPLY: "multiply '*'",
    TokenType.DIVIDE: "divide '/'",
    TokenType.ASSIGN: "assignment '='",
    TokenType.LESS: "less than '<'",
    TokenType.GREATER: "greater than '>'",
}

# parser : converts tokens to AST (abstract syntax tree)
class Parser:
    def __init__(self,tokens):
        self.tokens=tokens # list of the tokens from lexer
        self.pos=0 # current index in the token list
        self.current_token=tokens[0]

# advance : moves to the next token
    def advance(self): 
        self.pos+=1
        if self.pos<len(self.tokens):
            self.current_token=self.tokens[self.pos]

# expect : ensures the current token matches the expected type if not raises an error
    def expect(self, token_type):
        if self.current_token.type != token_type:
            expected = TOKEN_NAMES.get(token_type, token_type)
            raise ParserError(f"Expected {expected}, but got '{self.current_token.value}'",self.current_token.line,self.current_token.column)
        self.advance()

# factor : smallest unit
    def factor(self):
        token=self.current_token

        # unary operators: +x or -x
        if token.type in (TokenType.PLUS, TokenType.MINUS):
            op = token
            self.advance()
            node = self.factor()
            return UnaryOp(op, node)
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(token.value) 
        
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return Variable(token.value)
        
        # used for expressions like (3+5)
        elif token.type == TokenType.LPAREN:
            self.advance()
            node = self.comparison() # parse inside expression
            self.expect(TokenType.RPAREN) # to expect closing parantheses )
            return node 
        raise ParserError("Unexpected token in factor",token.line,token.column)

# term : handles * and /
    def term(self):
        node=self.factor()
        while self.current_token.type in (TokenType.MULTIPLY,TokenType.DIVIDE):
            op=self.current_token
            self.advance()
            node=BinaryOp(node,op,self.factor())
        return node
    
# expr : handles + and -
    def expr(self):
        node=self.term()
        while self.current_token.type in (TokenType.PLUS,TokenType.MINUS):
            op=self.current_token
            self.advance()
            node=BinaryOp(node,op,self.term())
        return node

# comparison : handles < and >
    def comparison(self):
        node=self.expr()
        # only one comparison is allowed
        if self.current_token.type in (TokenType.LESS,TokenType.GREATER):
            op=self.current_token
            self.advance()
            node=BinaryOp(node,op,self.expr())
        return node

# assignment : assigns the variable to expression
    def assignment(self):
        token=self.current_token
        if token.type != TokenType.IDENTIFIER:
            raise ParserError(
                "Expected variable name",
                token.line,
                token.column
)
        var_name=token.value
        self.advance()
        # expecting "="
        self.expect(TokenType.ASSIGN)
        # parse right hand side
        value=self.comparison()
        return Assign(var_name,value)

# print_statement : prints the expression
    def print_statement(self):
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        value=self.comparison()
        self.expect(TokenType.RPAREN)
        return Print(value)

#statement : one line of a code
    def statement(self):
        if self.current_token.type == TokenType.IDENTIFIER:
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == TokenType.ASSIGN:
                return self.assignment()
        if self.current_token.type == TokenType.PRINT:
            return self.print_statement()
        return self.comparison()

# parse : entire program
    def parse(self):
        statements = []
        # keep parsing until EOF (end of the file)
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        return Compound(statements)
