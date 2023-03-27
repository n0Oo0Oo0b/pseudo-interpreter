# doesnt work for some reason so run this instead
# sometimes you get this error
# `ModuleNotFoundError: No module named 'cambridgeScript'`
# so run this if you get that
# i love dirty hacks :kekw:

from cambridgeScript.interpreter.programs import Program

if __name__ == "__main__":
    p = Program.from_code(open(0).read())
    print(p)
    p.execute()
