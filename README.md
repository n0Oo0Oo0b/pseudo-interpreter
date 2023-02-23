# pseudo-interpreter (WIP)

A program to execute pseudocode programs (syntax as taught in CiE IGCSE Computer Science).

Made in vanilla python without any 3rd party modules.

## Why 'cambridgeScript'?

Pseudocode is supposed to be a flexible way of outlining code, and shouldn't follow specific conventions. However, the 'pseudocode' required by IGCSE Computer Science requires strict syntax. This makes it easer to write parsers and interpreters for executing IGCSE pseudocode (which is one of the main reasons I made this), but it also means pseudocode loses its value as a way of outlining code. Since the strict syntax almost makes pseudocode almost feel like another language entirely, I decided to name it 'cambridgeScript'.

## Features

- Variables (currently only supports numeric types, have to be declared with `DECLARE variable`)
- Basic expressions, including parenthesis and order of operations
- Selection - if/else conditionals
- Iteration - for, while, repeat until loops
- Basic I/O to stdin/stdout

### Planned features

- Variable types (`INTEGER`, `REAL`, `CHAR`, `STRING`, `BOOLEAN`)
- Case statements
- A command-line interface

## How to run

Execute the `cambridgeScript` directory with python3.10 or above. The script to execute will be read from stdin.
