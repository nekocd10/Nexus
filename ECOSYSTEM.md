# Nexus Ecosystem - Complete Guide

## Overview

Nexus is a complete full-stack programming ecosystem featuring:
- **Nexus Language**: A completely original programming language with unique paradigms
- **Package Manager (nxs)**: Package management with npm compatibility
- **Frontend Language (.nxs)**: HTML + custom GUI components that compile to browser-compatible code
- **Backend Language (.nxsjs)**: Decorator-based backend with database, API, and file handling
- **Build System**: Bundler and compiler for entire projects
- **Interoperability**: Call Python, JavaScript, and native code from Nexus

## Installation

```bash
# Clone or install Nexus
git clone https://github.com/nexus-lang/nexus.git
cd nexus

# Make CLI executable
chmod +x nexus_cli.py

# Create symlink for easy access (optional)
ln -s $(pwd)/nexus_cli.py /usr/local/bin/nexus
```

## Quick Start

### Create a new project
```bash
nexus new my-app
cd my-app
```

### Install dependencies
```bash
nexus nxs install react
nexus nxs install express
```

### Start development
```bash
nexus dev
```

This will:
- Compile `.nxs` frontend files to HTML/CSS/JS
- Compile `.nxsjs` backend files to Python Flask apps
- Start a dev server on http://localhost:5000
- Watch for file changes and auto-rebuild

## Project Structure

```
my-app/
├── src/
│   ├── index.nxs           # Frontend entry point
│   ├── api.nxsjs           # Backend entry point
│   ├── components/         # Reusable components
│   └── utils/              # Utility functions
├── public/                 # Static assets
├── dist/                   # Compiled output
├── nxs.json               # Project configuration
└── README.md
```

## Configuration (nxs.json)

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "entry": {
    "frontend": "src/index.nxs",
    "backend": "src/api.nxsjs"
  },
  "output": {
    "frontend": "dist/index.html",
    "backend": "dist/app.py"
  },
  "dependencies": {
    "react": "^18.0.0",
    "express": "^4.18.0"
  },
  "devDependencies": {
    "nexus-cli": "latest"
  }
}
```

## CLI Commands

### Project Management
```bash
nexus new <project-name>        # Create new project
nexus nxs install <package>     # Install package
nexus nxs remove <package>      # Remove package
nexus nxs search <query>        # Search packages
nexus nxs list                  # List installed packages
```

### Development
```bash
nexus run <file.nexus>          # Run a Nexus file
nexus dev [port]                # Start dev server (default: 5000)
nexus build                     # Build for production
nexus deploy [environment]      # Deploy to production
nexus repl                      # Interactive REPL
```

### Information
```bash
nexus version                   # Show version
nexus help                      # Show help
```

## Frontend Language (.nxs)

### Basic Structure

```html
<view class="app">
    <h1>Welcome</h1>
    <card>
        <h2>My Card</h2>
        <p>Content goes here</p>
    </card>
</view>

<style>
.app { max-width: 1200px; margin: 0 auto; }
</style>

<script>
function handleClick() {
    console.log('Clicked!');
}
</script>
```

### Custom Components

```html
<!-- View Container -->
<view class="container">
    Content
</view>

<!-- Card Component -->
<card>
    <h2>Title</h2>
    <p>Content</p>
</card>

<!-- Button -->
<btn @click="handleClick()">Click Me</btn>

<!-- Input with binding -->
<input type="text" @bind="fieldName" placeholder="Enter text" />
```

### State Management

```javascript
@state userName = "John"
@state userEmail = "john@example.com"
@state counter = 0

function incrementCounter() {
    counter++;
    updateDisplay();
}

function updateDisplay() {
    document.getElementById("count").textContent = counter;
}
```

### Event Handling

```html
<!-- Click event -->
<btn @click="handleClick()">Click</btn>

<!-- Change event -->
<input type="checkbox" @change="handleChange()" />

<!-- Input event -->
<input type="text" @input="handleInput()" />
```

### Example Frontend Application

```html
<view class="container">
    <h1>Todo App</h1>
    
    <card class="input-section">
        <input type="text" @bind="newTodo" placeholder="Add a todo..." />
        <btn @click="addTodo()">Add</btn>
    </card>
    
    <card class="todo-list">
        <h2>Todos</h2>
        <div id="todos"></div>
    </card>
</view>

<style>
.container { max-width: 600px; margin: 50px auto; }
.input-section { display: flex; gap: 10px; }
.todo-list { margin-top: 20px; }
input { flex: 1; padding: 8px; border: 1px solid #ddd; }
btn { padding: 8px 16px; background: #007bff; color: white; border: none; cursor: pointer; }
</style>

<script>
@state newTodo = ""
@state todos = []

function addTodo() {
    if (newTodo.trim()) {
        todos.push(newTodo);
        newTodo = "";
        renderTodos();
    }
}

function renderTodos() {
    const container = document.getElementById("todos");
    container.innerHTML = todos.map((todo, i) => 
        `<div class="todo-item">${todo} 
            <btn @click="removeTodo(${i})">✕</btn>
        </div>`
    ).join('');
}

function removeTodo(index) {
    todos.splice(index, 1);
    renderTodos();
}
</script>
```

## Backend Language (.nxsjs)

### Configuration

```javascript
@config {
    port: 5000,
    database: "app.db",
    cors: true,
    environment: "development"
}
```

### Models

```javascript
@model User {
    id: number,
    name: string,
    email: string,
    created_at: datetime,
    updated_at: datetime
}

@model Post {
    id: number,
    user_id: number,
    title: string,
    content: string,
    created_at: datetime
}
```

### Routes

```javascript
// GET request
@route GET "/api/users" {
    SELECT * FROM users
}

// GET with parameter
@route GET "/api/users/:id" {
    SELECT * FROM users WHERE id = :id
}

// POST request
@route POST "/api/users" @auth {
    INSERT INTO users (name, email) VALUES (?, ?)
}

// PUT request
@route PUT "/api/users/:id" @auth {
    UPDATE users SET name = ?, email = ? WHERE id = :id
}

// DELETE request
@route DELETE "/api/users/:id" @admin {
    DELETE FROM users WHERE id = :id
}
```

### Middleware

```javascript
@middleware auth {
    print("Checking authentication")
    // Verify JWT token
}

@middleware admin {
    print("Checking admin role")
    // Verify admin permissions
}

@middleware cors {
    print("Setting CORS headers")
    // Set cross-origin headers
}
```

### Example Backend Application

```javascript
@config {
    port: 5000,
    database: "blog.db"
}

@model User {
    id: number,
    username: string,
    email: string,
    password: string,
    created_at: datetime
}

@model Post {
    id: number,
    user_id: number,
    title: string,
    content: string,
    published: boolean,
    created_at: datetime
}

@route GET "/api/posts" {
    SELECT * FROM posts WHERE published = true
}

@route GET "/api/posts/:id" {
    SELECT * FROM posts WHERE id = :id
}

@route POST "/api/posts" @auth {
    INSERT INTO posts (user_id, title, content, published)
    VALUES (?, ?, ?, ?)
}

@route PUT "/api/posts/:id" @auth {
    UPDATE posts SET title = ?, content = ? WHERE id = :id
}

@route DELETE "/api/posts/:id" @auth {
    DELETE FROM posts WHERE id = :id
}

@middleware auth {
    print("Verifying user authentication")
}
```

## Nexus Core Language

### Contexts (Functions)

```nexus
~context greet name {
    "Hello, " ++ name => output
}

greet "Alice" => result
```

### Pools (Data Structures)

```nexus
[| 1, 2, 3, 4, 5 |] => numbers
[: name: "Alice", age: 30 :] => person
```

### Data Flows

```nexus
5 => x
x ++ 3 => y
y ** 2 => result
```

### Pattern Matching

```nexus
~gate checkNumber n {
    ? n > 0 => "positive"
    ? n < 0 => "negative"
    ? n == 0 => "zero"
}

-5 => n
checkNumber n => category
```

### Loops

```nexus
~reaction iterate {
    [| 1, 2, 3 |] => items
    ? items => process each item
}
```

## Package Manager (nxs)

### Commands

```bash
# Install a package
nexus nxs install <package> [version]
nexus nxs install react
nexus nxs install express@4.18.0

# Remove a package
nexus nxs remove <package>
nexus nxs remove react

# Search packages
nexus nxs search database
nexus nxs search <query>

# List installed packages
nexus nxs list

# Publish a package
nexus nxs publish

# View version
nexus nxs version
```

### Package Sources

The package manager searches in this order:
1. npm registry (if available)
2. Custom Nexus registry
3. Local packages (`./node_modules`, `./nxs_modules`)

### Creating a Package

```json
{
  "name": "my-package",
  "version": "1.0.0",
  "description": "A Nexus package",
  "main": "index.nexus",
  "exports": {
    "greet": "function greet(name) { return 'Hello ' + name; }",
    "calculate": "function calculate(x, y) { return x + y; }"
  },
  "dependencies": {},
  "keywords": ["utility", "helpers"]
}
```

## Build System

### Building

```bash
nexus build
```

Generates:
- `dist/index.html` - Compiled frontend
- `dist/app.py` - Compiled backend
- `dist/assets/` - Static files

### Development Mode

```bash
nexus dev [port]
```

Starts a dev server with:
- Hot reloading on file changes
- Error reporting
- Debugging tools
- Local API server

### Production Deployment

```bash
nexus build
nexus deploy production
```

Creates optimized artifacts for deployment:
- Minified HTML/CSS/JS
- Compiled Python Flask app
- Dependency information

## Interoperability

### Calling Python from Nexus

```python
# In your Python code
from nxs_interop import NexusInterop

interop = NexusInterop()

def my_python_function(x, y):
    return x + y

interop.register_python_function("add", my_python_function)
```

Then from Nexus:
```nexus
@import python.add
add 5 3 => result
```

### Calling JavaScript from Nexus

```javascript
// In your JavaScript
const myJsFunction = (x, y) => x * y;
exports.multiply = myJsFunction;
```

From Nexus:
```nexus
@import js.multiply
multiply 4 5 => result
```

### Module Loading

```nexus
@import "react" as React
@import "./utils" as utils
@import "database.py" as db

utils.helper => result
```

## Examples

### Example 1: Simple Todo App

**src/index.nxs** (Frontend)
```html
<view class="app">
    <h1>My Todos</h1>
    <input type="text" @bind="todoText" placeholder="Add a todo" />
    <btn @click="addTodo()">Add</btn>
    <div id="list"></div>
</view>

<script>
@state todoText = ""
@state todos = []

async function addTodo() {
    const response = await fetch('/api/todos', {
        method: 'POST',
        body: JSON.stringify({ text: todoText })
    });
    const todo = await response.json();
    todos.push(todo);
    todoText = "";
    render();
}

function render() {
    document.getElementById("list").innerHTML = 
        todos.map(t => `<div>${t.text}</div>`).join('');
}
</script>
```

**src/api.nxsjs** (Backend)
```javascript
@config {
    port: 5000,
    database: "todos.db"
}

@model Todo {
    id: number,
    text: string,
    completed: boolean
}

@route GET "/api/todos" {
    SELECT * FROM todos
}

@route POST "/api/todos" {
    INSERT INTO todos (text, completed) VALUES (?, false)
}
```

### Example 2: Using Nexus Core Language

**examples/data_processing.nexus**
```nexus
~context processNumbers nums {
    nums => data
    data ++ 100 => adjusted
    adjusted => output
}

[| 10, 20, 30 |] => myNumbers
processNumbers myNumbers => result
```

## Troubleshooting

### Port Already in Use
```bash
nexus dev 3000  # Use different port
```

### Module Not Found
```bash
# Ensure nxs.json exists
# Reinstall packages
nexus nxs install
```

### Build Errors
```bash
# Check for syntax errors
nexus run your-file.nexus

# Enable debug mode
nexus dev --debug
```

## Performance Tips

1. **Optimize builds**: Use `nexus build --minify`
2. **Enable caching**: Configure in `nxs.json`
3. **Lazy load modules**: Use dynamic imports
4. **Bundle size**: Monitor with `nexus analyze`

## Contributing

Contributions welcome! Please submit issues and pull requests.

## License

MIT - See LICENSE file

## Resources

- **Documentation**: Full Nexus specification and API docs
- **Examples**: Complete working examples in `/examples`
- **Community**: Join our Discord/forums
- **Blog**: Tutorials and best practices

---

For more information, visit [nexus.dev](https://nexus.dev)
