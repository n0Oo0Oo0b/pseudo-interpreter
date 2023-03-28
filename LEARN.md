# Introduction

Several parts of this project (namely the expression parser) are derived from [Crafting Interpreters](https://craftinginterpreters.com).
It explains most of the concepts used in a straightforward way, and is definitely worth a read if you would like to try something like this yourself.

If you see anything wrong, feel free to [open an issue](https://github.com/n0Oo0Oo0b/pseudo-interpreter/issues/new) describing the problem and I will get it sorted.

**NOTE:** Some code snippets/links included here may not be up to date. While I will change this file when significant changes are made to the repo, smaller changes may not be reflected here.


# How it works

## [Tokenizer](cambridgeScript/parser/tokens.py)

The tokens are parsed using a regular expression (TOKEN_REGEX), as defined in [constants.py](cambridgeScript/constants.py).
Other than that, the tokenizer performs a few rudimentary operations (e.g. resolving escape sequences in string literals) and outputs a list of tokens.
There isn't much interesting things going on here though.


## [Parser](cambridgeScript/interpreter/programs.py#L63)

Pseudocode separates statements through newlines, so each line can be parsed separately.

When entering a block (`WHILE`, `IF`, etc.), a new block is appended to a stack, which keeps track of the nesting state. When the block is complete (`ENDWHILE`, `ENDIF`, etc.), the block is popped from the 
stack and appended to the previous block.

### Parsing expressions

Parsing expressions is done with the [`Parser`](cambridgeScript/parser/parser.py) class, which is pretty much a python
copy of the java code [here](https://craftinginterpreters.com/parsing-expressions.html).


## [Interpreter](cambridgeScript/programs.py#L26)

Again, match-case syntax comes in handy here. Variables are stored in a special [`VariableState`](cambridgeScript/interpreter/variables.py) class, which is a simple wrapper around a dict.
