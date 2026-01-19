# Nexus Full-Stack Development Guide

Complete guide to using Nexus with all new features including package management, database integration, file system access, and interoperability.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Frontend Development (.nxs)](#frontend-development-nxs)
4. [Backend Development (.nxsjs)](#backend-development-nxsjs)
5. [Package Management](#package-management)
6. [Interoperability](#interoperability)
7. [Building & Deployment](#building--deployment)
8. [Examples](#examples)

## Installation

See [INSTALLATION.md](INSTALLATION.md) for detailed installation instructions.

Quick install:

```bash
git clone https://github.com/nekocd10/maybe-a-custom-language.git
cd maybe-a-custom-language
bash install.sh
```

## Quick Start

### Create a New Project

```bash
nexus new myapp
cd myapp
```

This generates:
- `src/index.nxs` - Frontend
- `src/api.nxsjs` - Backend
- `nxs.json` - Configuration
- `public/` - Static assets

### Start Development

```bash
# Install dependencies
nxs install express sqlite3 axios

# Start dev server
nexus dev

# Open http://localhost:5000
```

### Build for Production

```bash
nexus build

# Output in dist/
```

## Frontend Development (.nxs)

### Syntax Overview

.nxs files support three types of syntax:

1. **Standard HTML** - Normal HTML tags work as-is
2. **EJS Templates** - Template syntax from .ejs files
3. **Custom Components** - Nexus-specific components

### HTML & EJS Support

```nxs
<!-- Standard HTML -->
<div class="container">
    <h1>My App</h1>
    <p>Regular HTML works fine</p>
</div>

<!-- EJS Template Syntax -->
<% if (user) { %>
    <p>Welcome, <%= user.name %>!</p>
<% } %>

<!-- Unescaped output -->
<div><%- htmlContent %></div>
```

### Custom Components

```nxs
<view class="app">
    <!-- View: Flex container -->
    <h1>Welcome</h1>
    
    <!-- Card: Styled container -->
    <card>
        <h2>Contact Form</h2>
        
        <!-- Custom input binding -->
        <input type="text" placeholder="Name" @bind="name" />
        <input type="email" placeholder="Email" @bind="email" />
        
        <!-- Custom button -->
        <btn @click="submit()">Submit</btn>
    </card>
</view>

<style>
    .app { padding: 20px; }
    card { 
        background: white; 
        border-radius: 8px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>

<script>
    @state name = ""
    @state email = ""
    
    function submit() {
        console.log(`Name: ${name}, Email: ${email}`);
        // Send to backend
        fetch('/api/contact', {
            method: 'POST',
            body: JSON.stringify({ name, email })
        });
    }
</script>
```

### Component Reference

| Component | HTML Equivalent | Purpose |
|-----------|-----------------|---------|
| `<view>` | `<div>` with flexbox | Container with flexible layout |
| `<card>` | `<div>` with styling | Styled content card |
| `<btn>` | `<button>` | Interactive button |
| `<input>` | `<input>` | Form input with binding |

### Event Handling

```nxs
<!-- Click events -->
<btn @click="handleClick()">Click Me</btn>

<!-- Change events -->
<input @change="handleChange()" />

<!-- Input events -->
<input @input="handleInput()" />
```

### State Binding

```nxs
<script>
    @state counter = 0
    @state userName = ""
    @state items = [1, 2, 3]
    
    function increment() {
        counter = counter + 1
    }
</script>
```

## Backend Development (.nxsjs)

### Configuration

```nxsjs
@config {
    port: 5000,
    database: "app.db",
    cors: true,
    env: "development"
}
```

### Model Definition

```nxsjs
@model User {
    id: number,
    name: string,
    email: string,
    created_at: datetime
}

@model Post {
    id: number,
    title: string,
    content: text,
    author_id: number,
    created_at: datetime
}
```

### Routes & API Endpoints

```nxsjs
@route GET "/api/users" {
    SELECT * FROM users
}

@route GET "/api/users/:id" {
    SELECT * FROM users WHERE id = :id
}

@route POST "/api/users" @auth {
    INSERT INTO users (name, email) VALUES (?, ?)
}

@route PUT "/api/users/:id" @auth {
    UPDATE users SET name = ?, email = ? WHERE id = :id
}

@route DELETE "/api/users/:id" @admin {
    DELETE FROM users WHERE id = :id
}
```

### Middleware

```nxsjs
@middleware auth {
    // Check authentication token
    validate_token()
}

@middleware admin {
    // Check admin privileges
    check_admin_role()
}

@middleware logging {
    // Log requests
    log_request()
}
```

### Database Operations

```nxsjs
@model Product {
    id: number,
    name: string,
    price: number,
    stock: number
}

@route POST "/api/products" @auth {
    INSERT INTO Product (name, price, stock) 
    VALUES (?, ?, ?)
}

@route GET "/api/products/:id" {
    SELECT * FROM Product WHERE id = :id
}

@route PUT "/api/products/:id" @auth {
    UPDATE Product 
    SET name = ?, price = ?, stock = ? 
    WHERE id = :id
}
```

### File System Operations

```nxsjs
@route POST "/api/upload" @auth {
    // Write file
    file_write("uploads/data.json", content)
    
    // Read file
    data = file_read("config.json")
    
    // List directory
    files = dir_list("uploads/")
    
    // Delete file
    file_delete("temp.txt")
}
```

## Package Management

### Installing Packages

```bash
# Single package
nxs install react

# Multiple packages
nxs install express sqlite3 axios lodash

# Specific version
nxs install react@18.0.0

# From npm
nxs install @babel/core

# Dev dependencies
nxs install --save-dev webpack
```

### Searching Packages

```bash
nxs search database
nxs search http server
nxs search ui components
```

### Managing Dependencies

```bash
# List installed packages
nxs list

# Remove package
nxs remove react

# Update all packages
nxs update

# Update specific package
nxs install react@latest
```

### Running Scripts

Define scripts in `nxs.json`:

```json
{
  "scripts": {
    "dev": "nexus dev",
    "build": "nexus build",
    "start": "nexus dev --port 3000",
    "test": "python -m pytest",
    "lint": "eslint src/**/*.nxs"
  }
}
```

Run with:

```bash
nxs run dev
nxs run build
nxs run test
```

## Interoperability

### Calling Python Functions

```nxsjs
@import "math.py"

@route GET "/api/calculate" {
    result = call_python("math", "sqrt", 16)
    return result
}
```

### Using JavaScript Packages

```nxs
<script>
    // Use installed npm package
    import { v4 as uuidv4 } from 'uuid'
    
    @state id = uuidv4()
</script>
```

### HTTP Requests

```nxsjs
@route POST "/api/webhook" {
    response = http_request(
        "POST",
        "https://api.example.com/data",
        {
            "Content-Type": "application/json"
        },
        payload
    )
}
```

### Data Format Conversion

```nxsjs
@route GET "/api/data" {
    // Convert to JSON
    json_str = to_json(data)
    
    // Parse JSON
    obj = from_json(json_string)
    
    // Convert to dict
    dict = to_dict(keyed_pool)
}
```

## Building & Deployment

### Development Mode

```bash
# Watch mode - rebuilds on changes
nexus dev

# Watch mode on specific port
nexus dev 3000

# REPL mode
nexus repl
```

### Building

```bash
# Development build
nexus build

# Production build (optimized)
nexus build --production

# With bundling
nexus build --bundle
```

### Deployment

```bash
# Build for production
nexus build --production

# Output is in dist/
# Deploy dist/ to your server
```

### Build Configuration

In `nxs.json`:

```json
{
  "name": "myapp",
  "version": "1.0.0",
  "entry": {
    "frontend": "src/index.nxs",
    "backend": "src/api.nxsjs"
  },
  "output": {
    "frontend": "dist/index.html",
    "backend": "dist/app.py"
  },
  "build": {
    "minify": true,
    "bundler": "nexus",
    "sourceMap": true,
    "optimize": true
  }
}
```

## Examples

### Complete Todo App

**src/index.nxs** - Frontend

```nxs
<view class="app">
    <h1>My Todos</h1>
    
    <card>
        <input 
            type="text" 
            placeholder="Add a todo..." 
            @bind="inputValue" 
            @keypress="handleKeyPress"
        />
        <btn @click="addTodo()">Add</btn>
    </card>
    
    <card>
        <div id="todos">
            <!-- Todos will be rendered here -->
        </div>
    </card>
</view>

<style>
    .app { max-width: 600px; margin: 0 auto; padding: 20px; }
    card { 
        background: white; 
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
    }
    btn { 
        background: #007AFF; 
        color: white; 
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .todo-item {
        padding: 8px;
        border-bottom: 1px solid #eee;
    }
</style>

<script>
    @state inputValue = ""
    @state todos = []
    
    async function addTodo() {
        if (!inputValue.trim()) return
        
        const response = await fetch('/api/todos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: inputValue })
        })
        
        if (response.ok) {
            const todo = await response.json()
            todos.push(todo)
            inputValue = ""
            renderTodos()
        }
    }
    
    function renderTodos() {
        const todosDiv = document.getElementById('todos')
        todosDiv.innerHTML = todos.map(t => `
            <div class="todo-item">
                ${t.title}
                <btn @click="deleteTodo(${t.id})">Delete</btn>
            </div>
        `).join('')
    }
    
    function handleKeyPress(e) {
        if (e.key === 'Enter') {
            addTodo()
        }
    }
</script>
```

**src/api.nxsjs** - Backend

```nxsjs
@config {
    port: 5000,
    database: "todos.db",
    cors: true
}

@model Todo {
    id: number,
    title: string,
    completed: boolean,
    created_at: datetime
}

@route GET "/api/todos" {
    SELECT * FROM Todo ORDER BY created_at DESC
}

@route POST "/api/todos" @auth {
    INSERT INTO Todo (title, completed, created_at) 
    VALUES (?, false, datetime('now'))
    
    SELECT * FROM Todo WHERE id = last_insert_rowid()
}

@route PUT "/api/todos/:id" @auth {
    UPDATE Todo SET completed = ? WHERE id = :id
    SELECT * FROM Todo WHERE id = :id
}

@route DELETE "/api/todos/:id" @auth {
    DELETE FROM Todo WHERE id = :id
}

@middleware auth {
    // Verify user is authenticated
    validate_token()
}
```

**nxs.json** - Configuration

```json
{
  "name": "todo-app",
  "version": "1.0.0",
  "description": "A full-stack Todo application",
  "entry": {
    "frontend": "src/index.nxs",
    "backend": "src/api.nxsjs"
  },
  "output": {
    "frontend": "dist/index.html",
    "backend": "dist/app.py"
  },
  "dependencies": {
    "express": "^4.18.0",
    "sqlite3": "^5.1.0",
    "axios": "^1.3.0"
  },
  "scripts": {
    "dev": "nexus dev",
    "build": "nexus build",
    "start": "nexus dev --port 3000"
  }
}
```

## Advanced Topics

### Environment Variables

```bash
# .env file
NEXUS_ENV=development
DATABASE_URL=sqlite:///app.db
API_KEY=secret123
```

Access in code:

```nxsjs
@route GET "/api/status" {
    env = get_environment()
    return { environment: env.NEXUS_ENV }
}
```

### Error Handling

```nxs
<script>
    async function fetchData() {
        try {
            const res = await fetch('/api/data')
            if (!res.ok) throw new Error('Failed to fetch')
            return await res.json()
        } catch (error) {
            console.error('Error:', error)
            return null
        }
    }
</script>
```

### Authentication

```nxsjs
@route POST "/api/login" {
    user = find_user_by_email(email)
    if (verify_password(password, user.hash)) {
        token = generate_jwt_token(user.id)
        return { token: token }
    }
    return error("Invalid credentials")
}

@middleware auth {
    token = get_auth_header()
    user = verify_jwt_token(token)
    if (!user) {
        return error("Unauthorized", 401)
    }
}
```

## Resources

- [Language Specification](NEXUS_SPEC.md)
- [Implementation Guide](IMPLEMENTATION_GUIDE.md)
- [GitHub Repository](https://github.com/nekocd10/maybe-a-custom-language)
- [Examples Directory](nexus_examples/)

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review example projects
