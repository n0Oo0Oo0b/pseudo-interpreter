# Introduction

Many parts of this project are derived from [Crafting Interpreters](https://craftinginterpreters.com). It explains most
of the concepts used very well, and is definitely worth a read if you want to try something like this for yourself.

If you see anything wrong, feel free to [open an issue](https://github.com/n0Oo0Oo0b/pseudo-interpreter/issues/new)
describing the problem and I will get it sorted.

**Last updated at commit eb5e1a0b**


# How it works

## [Lexer](cambridgeScript/parser/lexer.py)

The tokens are parsed using a regular expression because I wasn't bothered to write a full lexer :P. Each token stores
its position in the source code and other information about the token (e.g. name of the identifier for identifier
tokens).

## [Syntax tree](cambridgeScript/syntax_tree)

This contains the classes for the nodes that will represent the program. It uses
the [visitor pattern](https://en.wikipedia.org/wiki/Visitor_pattern), so that functionality can be easily built on top
of it.

## [Parser](cambridgeScript/parser/parser.py)

Parsing statements are pretty straightforward, since each statement type starts with a different keyword, except for
assignment (note that expression statements don't exist since there's no need for them). This makes statement parsing
pretty trivial.

Parsing expressions is done with [recursive descent](https://en.wikipedia.org/wiki/Recursive_descent_parser).

## [Interpreter](cambridgeScript/interpreter/interpreter.py)

Variables are stored in a separate `VariableState` class (so that I can add functionality later if I want to). The
interpreter itself is just a visitor that visits both expressions and statements.
