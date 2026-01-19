# Nexus Programming Language - Complete Documentation

## Quick Start
See the [Getting Started Guide](#getting-started-guide) below for installation and first steps.

## Table of Contents
1. [Getting Started Guide](#getting-started-guide)
2. [Installation Instructions](#installation-instructions)
3. [Quick Examples](#quick-examples)
4. [Language Specification](#language-specification)
5. [Implementation Guide](#implementation-guide)
6. [Ecosystem & Modules](#ecosystem--modules)
7. [Full Stack Guide](#full-stack-guide)
8. [Advanced Topics](#advanced-topics)

---

## Getting Started Guide

### Installation
The easiest way to install Nexus is using the automatic installer:

```bash
# Download and run the installer
bash <(curl -sL https://github.com/nekocd10/maybe-a-custom-language/raw/main/install.sh)

# Or using wget
bash <(wget -qO- https://github.com/nekocd10/maybe-a-custom-language/raw/main/install.sh)
```

For local installation:
```bash
cd /workspaces/maybe-a-custom-language
bash install.sh
```

### Your First Program
Create a file `hello.nexus`:
```nexus
println "Hello, Nexus!"
```

Run it:
```bash
nexus hello.nexus
```

### Basic Concepts
- **Variables**: Declare with `let` or `var`
- **Pools**: Aggregate values using pool syntax
- **Contexts**: Create scoped environments
- **Functions**: Define reusable code blocks
- **Mutations**: Handle stateful changes

---

## Installation Instructions

### Requirements
- Python 3.8 or higher
- Git (for development installations)
- pip (Python package manager)

### From Source
```bash
git clone https://github.com/nekocd10/maybe-a-custom-language
cd maybe-a-custom-language
pip install -e .
```

### From PyPI (when available)
```bash
pip install nexus-lang
```

### Verify Installation
```bash
nexus --version
nexus --help
```

---

## Quick Examples

### Variables and Types
```nexus
let x = 42
let name = "Nexus"
let values = [1, 2, 3, 4, 5]
```

### Arithmetic Operations
```nexus
let sum = 10 + 20
let product = 5 * 3
let result = (100 - 50) / 2
```

### Control Flow
```nexus
if x > 0 then
  println "Positive"
else
  println "Non-positive"
end
```

### Functions
```nexus
def greet(name) do
  println "Hello, " + name
end

greet "World"
```

### Loops
```nexus
for i in range(1, 10) do
  println i
end
```

---

## Language Specification

See `docs/SPEC.md` for the complete Nexus Language Specification including:
- Syntax rules
- Type system
- Operator precedence
- Reserved keywords
- Grammar definition

---

## Implementation Guide

The Nexus interpreter consists of several components:

### Core Components
- **Lexer** (`src/lexer.py`): Tokenizes source code
- **Parser** (`src/parser.py`): Builds abstract syntax tree
- **Interpreter** (`src/interpreter.py`): Executes the AST
- **CLI** (`src/cli.py`): Command-line interface

### Extension Points
- Custom modules in `nxs_modules/`
- Backend implementations (`src/backend.py`)
- Frontend rendering (`src/frontend.py`)

For detailed implementation info, see `docs/IMPLEMENTATION.md`

---

## Ecosystem & Modules

The Nexus ecosystem includes several built-in modules:

### Express Module
Web framework for Nexus:
```nexus
use express
app = express.create
app.get "/", handler
```

### Package Manager
Install packages with:
```bash
nexus-pm install package-name
```

---

## Full Stack Guide

Nexus can be used for full-stack development:

### Backend
Create HTTP servers with the Express module.

### Frontend
Generate HTML/CSS with frontend utilities.

### Deployment
Bundle and deploy your Nexus applications.

See `docs/FULLSTACK.md` for complete examples.

---

## Advanced Topics

### Performance Optimization
See `docs/INTERPRETER_ALTERNATIVES.md` for compilation and optimization strategies.

### Interoperability
Nexus can interoperate with Python and other languages. See `docs/INTEROP.md`.

### Building & Bundling
Create standalone applications with the build system.

---

## Project Structure

```
maybe-a-custom-language/
├── src/                 # Core interpreter source code
├── docs/                # Documentation files
├── examples/            # Example Nexus programs
├── bin/                 # Binary/executable files
├── scripts/             # Installation and setup scripts
├── nxs_modules/         # Built-in modules
├── tests/               # Test suite
└── setup.py             # Package configuration
```

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

See LICENSE file for details.

## Support

- Report issues on GitHub
- Check existing documentation
- Review example programs in `examples/`
