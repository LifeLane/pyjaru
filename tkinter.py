import tkinter as tk
from tkinter import filedialog, scrolledtext

class PyJaRuIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("PyJaRu IDE")
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=1)
        
        self.run_button = tk.Button(root, text="Run", command=self.run_code)
        self.run_button.pack()
        
        self.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
        self.output_area.pack(fill=tk.BOTH, expand=1)
        
        self.root.bind('<Control-o>', self.open_file)
        self.root.bind('<Control-s>', self.save_file)

    def run_code(self):
        code = self.text_area.get("1.0", tk.END)
        self.output_area.delete("1.0", tk.END)
        tokens = lexer(code)
        ast = parse(tokens)
        interpreter = Interpreter()
        for node in ast:
            interpreter.visit(node)
            self.output_area.insert(tk.END, f"{node}\n")

    def open_file(self, event=None):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, code)

    def save_file(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".pyjaru")
        if file_path:
            with open(file_path, 'w') as file:
                code = self.text_area.get("1.0", tk.END)
                file.write(code)

root = tk.Tk()
app = PyJaRuIDE(root)
root.mainloop()
