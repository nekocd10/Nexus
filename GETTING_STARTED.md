# Getting Started with Nexus

## Installation

The Nexus interpreter is ready to use! No installation needed - just Python 3.

```bash
cd path/to/nexus-lang
bash install.sh
```

## Your First Nexus Program

### 1. Hello World
```bash
nexus run nexus_examples/01_hello.nexus
```

Output:
```
Hello, Nexus World!
```

### 2. Variables & Arithmetic
```bash
nexus run nexus_examples/02_variables.nexus
```

Output:
```
30
```

### 3. Collections (Pools)
```bash
nexus run nexus_examples/03_pools.nexus
```

Output:
```
[1, 2, 3, 4, 5]
{'name': 'Alice', 'age': 30, 'city': 'NYC'}
```

## Interactive REPL

Try Nexus interactively:

```bash
nexus repl
```

Then type:
```
nexus> 10 + 5 => output
15
nexus> "Hello, Nexus!" => output
Hello, Nexus!
nexus> [| 1, 2, 3 |] => output
[1, 2, 3]
```

## Language Basics

### Variables
```nexus
#var x = 10        // Immutable
@var y = 20        // Mutable
```

### Collections
```nexus
[| 1, 2, 3 |]           // Ordered pool
[: name="Bob", age=30 :] // Keyed pool
```

### Operations
```nexus
a + b => output    // Addition → output
a - b => output    // Subtraction → output
a * b => output    // Multiplication → output
a / b => output    // Division → output
```

### Comparisons
```nexus
a > b => output     // Greater than
a == b => output    // Equal
a != b => output    // Not equal
```

### Strings
```nexus
"Hello" + " " + "Nexus!" => output
```

## All Example Programs

1. **01_hello.nexus** - Hello world
2. **02_variables.nexus** - Variables and arithmetic
3. **03_pools.nexus** - Collections
4. **04_contexts.nexus** - Context definitions
5. **05_arithmetic.nexus** - Math operations
6. **06_comparison.nexus** - Comparisons
7. **07_mutation.nexus** - State changes
8. **08_strings.nexus** - String operations

Run any with:
```bash
python3 nexus nexus_examples/[number]_[name].nexus
```

## Debugging Tools

### View Tokens
```bash
python3 nexus --tokens nexus_examples/01_hello.nexus
```

### View AST
```bash
python3 nexus --ast nexus_examples/01_hello.nexus
```

## Creating Your Own Program

Create a file `my_program.nexus`:

```nexus
// My first Nexus program
#var x = 100
#var y = 50

x + y => output
x - y => output
x * y => output
x / y => output

"Program complete!" => output
```

Run it:
```bash
python3 nexus my_program.nexus
```

## Key Language Operators

| Operator | Use | Example |
|----------|-----|---------|
| `=>` | Send data forward | `value => output` |
| `@` | Mutable state | `@var x = 10` |
| `#` | Immutable value | `#var x = 10` |
| `~` | Define context | `~context name` |
| `[` `\|` ... `\|` `]` | Ordered pool | `[` `\|` `1, 2, 3` `\|` `]` |
| `[: ... :]` | Keyed pool | `[: x=1 :]` |
| `?` | Condition | `x ? > 10 => ...` |

## Next Steps

1. ✅ Run the examples
2. ✅ Try the REPL
3. ✅ Create your own programs
4. ✅ Read NEXUS_SPEC.md for full language details
5. ✅ Explore the source code

## Documentation

- **README.md** - Language overview
- **NEXUS_SPEC.md** - Complete specification
- **SHOWCASE.md** - Feature showcase
- **IMPLEMENTATION_SUMMARY.md** - Technical details

## Questions?

Check the source files:
- `nexus_lexer.py` - How tokenization works
- `nexus_parser.py` - How parsing works
- `nexus_interpreter.py` - How execution works

Enjoy coding in Nexus! 🚀
