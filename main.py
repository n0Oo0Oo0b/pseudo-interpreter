from cambridgeScript.interpreter.programs import Program


if __name__ == "__main__":
    p = Program.from_code(open(0).read())
    print(p)
    p.execute()
