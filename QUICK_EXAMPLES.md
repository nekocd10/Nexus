# Nexus Quick Examples

Real-world examples of using your new Nexus features.

## Example 1: Todo App (Full-Stack)

### Setup

```bash
nexus new todo-app
cd todo-app

# Install packages
nxs install express sqlite3 axios cors body-parser

# Start development
nexus dev
```

### Frontend: src/index.nxs

```nxs
<view class="container">
    <header>
        <h1>📝 Todo List</h1>
        <p class="subtitle">Never forget anything again</p>
    </header>
    
    <card class="input-card">
        <div class="input-group">
            <input 
                type="text" 
                placeholder="What needs to be done?" 
                @bind="newTodo"
                @keypress="handleKeyPress"
            />
            <btn @click="addTodo()">Add Todo</btn>
        </div>
    </card>
    
    <card class="todos-card">
        <div id="todos-list">
            <p class="empty">No todos yet. Add one to get started!</p>
        </div>
    </card>
</view>

<style>
    .container {
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
    }
    
    header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    h1 {
        font-size: 32px;
        margin-bottom: 5px;
    }
    
    .subtitle {
        color: #666;
        font-size: 14px;
    }
    
    card {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        padding: 20px;
        margin-bottom: 16px;
    }
    
    .input-group {
        display: flex;
        gap: 8px;
    }
    
    input {
        flex: 1;
        padding: 10px 12px;
        border: 1px solid #ddd;
        border-radius: 6px;
        font-size: 14px;
    }
    
    btn {
        background: #007AFF;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
    }
    
    btn:hover {
        background: #0051D5;
    }
    
    .empty {
        text-align: center;
        color: #999;
    }
</style>

<script>
    @state newTodo = ""
    @state todos = []
    @state loading = false
    
    // Load todos on startup
    async function loadTodos() {
        try {
            const response = await fetch('/api/todos')
            if (response.ok) {
                todos = await response.json()
                renderTodos()
            }
        } catch (error) {
            console.error('Error loading todos:', error)
        }
    }
    
    async function addTodo() {
        if (!newTodo.trim()) {
            alert('Please enter a todo!')
            return
        }
        
        loading = true
        try {
            const response = await fetch('/api/todos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: newTodo })
            })
            
            if (response.ok) {
                const todo = await response.json()
                todos.push(todo)
                newTodo = ""
                renderTodos()
            } else {
                alert('Failed to add todo')
            }
        } catch (error) {
            console.error('Error:', error)
        } finally {
            loading = false
        }
    }
    
    async function deleteTodo(id) {
        try {
            const response = await fetch(`/api/todos/${id}`, {
                method: 'DELETE'
            })
            
            if (response.ok) {
                todos = todos.filter(t => t.id !== id)
                renderTodos()
            }
        } catch (error) {
            console.error('Error:', error)
        }
    }
    
    async function toggleTodo(id) {
        const todo = todos.find(t => t.id === id)
        if (!todo) return
        
        try {
            const response = await fetch(`/api/todos/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ completed: !todo.completed })
            })
            
            if (response.ok) {
                todo.completed = !todo.completed
                renderTodos()
            }
        } catch (error) {
            console.error('Error:', error)
        }
    }
    
    function renderTodos() {
        const list = document.getElementById('todos-list')
        
        if (todos.length === 0) {
            list.innerHTML = '<p class="empty">No todos yet!</p>'
            return
        }
        
        list.innerHTML = todos.map(todo => `
            <div class="todo-item ${todo.completed ? 'completed' : ''}">
                <input 
                    type="checkbox" 
                    ${todo.completed ? 'checked' : ''}
                    onchange="toggleTodo(${todo.id})"
                />
                <span>${todo.title}</span>
                <btn onclick="deleteTodo(${todo.id})" class="delete-btn">Delete</btn>
            </div>
        `).join('')
    }
    
    function handleKeyPress(e) {
        if (e.key === 'Enter') {
            addTodo()
        }
    }
    
    // Load todos when page starts
    loadTodos()
</script>
```

### Backend: src/api.nxsjs

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

// Get all todos
@route GET "/api/todos" {
    SELECT * FROM Todo ORDER BY created_at DESC
}

// Get single todo
@route GET "/api/todos/:id" {
    SELECT * FROM Todo WHERE id = :id
}

// Create todo
@route POST "/api/todos" {
    INSERT INTO Todo (title, completed, created_at) 
    VALUES (?, false, datetime('now'))
    
    SELECT * FROM Todo WHERE id = last_insert_rowid()
}

// Update todo
@route PUT "/api/todos/:id" {
    UPDATE Todo SET completed = ? WHERE id = :id
    SELECT * FROM Todo WHERE id = :id
}

// Delete todo
@route DELETE "/api/todos/:id" {
    DELETE FROM Todo WHERE id = :id
}
```

### Configuration: nxs.json

```json
{
  "name": "todo-app",
  "version": "1.0.0",
  "description": "A simple todo application",
  "entry": {
    "frontend": "src/index.nxs",
    "backend": "src/api.nxsjs"
  },
  "output": {
    "frontend": "dist/index.html",
    "backend": "dist/api.py"
  },
  "dependencies": {
    "express": "^4.18.0",
    "sqlite3": "^5.1.0",
    "cors": "^2.8.5",
    "body-parser": "^1.20.0"
  },
  "scripts": {
    "dev": "nexus dev",
    "build": "nexus build",
    "start": "nexus dev --port 3000"
  }
}
```

### Run It

```bash
# Install dependencies
nxs install

# Start development server
nxs run dev

# Open browser to http://localhost:5000
```

---

## Example 2: Using Python Integration

### Create a Math API

```bash
nexus new math-api
cd math-api

nxs install numpy flask

# Create Python helper module
cat > src/calculations.py << 'EOF'
import math

def fibonacci(n):
    """Generate Fibonacci sequence"""
    a, b = 0, 1
    result = []
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result

def prime_factors(n):
    """Get prime factors"""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors
EOF
```

### Backend: src/api.nxsjs

```nxsjs
@config {
    port: 5000
}

@route GET "/api/fibonacci/:n" {
    result = call_python("calculations", "fibonacci", :n)
    return { sequence: result }
}

@route GET "/api/primes/:n" {
    result = call_python("calculations", "prime_factors", :n)
    return { factors: result }
}
```

### Frontend: src/index.nxs

```nxs
<view class="app">
    <h1>Math Operations</h1>
    
    <card>
        <h2>Fibonacci Sequence</h2>
        <input type="number" @bind="fibN" placeholder="Enter number" />
        <btn @click="getFibonacci()">Calculate</btn>
        <div id="fib-result"></div>
    </card>
    
    <card>
        <h2>Prime Factors</h2>
        <input type="number" @bind="primeN" placeholder="Enter number" />
        <btn @click="getPrimes()">Calculate</btn>
        <div id="prime-result"></div>
    </card>
</view>

<script>
    @state fibN = 10
    @state primeN = 100
    
    async function getFibonacci() {
        const res = await fetch(`/api/fibonacci/${fibN}`)
        const data = await res.json()
        document.getElementById('fib-result').innerHTML = 
            `<p>Sequence: ${data.sequence.join(', ')}</p>`
    }
    
    async function getPrimes() {
        const res = await fetch(`/api/primes/${primeN}`)
        const data = await res.json()
        document.getElementById('prime-result').innerHTML = 
            `<p>Factors: ${data.factors.join(', ')}</p>`
    }
</script>
```

---

## Example 3: Package Management

### Install Multiple Packages

```bash
nxs install react react-dom axios lodash uuid moment
nxs install --save-dev webpack jest eslint

# List all
nxs list

# Search for packages
nxs search "state management"
nxs search "database"

# Update all
nxs update
```

### Run Scripts

In nxs.json:
```json
{
  "scripts": {
    "dev": "nexus dev",
    "build": "nexus build --production",
    "test": "jest",
    "lint": "eslint src/**/*.nxs"
  }
}
```

Run with:
```bash
nxs run dev
nxs run build
nxs run test
nxs run lint
```

---

## Example 4: File Operations

### Backend: src/api.nxsjs

```nxsjs
@config { port: 5000 }

@route GET "/api/config" {
    content = file_read("config.json")
    return json_parse(content)
}

@route POST "/api/save-data" {
    file_write("data/output.json", json_stringify(data))
    return { saved: true }
}

@route GET "/api/files" {
    files = dir_list("public/")
    return { files: files }
}

@route POST "/api/backup" {
    file_write("backups/backup_" + timestamp + ".db", database_export())
    return { backed_up: true }
}
```

---

## Example 5: HTTP Integration

### Fetch External Data

```nxsjs
@config { port: 5000 }

@route GET "/api/weather/:city" {
    response = http_request(
        "GET",
        "https://api.weather.gov/points/" + :city,
        { "Accept": "application/json" }
    )
    
    if (response.ok) {
        data = json_parse(response.body)
        return data
    }
    
    return error("Weather not found", 404)
}

@route GET "/api/github/:user" {
    data = fetch_json("https://api.github.com/users/" + :user)
    return data
}
```

---

## Quick Command Reference

```bash
# Create & Setup
nexus new myapp                    # Create project
cd myapp
nxs install react express          # Install packages

# Development
nexus dev                          # Start dev server
nxs run dev                        # Same (via scripts)
nexus repl                         # Interactive shell

# Building
nexus build                        # Build project
nexus build --production           # Production build

# Packages
nxs list                           # List installed
nxs search query                   # Search packages
nxs update                         # Update all
nxs remove package                 # Remove package

# Utilities
nexus --version                    # Show version
nexus help                         # Show help
```

---

Enjoy building with Nexus! 🚀
