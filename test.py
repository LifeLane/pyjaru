code = '''
print(5 + 3);
x = 10;
print(x);
if (x > 5) {
  print("x is greater than 5");
}
while (x < 15) {
  x = x + 1;
  print(x);
}
def add(a, b) {
  return a + b;
}
print(add(3, 4));
'''
tokens = lexer(code)
ast = parse(tokens)
interpreter = Interpreter()
for node in ast:
    interpreter.visit(node)
