# CalcLang

CalcLang is a small interpreted language implemented in Python. It includes a REPL, arithmetic expressions, variables, conditionals, loops, user-defined functions, return values, printing, and a few built-in math helpers.

## What It Supports

- Numeric expressions with `+`, `-`, `*`, `/`
- Comparisons with `==`, `!=`, `<`, `<=`, `>`, `>=`
- Variables and assignment with `=`
- `if` / `then` / `else` / `end` blocks
- `while` / `do` / `end` loops
- Function definitions with `def` and `return`
- Function calls with comma-separated arguments
- `print` statements
- Built-in functions: `sqrt`, `pow`, and `abs`

CalcLang uses floating-point numbers internally, so numeric literals and results are handled as floats.

## Project Structure

```text
README.md
CalcLang/
  CalcLang.py      # REPL entry point
  lexer.py         # Converts source text into tokens
  parser.py        # Builds the AST from tokens
  ast_nodes.py     # AST node definitions
  interpreter.py   # Executes the AST
```

## Running The Interpreter

From the repository root:

```bash
cd CalcLang
python CalcLang.py
```

You will be dropped into an interactive prompt:

```text
Welcome to CalcLang! Type your code below. Type 'exit' to quit.
CalcLang>
```

Type `exit` to leave the REPL.

## Example Program

```text
def factorial(n)
    if n <= 1 then
        return 1
    else
        return n * factorial(n - 1)
    end
end

print factorial(5)
print sqrt(25)
```

## Language Notes

- Blocks must end with `end`.
- `if` statements may include an optional `else` branch.
- The interpreter treats any nonzero value as true and `0.0` as false.
- Comparison results are returned as `1.0` or `0.0`.
- Multi-line input is supported in the REPL for incomplete blocks.

## Error Handling

The REPL prints runtime or syntax errors directly in the terminal. Function calls also keep a simple call-stack trace that is shown when an error occurs inside a nested call.
