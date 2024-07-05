class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(ASTNode):
    def __init__(self, value):
        self.value = value

class Print(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class Assign(ASTNode):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

class If(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class While(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Var(ASTNode):
    def __init__(self, name):
        self.name = name

class ArrayLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class ArrayIndex(ASTNode):
    def __init__(self, name, index):
        self.name = name
        self.index = index

class DictLiteral(ASTNode):
    def __init__(self, pairs):
        self.pairs = pairs

class SetLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class TupleLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class ClassDef(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class ClassInstance(ASTNode):
    def __init__(self, class_name, args):
        self.class_name = class_name
        self.args = args

class MethodCall(ASTNode):
    def __init__(self, obj_name, method_name, args):
        self.obj_name = obj_name
        self.method_name = method_name
        self.args = args

def parse(tokens):
    def expect(kind):
        nonlocal pos
        if pos < len(tokens) and tokens[pos][0] == kind:
            pos += 1
        else:
            raise SyntaxError(f'Expected {kind}')

    def expression():
        node = term()
        while pos < len(tokens) and tokens[pos][0] in ('PLUS', 'MINUS', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'):
            token = tokens[pos]
            pos += 1
            node = BinOp(left=node, op=token[0], right=term())
        return node

    def term():
        node = factor()
        while pos < len(tokens) and tokens[pos][0] in ('TIMES', 'DIVIDE'):
            token = tokens[pos]
            pos += 1
            node = BinOp(left=node, op=token[0], right=factor())
        return node

    def factor():
        token = tokens[pos]
        if token[0] == 'NUMBER':
            pos += 1
            return Num(value=int(token[1]))
        elif token[0] == 'IDENT':
            name = token[1]
            pos += 1
            if pos < len(tokens) and tokens[pos][0] == 'LBRACK':
                pos += 1
                index = expression()
                expect('RBRACK')
                return ArrayIndex(name=name, index=index)
            elif pos < len(tokens) and tokens[pos][0] == 'LPAREN':
                pos -= 1
                return function_call()
            elif pos < len(tokens) and tokens[pos][0] == 'DOT':
                pos += 1
                method_name = tokens[pos][1]
                pos += 1
                expect('LPAREN')
                args = []
                if tokens[pos][0] != 'RPAREN':
                    args.append(expression())
                    while tokens[pos][0] == 'COMMA':
                        pos += 1
                        args.append(expression())
                expect('RPAREN')
                return MethodCall(obj_name=name, method_name=method_name, args=args)
            return Var(name=name)
        elif token[0] == 'LPAREN':
            pos += 1
            elements = []
            if tokens[pos][0] != 'RPAREN':
                elements.append(expression())
                while tokens[pos][0] == 'COMMA':
                    pos += 1
                    elements.append(expression())
                if tokens[pos][0] == 'COMMA':
                    pos += 1  # Handle trailing comma
            expect('RPAREN')
            if len(elements) == 1:
                return elements[0]
            return TupleLiteral(elements=elements)
        elif token[0] == 'LBRACK':
            pos += 1
            elements = []
            if tokens[pos][0] != 'RBRACK':
                elements.append(expression())
                while tokens[pos][0] == 'COMMA':
                    pos += 1
                    elements.append(expression())
            expect('RBRACK')
            return ArrayLiteral(elements=elements)
        elif token[0] == 'LBRACE':
            pos += 1
            if tokens[pos][0] == 'RBRACE':
                pos += 1
                return SetLiteral(elements=[])
            pairs = []
            if tokens[pos][0] != 'RBRACE':
                pairs.append(pair())
                while tokens[pos][0] == 'COMMA':
                    pos += 1
                    pairs.append(pair())
            expect('RBRACE')
            if len(pairs) == 1 and isinstance(pairs[0], Var):
                return SetLiteral(elements=[p[0] for p in pairs])
            return DictLiteral(pairs=pairs)
        elif token[0] == 'NEW':
            pos += 1
            class_name = tokens[pos][1]
            pos += 1
            expect('LPAREN')
            args = []
            if tokens[pos][0] != 'RPAREN':
                args.append(expression())
                while tokens[pos][0] == 'COMMA':
                    pos += 1
                    args.append(expression())
            expect('RPAREN')
            return ClassInstance(class_name=class_name, args=args)
        else:
            raise SyntaxError('Unexpected token')

    def pair():
        key = expression()
        expect('COLON')
        value = expression()
        return (key, value)

    def function_call():
        name = tokens[pos][1]
        pos += 1
        expect('LPAREN')
        args = []
        if tokens[pos][0] != 'RPAREN':
            args.append(expression())
            while tokens[pos][0] == 'COMMA':
                pos += 1
                args.append(expression())
        expect('RPAREN')
        return FunctionCall(name=name, args=args)

    def statement():
        if tokens[pos][0] == 'PRINT':
            pos += 1
            expect('LPAREN')
            expr = expression()
            expect('RPAREN')
            expect('SEMI')
            return Print(expression=expr)
        elif tokens[pos][0] == 'IDENT':
            name = tokens[pos][1]
            pos += 1
            expect('ASSIGN')
            expr = expression()
            expect('SEMI')
            return Assign(name=name, expression=expr)
        elif tokens[pos][0] == 'IF':
            pos += 1
            expect('LPAREN')
            condition = expression()
            expect('RPAREN')
            expect('LBRACE')
            body = []
            while tokens[pos][0] != 'RBRACE':
                body.append(statement())
            expect('RBRACE')
            return If(condition=condition, body=body)
        elif tokens[pos][0] == 'WHILE':
            pos += 1
            expect('LPAREN')
            condition = expression()
            expect('RPAREN')
            expect('LBRACE')
            body = []
            while tokens[pos][0] != 'RBRACE':
                body.append(statement())
            expect('RBRACE')
            return While(condition=condition, body=body)
        elif tokens[pos][0] == 'DEF':
            pos += 1
            name = tokens[pos][1]
            pos += 1
            expect('LPAREN')
            params = []
            if tokens[pos][0] != 'RPAREN':
                params.append(tokens[pos][1])
                pos += 1
                while tokens[pos][0] == 'COMMA':
                    pos += 1
                    params.append(tokens[pos][1])
                    pos += 1
            expect('RPAREN')
            expect('LBRACE')
            body = []
            while tokens[pos][0] != 'RBRACE':
                body.append(statement())
            expect('RBRACE')
            return FunctionDef(name=name, params=params, body=body)
        elif tokens[pos][0] == 'CLASS':
            pos += 1
            name = tokens[pos][1]
            pos += 1
            expect('LBRACE')
            body = []
            while tokens[pos][0] != 'RBRACE':
                body.append(statement())
            expect('RBRACE')
            return ClassDef(name=name, body=body)
        else:
            raise SyntaxError('Unexpected statement')

    pos = 0
    ast = []
    while pos < len(tokens):
        ast.append(statement())
    return ast
