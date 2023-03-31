from .parser.parser import Parser
from .parser.tokens import parse_tokens

if __name__ == "__main__":
    tokens = parse_tokens(open(0).read())
    for token in tokens:
        print(token)
    parser = Parser(tokens)
    print(parser.block())
