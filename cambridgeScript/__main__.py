from cambridgeScript.interpreter.programs import Program
import argparse



if __name__ == "__main__":
    # p = Program.from_code(open(0).read())
    # print(p)
    # p.execute()

    parser = argparse.ArgumentParser(description='Cambridge Script CLI')
    subparsers = parser.add_subparsers(help='sub-command help')
    run_parser = subparsers.add_parser("run", help="run a program")
    run_parser.add_argument("filename", type=str, help="name of the file")
    run_parser.add_argument("--debug", type=bool, help="print debug info")

    def run(args):
        with open(args.filename) as f:
            p = Program.from_code(f.read())
            if (args.debug): print(p)
            p.execute()

    run_parser.set_defaults(func=run)
    args = parser.parse_args()
    
    args.func(args)
    

