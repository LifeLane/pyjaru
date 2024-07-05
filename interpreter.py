class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.classes = {}

    def visit(self, node):
        try:
            if isinstance(node, BinOp):
                left = self.visit(node.left)
                right = self.visit(node.right)
                if node.op == 'PLUS':
                    return left + right
                elif node.op == 'MINUS':
                    return left - right
                elif node.op == 'TIMES':
                    return left * right
                elif node.op == 'DIVIDE':
                    return left / right
                elif node.op == 'EQ':
                    return left == right
                elif node.op == 'NE':
                    return left != right
                elif node.op == 'LT':
                    return left < right
                elif node.op == 'GT':
                    return left > right
                elif node.op == 'LE':
                    return left <= right
                elif node.op == 'GE':
                    return left >= right
            elif isinstance(node, Num):
                return node.value
            elif isinstance(node, Var):
                if node.name in self.variables:
                    return self.variables[node.name]
                else:
                    raise NameError(f"Variable '{node.name}' not defined")
            elif isinstance(node, Assign):
                self.variables[node.name] = self.visit(node.expression)
            elif isinstance(node, Print):
                print(self.visit(node.expression))
            elif isinstance(node, If):
                if self.visit(node.condition):
                    for stmt in node.body:
                        self.visit(stmt)
            elif isinstance(node, While):
                while self.visit(node.condition):
                    for stmt in node.body:
                        self.visit(stmt)
            elif isinstance(node, FunctionDef):
                self.functions[node.name] = (node.params, node.body)
            elif isinstance(node, FunctionCall):
                if node.name in self.functions:
                    params, body = self.functions[node.name]
                    local_vars = self.variables.copy()
                    for param, arg in zip(params, node.args):
                        self.variables[param] = self.visit(arg)
                    for stmt in body:
                        self.visit(stmt)
                    result = self.variables.get('return', None)
                    self.variables = local_vars
                    return result
                else:
                    raise NameError(f"Function '{node.name}' not defined")
            elif isinstance(node, ArrayLiteral):
                return [self.visit(element) for element in node.elements]
            elif isinstance(node, ArrayIndex):
                array = self.variables.get(node.name, [])
                index = self.visit(node.index)
                if isinstance(array, list) and 0 <= index < len(array):
                    return array[index]
                else:
                    raise IndexError(f"Index '{index}' out of range for array '{node.name}'")
            elif isinstance(node, DictLiteral):
                return {self.visit(key): self.visit(value) for key, value in node.pairs}
            elif isinstance(node, SetLiteral):
                return {self.visit(element) for element in node.elements}
            elif isinstance(node, TupleLiteral):
                return tuple(self.visit(element) for element in node.elements)
            elif isinstance(node, ClassDef):
                self.classes[node.name] = node.body
            elif isinstance(node, ClassInstance):
                if node.class_name in self.classes:
                    local_vars = self.variables.copy()
                    instance_vars = {}
                    for param, arg in zip(node.args, node.args):
                        instance_vars[param.name] = self.visit(arg)
                    self.variables.update(instance_vars)
                    for stmt in self.classes[node.class_name]:
                        self.visit(stmt)
                    self.variables = local_vars
                    return instance_vars
                else:
                    raise NameError(f"Class '{node.class_name}' not defined")
            elif isinstance(node, MethodCall):
                if node.obj_name in self.variables and node.method_name in self.variables[node.obj_name]:
                    method = self.variables[node.obj_name][node.method_name]
                    params, body = method
                    local_vars = self.variables.copy()
                    for param, arg in zip(params, node.args):
                        self.variables[param] = self.visit(arg)
                    for stmt in body:
                        self.visit(stmt)
                    result = self.variables.get('return', None)
                    self.variables = local_vars
                    return result
                else:
                    raise NameError(f"Method '{node.method_name}' not defined in object '{node.obj_name}'")
        except NameError as e:
            print(f"NameError: {e}")
        except IndexError as e:
            print(f"IndexError: {e}")
        except SyntaxError as e:
            print(f"SyntaxError: {e}")
        except Exception as e:
            print(f"Error: {e}")
