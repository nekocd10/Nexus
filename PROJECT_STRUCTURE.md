# Project Structure

```
maybe-a-custom-language/
│
├── README.md                    # Main project README
├── setup.py                     # Python package configuration
├── install.sh                   # Local installation script (for development)
├── installer.sh                 # Curl-installable automatic installer
│
├── src/                         # Core interpreter source code
│   ├── __init__.py              # Package initialization
│   ├── cli.py                   # Command-line interface
│   ├── lexer.py                 # Lexical analysis/tokenization
│   ├── parser.py                # Syntax analysis/AST generation
│   ├── interpreter.py           # AST execution engine
│   ├── backend.py               # Compilation backends
│   ├── frontend.py              # Frontend utilities
│   ├── build.py                 # Build system
│   ├── bundler.py               # Application bundler
│   ├── interop.py               # Language interoperability
│   └── package_manager.py       # Package management
│
├── docs/                        # Comprehensive documentation
│   ├── README.md                # Documentation guide
│   ├── DOCUMENTATION.md         # Complete unified documentation
│   ├── SPEC.md                  # Language specification
│   ├── FULLSTACK.md             # Web development guide
│   ├── IMPLEMENTATION.md        # Implementation details
│   ├── INTERPRETER_ALTERNATIVES.md  # Performance optimization
│   ├── QUICK_EXAMPLES.md        # Quick reference
│   ├── GETTING_STARTED.md       # Getting started
│   ├── ECOSYSTEM.md             # Module ecosystem
│   ├── INDEX.md                 # Documentation index
│   └── IMPLEMENTATION_SUMMARY.md # Implementation summary
│
├── examples/                    # Example Nexus programs
│   ├── 01_hello.nexus           # Hello world
│   ├── 02_variables.nexus       # Variables and types
│   ├── 03_pools.nexus           # Collections
│   ├── 04_contexts.nexus        # Functions/contexts
│   ├── 05_arithmetic.nexus      # Arithmetic operations
│   ├── 06_comparison.nexus      # Comparisons
│   ├── 07_mutation.nexus        # State mutations
│   ├── 08_strings.nexus         # String operations
│   └── examples.py              # Example utilities
│
├── scripts/                     # Utility scripts
│   ├── install.sh               # Installation script (copy)
│   └── installer.sh             # Curl installer (copy)
│
├── config/                      # Configuration files
│   ├── nxs.json                 # Language configuration
│   └── setup.py                 # Setup copy
│
├── nxs_modules/                 # Built-in modules
│   ├── express/                 # Web framework module
│   │   ├── __init__.py
│   │   └── app.py
│   └── README.md
│
├── bin/                         # Binary/executable directory (future use)
│
└── .gitignore                   # Git ignore patterns

## Directory Purpose

### `/src` - Core Implementation
The interpreter implementation with lexer, parser, and runtime.

### `/docs` - Documentation
All documentation consolidated. See `docs/README.md` for navigation.

### `/examples` - Example Programs
Sample Nexus programs demonstrating language features.

### `/nxs_modules` - Built-in Modules
Modules like Express for web development.

### `/scripts` - Build & Installation Scripts
Scripts for installation and building.

### `/config` - Configuration
Project configuration files.

### `/bin` - Binaries (Future)
Compiled executables and command-line tools.
```

## Getting Started

1. **Installation**: See [README.md](README.md#installation-methods)
2. **Quick Start**: See [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md#quick-start)
3. **Examples**: Check [examples/](examples/) directory
4. **Full Guide**: Read [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md)

## Key Files

- **Main Entry Point**: `src/cli.py`
- **Package Configuration**: `setup.py` and `config/nxs.json`
- **Installer**: `installer.sh` (curl-installable)
- **Documentation**: `docs/DOCUMENTATION.md` (consolidated)
