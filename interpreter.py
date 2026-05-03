from Lexer import Lexer
from parser import Parser
from TokenType import TokenType
from error import InterpreterRuntimeError, StringError


# evaluates the AST and produces a result
class Interpreter:
    def __init__(self):
        self.variables = {} # stores variable names and values
        self.output = [] # stores print outputs

    # calls the correct method 
    def visit(self, node):
        if type(node).__name__ == "Number":
            return self.visit_Number(node)
        elif type(node).__name__ == "String":
            return self.visit_String(node)
        elif type(node).__name__ == "Variable":
            return self.visit_Variable(node)
        elif type(node).__name__ == "BinaryOp":
            return self.visit_BinaryOp(node)
        elif type(node).__name__ == "UnaryOp":
            return self.visit_UnaryOp(node)
        elif type(node).__name__ == "Assign":
            return self.visit_Assign(node)
        elif type(node).__name__ == "Print":
            return self.visit_Print(node)
        elif type(node).__name__ == "Compound":
            return self.visit_Compound(node)
        else:
            raise InterpreterRuntimeError(f"No visit method for {type(node).__name__}",0,0)

    # converts number value to int or float
    def visit_Number(self, node):
        value = node.value

        if isinstance(value, int) or isinstance(value, float):
            return value

        if isinstance(value, str):
            if "." in value:
                return float(value)
            return int(value)

        raise InterpreterRuntimeError(f"Invalid number value: {value}",node.line,node.column)

    # returns the string value directly
    def visit_String(self, node):
        return node.value

    # looks up variable value from memory
    def visit_Variable(self, node):
        var_name = node.name

        if var_name not in self.variables:
            raise InterpreterRuntimeError(f"Variable '{var_name}' is not defined", node.line, node.column)

        return self.variables[var_name]

    # evaluates math, string, and comparison operations
    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        op_type = node.op.type
        op_line = node.op.line
        op_col = node.op.column

        left_is_str = isinstance(left, str)
        right_is_str = isinstance(right, str)

        if op_type == TokenType.PLUS:
            # string + string -> concatenation
            if left_is_str and right_is_str:
                return left + right
            # number + number -> addition
            if not left_is_str and not right_is_str:
                return left + right
            # mixed types are not allowed
            raise StringError(
                f"Cannot use '+' between string and number",
                op_line, op_col
            )

        # operations below are only valid for numbers
        if left_is_str or right_is_str:
            op_symbol = {
                TokenType.MINUS: "-",
                TokenType.MULTIPLY: "*",
                TokenType.DIVIDE: "/",
                TokenType.LESS: "<",
                TokenType.GREATER: ">",
            }.get(op_type, "?")
            raise StringError(
                f"Cannot use '{op_symbol}' with strings",
                op_line, op_col
            )

        if op_type == TokenType.MINUS:
            return left - right

        elif op_type == TokenType.MULTIPLY:
            return left * right

        elif op_type == TokenType.DIVIDE:
            if right == 0:
                raise InterpreterRuntimeError("Division by zero", op_line, op_col)
            return left / right

        elif op_type == TokenType.LESS:
            return left < right

        elif op_type == TokenType.GREATER:
            return left > right

        raise InterpreterRuntimeError(f"Unknown operator: {node.op}", op_line, op_col)

    # applies a plus or minus sign to a value
    def visit_UnaryOp(self, node):
        value = self.visit(node.node)

        if isinstance(value, str):
            raise StringError(
                "Cannot apply unary operator to a string",
                node.op.line, node.op.column
            )

        if node.op.type == TokenType.MINUS:
            return -value

        elif node.op.type == TokenType.PLUS:
            return +value

        raise InterpreterRuntimeError(f"Unknown unary operator: {node.op}", node.op.line, node.op.column)

    # stores the result of an expression in variables
    def visit_Assign(self, node):
        value = self.visit(node.value)
        self.variables[node.name] = value
        return value

    # evaluates the expression and adds result to output
    def visit_Print(self, node):
        value = self.visit(node.value)
        # strings are printed without extra quotes
        self.output.append(str(value))
        return value

    # runs all statements one by one
    def visit_Compound(self, node):
        last_value = None

        for statement in node.statements:
            last_value = self.visit(statement)

        if self.output:
            return "\n".join(self.output) # return print outputs if any
        return last_value # otherwise return last value

    # takes source code, runs it through lexer, parser, and interpreter
    def run(self, fn, text):
        self.output = []

        try:
            lexer = Lexer(text)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            result = self.visit(ast)

            return result, None

        except Exception as error:
            return None, error
