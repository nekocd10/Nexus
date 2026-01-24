# Nexus Programming Language

A simple, intuitive programming language designed for clarity and expressiveness. Nexus combines the ease of Python with the structure of statically-typed languages.

## 🚀 Quick Install (One-Liner)

Works on **all devices**: Linux, macOS, Windows, Termux, 32-bit, 64-bit, ARM, and more.

```bash
bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)
```

### Platform-specific one-liners

If you prefer an explicit one-liner for your platform, use one of the following.

```bash
# macOS (Intel / Apple Silicon)
/bin/bash -c "$(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)"

# Termux (Android)
pkg install python curl -y
bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)

# Windows (recommended: WSL or Git Bash)
# Using WSL (runs the installer inside WSL):
wsl bash -c "bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)"

# Alternatively on Windows (PowerShell + Git Bash):
Invoke-WebRequest -Uri https://github.com/nekocd10/Nexus/raw/main/installer.sh -OutFile installer.sh; bash installer.sh
```

<!-- Native PowerShell installer -->
```powershell
# Native Windows (PowerShell) - runs a native PowerShell installer
powershell -NoProfile -ExecutionPolicy Bypass -Command "& { iwr https://raw.githubusercontent.com/nekocd10/Nexus/main/installer.ps1 -OutFile $env:TEMP\nexus_installer.ps1; & $env:TEMP\nexus_installer.ps1 }"
```

**What it does automatically:**
- ✅ Detects your OS and architecture
- ✅ Installs everything needed
- ✅ Cleans up markdown files
- ✅ Creates global `nexus` and `nxs` commands
- ✅ Sets up `~/.nxs/` folder

---

**Installation Commands (Detailed)**

If you prefer explicit package-manager commands instead of the one-liners above, use the commands for your platform below.

- Linux (Debian/Ubuntu):
```bash
sudo apt update
sudo apt install -y python3 python3-pip curl git
bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)
```

- Linux (Fedora/RHEL):
```bash
sudo dnf install -y python3 python3-pip curl git
bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)
```

- Linux (Arch):
```bash
sudo pacman -Syu --noconfirm python python-pip git curl
bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)
```

- Alpine:
```bash
sudo apk add --no-cache python3 py3-pip curl unzip
bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)
```

- macOS (Homebrew):
```bash
brew install python git curl
/bin/bash -c "$(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)"
```

- Windows (PowerShell, native):
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "& { iwr https://raw.githubusercontent.com/nekocd10/Nexus/main/installer.ps1 -OutFile $env:TEMP\nexus_installer.ps1; & $env:TEMP\nexus_installer.ps1 }"
```

- Windows (WSL):
```bash
wsl bash -c "bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)"
```

- Termux (Android):
```bash
pkg update && pkg install -y python curl git
bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)
```

Notes:
- If `nexus` is not immediately available after install, add your Python user Scripts directory to PATH. For example:
```bash
# Linux / macOS (zsh/bash)
export PATH="$HOME/.local/bin:$PATH"

# Windows (PowerShell)
setx PATH "$env:PATH;$(python -m site --user-base)\Scripts"
```

**Documentation Index (summaries)**

The `docs/` folder contains full guides. Below are short summaries and links — open the linked files for full content.

- Backend System: Overview of `.nxsjs` backend decorators, routes, models and examples. See [docs/BACKEND_SYSTEM.md](docs/BACKEND_SYSTEM.md).
- Getting Started: Quick install and first programs (Hello World, REPL, examples). See [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).
- Quick Examples: Full example projects (Todo app, full-stack examples). See [docs/QUICK_EXAMPLES.md](docs/QUICK_EXAMPLES.md).
- Specification: Language philosophy and core syntax (contexts, pools, flow arrows). See [docs/SPEC.md](docs/SPEC.md).
- Full-Stack Guide: Building and deploying full-stack Nexus apps. See [docs/FULLSTACK.md](docs/FULLSTACK.md).
- Ecosystem: Overview of package manager, modules, build system and interoperability. See [docs/ECOSYSTEM.md](docs/ECOSYSTEM.md).
- Implementation: Deep architecture and component descriptions for the interpreter and tooling. See [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md).
- Implementation Summary: Short technical summary and file inventory. See [docs/IMPLEMENTATION_SUMMARY.md](docs/IMPLEMENTATION_SUMMARY.md).
- Interpreter Alternatives: Notes on potential alternative runtime implementations (Go, Rust, etc.). See [docs/INTERPRETER_ALTERNATIVES.md](docs/INTERPRETER_ALTERNATIVES.md).
- Index: Master index linking all documentation. See [docs/INDEX.md](docs/INDEX.md).
- Complete Documentation: Aggregated table of contents and full doc index. See [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md).

If you'd like, I can inline any of the above files directly into `README.md` (making it a single-file reference), or remove selected files from `docs/` if you prefer a slimmed-down repository. Tell me which files you'd like inlined or removed.

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
<summary><b>📚 Complete Documentation Index</b></summary>

All documentation is organized below in collapsible sections. Choose what you need:

- **Getting Started** - New to Nexus? Start here
- **Language Specification** - Complete language syntax and features
- **Backend System** - Building APIs and servers with .nxsjs
- **Full Stack Guide** - Building complete web applications
- **Quick Examples** - Real-world code examples
- **Implementation Details** - How Nexus works internally
- **Ecosystem** - Tools, modules, and packages
- **Interpreter Alternatives** - Different ways to run Nexus code

</details>

---

<details>
<summary><b>🚀 Getting Started with Nexus</b></summary>

### Introduction

Nexus is a complete programming language designed for:
- **Clarity** - Easy to read and understand
- **Expressiveness** - Powerful syntax for complex ideas  
- **Full-Stack Development** - Frontend UI and backend APIs in one language

### Your First Program

```bash
# Install Nexus
bash <(curl -sL https://github.com/nekocd10/Nexus/raw/main/installer.sh)

# Create your first file
echo 'println "Hello, Nexus!"' > hello.nexus

# Run it
nexus hello.nexus
```

### Basic Syntax

**Variables:**
```nexus
let x = 42
let name = "Nexus"
let numbers = [1, 2, 3, 4, 5]
```

**Functions:**
```nexus
def add(a, b) do
  return a + b
end

result = add(10, 20)
println result
```

**Loops:**
```nexus
for i in range(1, 10) do
  println i
end
```

**Conditionals:**
```nexus
if x > 5 do
  println "X is greater than 5"
else
  println "X is 5 or less"
end
```

### Two File Types

Nexus has two distinct file types for full-stack development:

**Frontend (.nxs):**
```nexus
<view class="app">
  <h1>My App</h1>
  <btn @click="handleClick()">Click me</btn>
</view>
```

**Backend (.nxsjs):**
```nexus
@config { port: 5000 }

@route GET "/api/data" {
  return database.query("SELECT * FROM data")
}
```

### Next Steps

- Read the **Language Specification** for complete syntax
- Check **Quick Examples** for real-world code
- Learn **Full Stack Guide** for web development
- Review **Backend System** for API development

</details>

---

<details>
<summary><b>📖 Language Specification</b></summary>

## Core Concepts

### Contexts
Contexts are isolated execution environments with inputs and outputs:

```nexus
~context AddNumbers
  @in: a, b
  @out: result
  result => a + b
```

### Reactions  
Reactions respond to conditions:

```nexus
~reaction OnUserLogin
  condition ? user_logged_in => send_welcome_email
  condition ? user_logged_in => load_dashboard
```

### Gates
Gates provide conditional branching:

```nexus
~gate x
  ? > 5 => big_number
  ? <= 5 => small_number
  else => zero
```

### Pools (Arrays)
```nexus
let numbers = [1, 2, 3, 4, 5]
let first = numbers[0]
let length = numbers.length
```

### Keyed Pools (Objects)
```nexus
let user = [: name="Alice", age=30, email="alice@nexus.dev" :]
let name = user.name
```

### Variables

**Immutable (default):**
```nexus
#var x = 10
x = 20  // Error: cannot modify
```

**Mutable:**
```nexus
@var x = 10
x = 20  // OK
```

### Flows
Data flows between values and contexts:

```nexus
x => output              // Forward flow
y <= output              // Backward flow  
a <> b                   // Bidirectional
context @> value         // To context
value <@ context         // From context
x ++> y                  // Increment and flow
```

### Operators

**Arithmetic:** `+`, `-`, `*`, `/`, `%`, `**`

**Comparison:** `==`, `!=`, `>`, `<`, `>=`, `<=`

**Logical:** `&` (and), `|` (or), `!` (not)

**Type Checking:** `is`, `as`

### Type System

Nexus has optional typing with inference:

```nexus
let x: number = 42
let name: string = "Nexus"
let items: pool = [1, 2, 3]
let config: keyed_pool = [: key="value" :]
```

### Functions

```nexus
def greet(name, greeting) do
  return greeting + ", " + name + "!"
end

def add(a, b) do
  return a + b
end

result = greet("Alice", "Hello")
```

### Pattern Matching

```nexus
match value
  case 1 => "one"
  case 2 => "two"
  case _ => "other"
```

### Error Handling

```nexus
try
  risky_operation()
catch error
  println error.message
```

### Comments

```nexus
# Single line comment
# This is a comment

~ Multi-line comment
~ This is a multi-line
~ comment
```

</details>

---

<details>
<summary><b>🔧 Backend System (.nxsjs)</b></summary>

## Overview

`.nxsjs` files define the complete backend using decorators. This is **pure Nexus syntax**, not JavaScript.

## Core Decorators

**Application Configuration:**
```nexus
@config {
    port: 5000,
    database: "nexus.db",
    redis: "redis://localhost:6379"
}
```

**Data Models:**
```nexus
@model User {
    id: number,
    name: string,
    email: string,
    created_at: date
}
```

**HTTP Routes:**
```nexus
@route GET "/api/users" {
    return database.query("SELECT * FROM users")
}

@route POST "/api/users" @validate @auth {
    user = request.body
    return database.insert("users", user)
}
```

**Middleware:**
```nexus
@middleware auth {
    token = request.headers["authorization"]
    request.user = verify_token(token)
}
```

**Services:**
```nexus
@service UserService {
    def create_user(name, email) {
        user = { name: name, email: email }
        return database.insert("users", user)
    }
}
```

**Background Tasks:**
```nexus
@task ProcessEmails {
    cron: "0 * * * *",
    queue: "emails",
    retry: 3
    
    emails = database.query("SELECT * FROM emails WHERE sent = false")
    for email in emails {
        send_email(email.to, email.subject, email.body)
    }
}
```

**Security:**
```nexus
@auth {
    strategy: "jwt",
    secret: env.JWT_SECRET
}

@permission "admin" {
    check: fn(user) => user.is_admin
}

@rateLimit(100, 60000) { }  # 100 requests per minute
```

**Performance:**
```nexus
@cache {
    ttl: 3600,
    backend: "redis"
}

@cluster {
    nodes: ["node1", "node2", "node3"],
    strategy: "round_robin"
}
```

## 74 Supported Decorators

**Application & Environment:**
@config, @env, @profile, @feature, @flag

**Lifecycle:**
@startup, @shutdown, @task, @cron, @worker, @queue

**Data:**
@model, @repository, @transaction, @cache, @index, @migration, @seed

**Security:**
@auth, @permission, @role, @policy, @rateLimit, @cors, @csrf

**Validation:**
@validate, @schema, @contract, @sanitize

**Observability:**
@log, @trace, @metric, @health, @audit

**Performance:**
@optimize, @parallel, @cluster, @shard, @loadBalance

**Resilience:**
@error, @retry, @fallback, @timeout, @circuitBreaker

**Architecture:**
@module, @service, @plugin, @extension, @boundary

**Realtime:**
@socket, @stream, @event, @pubsub, @channel

**Files:**
@upload, @file, @media, @cdn

**Testing:**
@test, @mock, @benchmark, @assert

**Deployment:**
@deploy, @region, @resource, @limit

**HTTP:**
@route (with GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)

## Complete Example

```nexus
@config {
    port: 5000,
    database: "postgres://localhost/app"
}

@model User {
    id: number,
    name: string,
    email: string
}

@service UserService {
    def create_user(name, email) {
        return database.insert("users", { name: name, email: email })
    }
}

@route POST "/api/users" @validate @auth {
    user = UserService.create_user(request.body.name, request.body.email)
    return { status: 201, data: user }
}

@route GET "/api/users/:id" @cache(3600) {
    user = database.query("SELECT * FROM users WHERE id = ?", :id)
    return user ? { status: 200, data: user } : { status: 404 }
}

@task SendDailyEmails {
    cron: "0 9 * * *",
    queue: "emails"
    
    users = database.query("SELECT * FROM users WHERE email_notifications = true")
    for user in users {
        send_email(user.email, "Daily Summary", generate_summary())
    }
}

@health {
    db_ok = database.ping()
    return { status: db_ok ? "healthy" : "unhealthy" }
}
```

See **Backend System** doc for complete reference.

</details>

---

<details>
<summary><b>🌐 Full Stack Development Guide</b></summary>

## Building Complete Web Applications

### Project Structure

```
my-app/
├── src/
│   ├── index.nxs           # Main frontend
│   ├── components/         # Reusable UI components
│   │   ├── header.nxs
│   │   ├── footer.nxs
│   │   └── card.nxs
│   ├── api.nxsjs           # Main backend entry
│   ├── api/                # Backend services
│   │   ├── users.nxsjs
│   │   ├── posts.nxsjs
│   │   └── auth.nxsjs
│   └── models/
│       └── schema.nxsjs    # Data models
├── dist/                   # Built output
├── nxs.json               # Project config
└── package.json           # Dependencies
```

### Frontend (.nxs) - UI Layer

```nexus
<view class="app">
  <header>
    <h1>My App</h1>
    <nav>
      <btn @click="goHome()">Home</btn>
      <btn @click="goAbout()">About</btn>
    </nav>
  </header>
  
  <main>
    <card>
      <h2>Welcome</h2>
      <input @bind="username" placeholder="Enter name" />
      <btn @click="submit()">Submit</btn>
    </card>
  </main>
  
  <footer>
    <p>© 2024 My App</p>
  </footer>
</view>
```

### Backend (.nxsjs) - API Layer

```nexus
@config {
    port: 5000,
    database: "postgres://localhost/myapp"
}

@route POST "/api/submit" @validate {
    data = request.body
    saved = database.insert("submissions", data)
    return { status: 201, data: saved }
}

@route GET "/api/data" @cache(3600) {
    return database.query("SELECT * FROM data")
}
```

### Full-Stack Workflow

1. **Create project:**
   ```bash
   nexus new my-app
   cd my-app
   ```

2. **Build frontend + backend:**
   ```bash
   nexus build
   ```

3. **Run development server:**
   ```bash
   nexus dev
   ```

4. **Deploy:**
   ```bash
   nexus deploy
   ```

### Communication

**Frontend to Backend:**
```nexus
# In .nxs file:
fetch("/api/data")
  .then(response => response.json())
  .then(data => updateUI(data))
```

**Backend to Database:**
```nexus
# In .nxsjs file:
@route GET "/api/users/:id" {
    user = database.query("SELECT * FROM users WHERE id = ?", :id)
    return user
}
```

### State Management

**Frontend State:**
```nexus
@state {
    username: "Alice",
    email: "alice@nexus.dev",
    isLoading: false
}
```

**Backend State:**
```nexus
@cache {
    key: "user_data_:id",
    ttl: 3600
}
```

</details>

---

<details>
<summary><b>💡 Quick Examples & Patterns</b></summary>

## Real-World Code Examples

### Example 1: Simple API

```nexus
@config { port: 3000 }

@model Product {
    id: number,
    name: string,
    price: number
}

@route GET "/api/products" {
    return database.query("SELECT * FROM products")
}

@route GET "/api/products/:id" {
    product = database.query("SELECT * FROM products WHERE id = ?", :id)
    return product || { error: "Not found" }
}

@route POST "/api/products" @auth @permission("admin") {
    product = request.body
    return database.insert("products", product)
}
```

### Example 2: Authentication

```nexus
@service AuthService {
    def register(email, password) {
        hashed = hash_password(password)
        user = database.insert("users", { email: email, password: hashed })
        token = generate_jwt(user.id)
        return { user: user, token: token }
    }
    
    def login(email, password) {
        user = database.query("SELECT * FROM users WHERE email = ?", email)
        if !user || !verify_password(password, user.password) {
            return { error: "Invalid credentials" }
        }
        token = generate_jwt(user.id)
        return { user: user, token: token }
    }
}

@route POST "/api/auth/register" {
    result = AuthService.register(request.body.email, request.body.password)
    return result.error ? { status: 401, error: result.error } : { status: 201, data: result }
}

@route POST "/api/auth/login" {
    result = AuthService.login(request.body.email, request.body.password)
    return result.error ? { status: 401, error: result.error } : { status: 200, data: result }
}
```

### Example 3: Background Jobs

```nexus
@task SendWelcomeEmails {
    cron: "0 9 * * *",
    queue: "emails",
    retry: 3,
    timeout: 30000
    
    new_users = database.query("SELECT * FROM users WHERE welcomed = false LIMIT 100")
    
    for user in new_users {
        try {
            send_email(user.email, "Welcome to Nexus!", "Welcome email HTML")
            database.update("users", user.id, { welcomed: true })
        } catch error {
            log.error("Failed to send welcome email", { user_id: user.id, error: error.message })
        }
    }
}
```

### Example 4: Frontend UI

```nexus
<view class="container">
    <header class="navbar">
        <h1>Todo App</h1>
        <btn @click="logout()">Logout</btn>
    </header>
    
    <section class="input-section">
        <input 
            type="text"
            @bind="newTodo"
            placeholder="Add a new todo..."
            @keypress="handleKeyPress"
        />
        <btn @click="addTodo()">Add</btn>
    </section>
    
    <section class="todos-section">
        <div id="todos-list">
            <!-- Todos rendered here -->
        </div>
    </section>
</view>
```

### Example 5: Caching & Performance

```nexus
@route GET "/api/expensive-operation" @cache(1800) @timeout(5000) {
    result = perform_expensive_calculation()
    return { data: result, cached: false }
}

@optimize {
    compression: true,
    minify: true
}

@cluster {
    nodes: ["server1", "server2", "server3"],
    strategy: "round_robin"
}
```

</details>

---

<details>
<summary><b>⚙️ Implementation Details</b></summary>

## How Nexus Works

### Architecture

```
Source Code (.nxs / .nxsjs)
        ↓
    Lexer (Tokenization)
        ↓
    Parser (AST Generation)
        ↓
    Interpreter (Execution)
        ↓
    Output
```

### Lexer (src/lexer.py)

Converts source code into tokens:

```python
# Example tokenization
Input:  let x = 42
Output: [Token(KEYWORD, 'let'), Token(IDENTIFIER, 'x'), 
         Token(OPERATOR, '='), Token(NUMBER, '42')]
```

### Parser (src/parser.py)

Builds Abstract Syntax Tree from tokens:

```
let x = 42
    ↓
VarDeclaration(
    name='x',
    value=Literal(42),
    mutable=False
)
```

### Interpreter (src/interpreter.py)

Executes the AST:

```python
class NexusInterpreter:
    def visit(self, node):
        if isinstance(node, VarDeclaration):
            # Execute variable declaration
        elif isinstance(node, BinaryOp):
            # Execute operation
        # ...
```

### Module System

Modules provide organization:

```nexus
~context UserManagement
  @in: user_data
  @out: saved_user
  saved_user => database.insert("users", user_data)
```

### Type System

Nexus uses optional typing with inference:

```nexus
let x = 42              # Type inferred as number
let name: string = "Alice"  # Explicit type
let items: pool = [1, 2, 3]  # Array type
```

### Memory Management

Variables are stored in environments:

```python
class NexusEnvironment:
    def __init__(self, parent=None):
        self.vars = {}      # Variable storage
        self.parent = parent  # Parent scope
```

### Error Handling

Errors are caught and reported:

```python
try:
    result = interpreter.visit(node)
except SyntaxError as e:
    print(f"Syntax Error: {e}")
except NameError as e:
    print(f"Name Error: {e}")
```

</details>

---

<details>
<summary><b>🌍 Ecosystem & Packages</b></summary>

## Available Modules

### Express (Web Framework)

```nexus
use express

app = express.create
app.get "/", |request| do
  return { status: 200, body: "Hello!" }
end
app.listen 3000
```

### Built-in Functions

- `println(value)` - Print to console
- `print(value)` - Print without newline
- `type_of(value)` - Get value type
- `length(value)` - Get length of collection
- `range(start, end)` - Create range
- `now()` - Current timestamp

### Database Integration

```nexus
database.query("SELECT * FROM users")
database.insert("users", { name: "Alice" })
database.update("users", id, { name: "Bob" })
database.delete("users", id)
```

### Package Manager

```bash
# Search for packages
nxs search http-client

# Install package
nxs install http-client

# View installed packages
nxs list

# Update package
nxs update http-client
```

### External Integrations

- **Database:** PostgreSQL, MySQL, SQLite, MongoDB
- **Cache:** Redis, Memcached
- **Auth:** JWT, OAuth2, SAML
- **Email:** SMTP, SendGrid, Mailgun
- **Storage:** AWS S3, Google Cloud Storage
- **Payment:** Stripe, PayPal, Square

</details>

---

<details>
<summary><b>🎭 Alternative Interpreters</b></summary>

## Different Ways to Run Nexus

### 1. CLI Interpreter (Default)

```bash
nexus program.nexus
```

- Direct AST interpretation
- Fastest for small scripts
- Best for development

### 2. REPL Mode

```bash
nexus --repl

> let x = 42
> println x
42
> def add(a, b) do return a + b end
> add(10, 20)
30
```

- Interactive exploration
- Real-time feedback
- Great for learning

### 3. Script Runner

```bash
nxs my-script.nexus --args "arg1" "arg2"
```

- Command-line arguments
- Exit codes
- Batch processing

### 4. Module Import

```nexus
use my-module
result = my-module.function()
```

- Code reuse
- Better organization
- Encapsulation

### 5. Library Mode

```python
from nexus import NexusInterpreter

interpreter = NexusInterpreter()
result = interpreter.execute("let x = 42")
```

- Embedding Nexus in Python
- Extended functionality
- Custom integrations

### Comparison

| Method | Speed | Interactivity | Use Case |
|--------|-------|---------------|----------|
| CLI | Fast | Low | Production |
| REPL | Fast | High | Development |
| Script | Fast | Medium | Automation |
| Module | Fast | Low | Code reuse |
| Library | Medium | Medium | Integration |

</details>

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

MIT# 

