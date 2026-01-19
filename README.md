# Nexus Programming Language

A simple, intuitive programming language designed for clarity and expressiveness. Nexus combines the ease of Python with the structure of statically-typed languages.

## Quick Install

```bash
# One-liner installation from anywhere
bash <(curl -sL https://github.com/nekocd10/maybe-a-custom-language/raw/main/installer.sh)
```

Or locally from the repository:
```bash
bash install.sh
```

## Quick Start

```bash
# Create your first program
echo 'println "Hello, Nexus!"' > hello.nexus

# Run it
nexus hello.nexus
```

## Features

- **Clear Syntax** - Easy to read and understand
- **Type System** - Optional type annotations with smart inference
- **First-Class Functions** - Functions as values
- **Pattern Matching** - Express complex logic concisely
- **Modules** - Organize code with a module system
- **Interoperability** - Call Python and other languages
- **Full Stack** - Build web apps with built-in Express module

## Project Structure

```
maybe-a-custom-language/
├── src/                 # Core interpreter source code
│   ├── lexer.py         # Tokenization
│   ├── parser.py        # AST generation
│   ├── interpreter.py   # Execution engine
│   └── cli.py           # Command-line interface
├── docs/                # Comprehensive documentation
│   ├── DOCUMENTATION.md # Complete guide (all in one)
│   ├── SPEC.md          # Language specification
│   └── FULLSTACK.md     # Web development guide
├── examples/            # Example Nexus programs
├── nxs_modules/         # Built-in modules
├── scripts/             # Installation & build scripts
├── installer.sh         # Curl-installable setup script
├── install.sh           # Local repository setup
└── setup.py             # Python package configuration
```

## Installation Methods

### Method 1: Curl (Recommended for Fresh Installs)
```bash
bash <(curl -sL https://github.com/nekocd10/maybe-a-custom-language/raw/main/installer.sh)
```

### Method 2: Wget
```bash
bash <(wget -qO- https://github.com/nekocd10/maybe-a-custom-language/raw/main/installer.sh)
```

### Method 3: Local Repository
```bash
git clone https://github.com/nekocd10/maybe-a-custom-language
cd maybe-a-custom-language
bash install.sh
```

### Verify Installation
```bash
nexus --version
```

## Examples

### Variables and Types
```nexus
let x = 42
let name = "Nexus"
let numbers = [1, 2, 3, 4, 5]
```

### Functions
```nexus
def add(a, b) do
  return a + b
end

let result = add(10, 20)
```

### Loops
```nexus
for i in range(1, 10) do
  println i
end
```

### Full-Stack Web App
```nexus
use express

app = express.create
app.get "/", |request| do
  return { status: 200, body: "Hello!" }
end

app.listen 3000
```

## Documentation

- **[Complete Guide](docs/DOCUMENTATION.md)** - Full documentation, quick start, and examples
- **[Language Specification](docs/SPEC.md)** - Grammar, syntax rules, and type system
- **[Full-Stack Guide](docs/FULLSTACK.md)** - Web development with Nexus

## Command Reference

```bash
# Basic usage
nexus script.nexus          # Run a Nexus script
nexus                       # Interactive REPL

# CLI Options
nexus --version             # Show version
nexus --help                # Show help message
nexus --parse script.nexus  # Show AST
```

## Development

### Requirements
- Python 3.8+
- Git (for cloning)

### Setting up for Development
```bash
git clone https://github.com/nekocd10/maybe-a-custom-language
cd maybe-a-custom-language
pip install -e .[dev]
```

### Running Tests
```bash
python -m pytest
```

## Modules

### Built-in Modules

#### Express (Web Framework)
```nexus
use express
app = express.create
app.get "/api/data", handler
app.listen 8080
```

#### Package Manager
```bash
nexus-pm search react
nexus-pm install react
```

## Performance

For optimization and compilation strategies, see the [performance guide](docs/INTERPRETER_ALTERNATIVES.md).

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Roadmap

- [ ] Compiler backend for better performance
- [ ] Language Server Protocol support
- [ ] Expanded standard library
- [ ] Package registry
- [ ] VS Code extension

## Support

- 📖 [Documentation](docs/DOCUMENTATION.md)
- 🐛 [Report Issues](https://github.com/nekocd10/maybe-a-custom-language/issues)
- 💬 [Discussions](https://github.com/nekocd10/maybe-a-custom-language/discussions)

## License

See LICENSE file for details.

---

**Made with ❤️ for clean, expressive code**
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