# Nexus Programming Language

**A Completely Original Language with Unique Syntax and Paradigms**

Nexus is not inspired by Node.js or Python. It's a fundamentally different programming language with its own unique concepts, syntax, and execution model that has never been seen in mainstream programming languages.

## Philosophy

Instead of copying existing paradigms, Nexus introduces:

- **Contexts** instead of functions
- **Pools** instead of arrays/objects  
- **Flow Operators** for explicit data movement
- **Condition Gates** instead of if/else
- **Reactions** instead of loops
- **Mutable State Markers** with `@` prefix
- **Quantum Operators** for handling alternatives

## Core Concepts

### 1. Contexts (Not Functions)
Named execution scopes with explicit inputs and outputs:

```nexus
~context add_numbers
  @in: a, b
  @out: result
  result => a + b
```

### 2. Pools (Not Arrays or Objects)
Unique data structures with two variants:

```nexus
[| 1, 2, 3, 4, 5 |]         // Ordered pool
[: name="Alice", age=30 :]   // Keyed pool
```

### 3. Flow Operators
Explicit data flow with `=>`, `<=`, `@>`, `++>`:

```nexus
value => output              // Forward flow to function
value => variable            // Forward flow to variable
counter ++> counter          // Increment and flow
```

### 4. Mutable State Markers
Clear distinction between immutable and mutable:

```nexus
#var x = 10      // Immutable binding
@var y = 20      // Mutable state
```

### 5. Condition Gates
Alternative to if/else:

```nexus
~gate check_value
  value ? > 100
    => "large"
  | < 100
    => "small"
  | else
    => "medium"
```

## Unique Operators

| Operator | Meaning |
|----------|---------|
| `=>` | Forward data flow |
| `<=` | Backward data flow |
| `@>` | Channel forward |
| `<@` | Channel backward |
| `++>` | Increment and flow |
| `~` | Context/Reaction marker |
| `@` | Mutable state marker |
| `#` | Immutable binding |
| `?` | Condition gate |
| `[` `\|` ... `\|` `]` | Ordered pool |
| `[` `:` ... `:` `]` | Keyed pool |

## Quick Start

### Installation

```bash
cd /workspaces/maybe-a-custom     
chmod +x nexus
```

### Hello World
```nexus
"Hello, Nexus!" => output
```

Run it:
```bash
./nexus examples/01_hello.nexus
```

### Variables
```nexus
#var x = 10
@var counter = 0
x + counter => output
```

### Arithmetic
```nexus
#var a = 15
#var b = 3

a + b => output    // 18
a - b => output    // 12
a * b => output    // 45
a / b => output    // 5.0
```

### Working with Pools
```nexus
#var numbers = [| 1, 2, 3, 4, 5 |]
numbers => output

#var person = [: name="Bob", age=30, city="NYC" :]
person => output
```

## Running Programs

### Execute file
```bash
./nexus nexus_examples/01_hello.nexus
./nexus nexus_examples/03_pools.nexus
./nexus nexus_examples/05_arithmetic.nexus
```

### Interactive REPL
```bash
./nexus --repl
```

### Debug: Show tokens
```bash
./nexus --tokens nexus_examples/01_hello.nexus
```

### Debug: Show AST
```bash
./nexus --ast nexus_examples/01_hello.nexus
```

## Examples

The `nexus_examples/` directory contains:

1. `01_hello.nexus` - Hello world
2. `02_variables.nexus` - Immutable and mutable bindings
3. `03_pools.nexus` - Ordered and keyed pools
4. `04_contexts.nexus` - Context definitions
5. `05_arithmetic.nexus` - Arithmetic operations
6. `06_comparison.nexus` - Comparison operations
7. `07_mutation.nexus` - Mutable state modifications
8. `08_strings.nexus` - String operations

## Language Features

### Variables
```nexus
#var x = 10          // Immutable
@var mutable = 20    // Mutable
```

### Contexts
```nexus
~context process
  @in: input, mode
  @out: result
  result = input * 2
```

### Data Flow
```nexus
value => output                  // Send to output
value => variable                // Store in variable
@counter ++> @counter            // Increment
```

### Collections
```nexus
#var ordered = [| 1, 2, 3 |]
#var keyed = [: x=10, y=20 :]
```

### Operators
```nexus
a + b       // Addition
a - b       // Subtraction
a * b       // Multiplication
a / b       // Division
a % b       // Modulo

a == b      // Equal
a != b      // Not equal
a < b       // Less than
a > b       // Greater than
a <= b      // Less or equal
a >= b      // Greater or equal
```

## Built-in Functions

```nexus
output          // Print to console
input           // Read user input
type_of         // Get type
length          // Get collection length
```

## Architecture

### Components

1. **Lexer** (`nexus_lexer.py`) - Tokenizes Nexus source
2. **Parser** (`nexus_parser.py`) - Builds AST
3. **Interpreter** (`nexus_interpreter.py`) - Executes AST
4. **CLI** (`nexus`) - Command-line interface

### What Makes It Completely Original

✨ **No Functions** - Uses contexts with explicit inputs/outputs  
✨ **No Arrays/Objects** - Uses pools with unique syntax  
✨ **No if/else** - Uses condition gates with `?` operator  
✨ **No Loops** - Uses reactions that trigger on conditions  
✨ **Explicit Flow** - Data movement marked with `=>`, `<=`, `@>`  
✨ **Mutable Markers** - `@` prefix clearly shows state  
✨ **Original Syntax** - Every aspect is completely unique  

## Why This Is Different

| Aspect | Traditional | Nexus |
|--------|-----------|-------|
| **Function** | `function foo()` / `def foo():` | `~context foo @in: @out:` |
| **Array** | `[1,2,3]` | `[` `\|` `1, 2, 3` `\|` `]` |
| **Object** | `{x:1, y:2}` | `[: x=1, y=2 :]` |
| **If Statement** | `if (x > 5) {}` | `~gate condition ? > 5 => action` |
| **Loop** | `for (i=0; i<10; i++)` | `~reaction name ? condition => action` |
| **Return** | `return value` | `value => output` |
| **Variable** | `var x = 10` | `#var x = 10` (immutable) |
| **Mutable** | Context dependent | `@var x = 10` (explicit) |

## Contributing

This is a complete language implementation. Feel free to:
- Add new operators
- Extend contexts
- Improve error messages
- Create more examples
- Build standard library

## License

MIT