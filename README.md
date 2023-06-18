# pseudo-interpreter (WIP)

A program to execute pseudocode programs (syntax as taught in CiE IGCSE Computer Science).

All working parts of the interpreter were made with vanilla python (no 3rd party libs)

## Why 'cambridgeScript'?

Pseudocode is supposed to be a flexible way of outlining code, and shouldn't follow specific conventions. However, the 'pseudocode' required by IGCSE Computer Science requires strict syntax. This makes it easer to write parsers and interpreters for executing IGCSE pseudocode (which is one of the main reasons I made this), but it also means pseudocode loses its value as a way of outlining code. Since the strict syntax almost makes pseudocode almost feel like another language entirely, I decided to name it 'cambridgeScript'.

### Planned features

- `CHAR` datatype
- Actually implementing the whole interpreter
- A command-line interface
    - Options for implementation details (such as variable scope)
- Library functions (such as DIV and MOD)

## How to run

Run with `python3 -m cambridgeScript < file.txt`

Python 3.11+ is required (tested on 3.11.2).
