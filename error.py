# base error class for all custom errors for this project
class Error(Exception):
    def __init__(self, name, details, line, column):
        self.name = name # type of error
        self.details = details # description of error
        self.line = line # line number where error occurred
        self.column = column # column position

    def __str__(self):
        return f"{self.name}: {self.details} at line {self.line}, column {self.column}"

# error for invalid characters
class IllegalCharError(Error):
    def __init__(self, details, line, column):
        super().__init__("Illegal Character", details, line, column)

# error for invalid number formats exp: 3.1.4.5
class InvalidNumberError(Error):
    def __init__(self, details, line, column):
        super().__init__("Invalid Number", details, line, column)

# syntax errors from parser
class ParserError(Error):
    def __init__(self, details, line, column):
        super().__init__("Syntax Error", details, line, column)