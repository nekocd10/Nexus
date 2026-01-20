# Nexus Programming Language

A simple, intuitive programming language designed for clarity and expressiveness. Nexus combines the ease of Python with the structure of statically-typed languages.

## 🚀 Quick Install (One-Liner)

Works on **all devices**: Linux, macOS, Windows, Termux, 32-bit, 64-bit, ARM, and more.

```bash
bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)
```

**What it does automatically:**
- ✅ Detects your OS and architecture
- ✅ Installs everything needed
- ✅ Cleans up markdown files
- ✅ Creates global `nexus` and `nxs` commands
- ✅ Sets up `~/.nxs/` folder

---

## Quick Start

```bash
# Create your first program
echo 'println "Hello, Nexus!"' > hello.nexus

# Run it
nexus hello.nexus
```

---

<details>
<summary><b>📱 Installation Methods & Device Support</b></summary>

### Installation Methods

**Method 1: Curl (Recommended)**
```bash
bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)
```

**Method 2: Wget**
```bash
bash <(wget -qO- https://github.com/nekocd10/Nexus/raw/main/installer.sh)
```

**Method 3: Local Repository**
```bash
git clone https://github.com/nekocd10/Nexus
cd Nexus
bash install.sh
```

**Method 4: Termux (Mobile)**
```bash
pkg install python curl
bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)
```

**Method 5: Docker**
```dockerfile
FROM python:3.11-slim
RUN bash -c "$(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)"
CMD ["nexus"]
```

Or with Alpine (minimal):
```dockerfile
FROM python:3.11-alpine
RUN apk add --no-cache git curl && \
    bash -c "$(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)"
CMD ["nexus"]
```

### Supported Devices & Linux Distros

| Platform | Support | Notes |
|----------|---------|-------|
| **Linux (All Distros)** | ✅ | Ubuntu, Debian, Fedora, Arch, Alpine, openSUSE, etc. |
| **macOS** | ✅ | Intel & Apple Silicon |
| **Windows** | ✅ | 32-bit & 64-bit |
| **Raspberry Pi** | ✅ | All models |
| **Android (Termux)** | ✅ | ARM & x86 |
| **Docker** | ✅ | All base images |
| **32-bit Systems** | ✅ | x86 & ARM |
| **64-bit Systems** | ✅ | x86_64 & ARM64 |

### Verify Installation
```bash
nexus --version
nexus --help
nxs --version
```

</details>

---

<details>
<summary><b>📚 Features & Examples</b></summary>

### Language Features

- **Clear Syntax** - Easy to read and understand
- **Type System** - Optional type annotations with smart inference
- **First-Class Functions** - Functions as values
- **Pattern Matching** - Express complex logic concisely
- **Modules** - Organize code with a module system
- **Interoperability** - Call Python and other languages
- **Full Stack** - Build web apps with built-in Express module

### Code Examples

**Variables and Types**
```nexus
let x = 42
let name = "Nexus"
let numbers = [1, 2, 3, 4, 5]
```

**Functions**
```nexus
def add(a, b) do
  return a + b
end

let result = add(10, 20)
```

**Loops**
```nexus
for i in range(1, 10) do
  println i
end
```

**Full-Stack Web App**
```nexus
use express

app = express.create
app.get "/", |request| do
  return { status: 200, body: "Hello!" }
end

app.listen 3000
```

</details>

---

<details>
<summary><b>🛠️ Installation Details & What Gets Installed</b></summary>

### Installation Process

The installer automatically:
1. Detects OS (Linux, macOS, Windows, Termux)
2. Detects architecture (32-bit, 64-bit, ARM, etc.)
3. Verifies Python 3.8+ installation
4. Downloads from GitHub
5. Installs Python package
6. **Deletes all markdown files** (saves ~20 MB)
7. **Renames folder to `.nxs`**
8. Creates global CLI commands
9. Sets up shell profile
10. Verifies everything works

### Installation Location

| OS | Location |
|----|----------|
| Linux/macOS/Termux | `~/.nxs/` |
| Windows | `%USERPROFILE%\.nxs\` |

### What Gets Installed

```
~/.nxs/
├── src/              # Source code (~10 MB)
├── docs/             # Documentation (~2 MB)
├── examples/         # Examples (~1 MB)
├── nxs_modules/      # Built-in modules (~5 MB)
├── config/           # Configuration files
└── setup.py

Total size: 50-80 MB
All .md files: DELETED ✓
```

### System Requirements

- **Python**: 3.8 or higher
- **Download tool**: curl, wget, or git
- **OS**: Any Linux, macOS, Windows, Termux, BSD, etc.
- **Architecture**: x86, x86_64, ARM, ARM64, or other

</details>

---

<details>
<summary><b>📖 Documentation & Commands</b></summary>

### Project Structure

```
Nexus/
├── src/                # Core interpreter
│   ├── lexer.py
│   ├── parser.py
│   ├── interpreter.py
│   ├── cli.py
│   └── (10 more modules)
├── docs/               # Documentation
├── examples/           # Example programs
├── scripts/            # Installation scripts
├── nxs_modules/        # Built-in modules
└── config/             # Configuration
```

### Commands

```bash
nexus script.nexus      # Run a Nexus program
nxs script.nexus        # Alias (shorter)
nexus --version         # Show version
nexus --help            # Show help
nexus --parse file.nxs  # Show AST
```

### Documentation Files

Inside `~/.nxs/docs/`:
- `DOCUMENTATION.md` - Complete reference
- `SPEC.md` - Language specification
- `FULLSTACK.md` - Web development guide

### Built-in Modules

**Express (Web Framework)**
```nexus
use express
app = express.create
app.get "/", handler
app.listen 3000
```

**Package Manager**
```bash
nexus-pm search package
nexus-pm install package
```

</details>

---

<details>
<summary><b>🔧 Development & Contributing</b></summary>

### Requirements

- Python 3.8+
- Git (for cloning)
- pip (Python package manager)

### Setting Up for Development

```bash
git clone https://github.com/nekocd10/Nexus
cd Nexus
pip install -e .
```

### Running from Source

```bash
cd ~/.nxs
python -m src.cli script.nexus
```

### Running Tests

```bash
python -m pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your work (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

</details>

---

<details>
<summary><b>❓ Troubleshooting & FAQ</b></summary>

### Python not found

**Linux:**
```bash
sudo apt install python3
```

**macOS:**
```bash
brew install python@3.11
```

**Termux:**
```bash
pkg install python
```

**Windows:**
Download from [python.org](https://www.python.org) and check "Add Python to PATH"

### Command not recognized after installation

Restart your terminal or run:
```bash
source ~/.bashrc      # Linux/Termux
source ~/.zshrc       # macOS with zsh
```

### Installation failed

Try the wget fallback:
```bash
bash <(wget -qO- https://github.com/nekocd10/Nexus/raw/main/installer.sh)
```

Or install from local repository:
```bash
git clone https://github.com/nekocd10/Nexus
cd Nexus
bash install.sh
```

### Uninstalling

```bash
# Remove installation
rm -rf ~/.nxs

# Remove from shell profile (optional)
nano ~/.bashrc
# Remove lines mentioning "nxs" or "Nexus"
```

### What happens to documentation?

Documentation is stored in `~/.nxs/docs/` after installation. Root `.md` files are automatically deleted to save space.

</details>

---

<details>
<summary><b>🎯 Roadmap & Support</b></summary>

### Roadmap

- [ ] Compiler backend for better performance
- [ ] Language Server Protocol (LSP) support
- [ ] Expanded standard library
- [ ] Official package registry
- [ ] VS Code extension
- [ ] IDE support for other editors
- [ ] REPL improvements

### Support & Resources

- 🐛 [Report Issues](https://github.com/nekocd10/Nexus/issues)
- 💬 [Discussions](https://github.com/nekocd10/Nexus/discussions)
- 📧 Email: dev@nexus-lang.dev

</details>

---

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

MIT# Dummy commit to force GitHub update
# Another dummy
# Force raw update
