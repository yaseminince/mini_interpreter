class Number:  
    def __init__(self,value):
        self.value=value #int or float
    def __repr__(self):
        return f"Number({self.value})"

class Variable:
    def __init__(self,name):
        self.name=name # string 
    def __repr__(self):
        return f"Variable({self.name})"
class BinaryOp:
    def __init__(self,left,op,right):
        self.left=left #left node
        self.op=op # token (PLUS , MINUS, etc.)
        self.right=right #right node
    def __repr__(self):
        return f"BinaryOp({self.left}, {self.op}, {self.right})"
class UnaryOp:
    def __init__(self, op, node):
        self.op = op
        self.node = node
    def __repr__(self):
        return f"UnaryOp({self.op}, {self.node})"
class Assign:
    def __init__(self,name,value):
        self.name=name
        self.value=value
    def __repr__(self):
        return f"Assign({self.name},{self.value})"
class Print:
    def __init__(self,value):
        self.value=value
    def __repr__(self):
        return f"Print({self.value})"
class Compound:
    def __init__(self,statements):
        self.statements=statements # list
    def __repr__(self):
        return f"Compound({self.statements})"

