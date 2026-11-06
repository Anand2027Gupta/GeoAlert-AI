import py_compile
try:
    py_compile.compile('model.py', doraise=True)
    print("Syntax OK - model.py compiles successfully")
except py_compile.PyCompileError as e:
    print(f"Syntax Error: {e}")