#!/usr/bin/env python3
"""
Nexus Complete Stack Example
A full working example of a Nexus application
"""

# Example 1: Hello World Application
HELLO_WORLD_FRONTEND = """<view class="container">
    <h1>Hello Nexus</h1>
    <p>Welcome to your first Nexus application!</p>
</view>

<style>
.container {
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    text-align: center;
    font-family: Arial, sans-serif;
}
</style>
"""

HELLO_WORLD_BACKEND = """@config {
    port: 5000,
    database: "hello.db"
}

@route GET "/api/message" {
    SELECT "Hello from Nexus!" as message
}
"""

# Example 2: Counter Application
COUNTER_FRONTEND = """<view class="app">
    <h1>Counter Application</h1>
    
    <card>
        <h2 id="counter-value">0</h2>
        <div class="buttons">
            <btn @click="increment()">+</btn>
            <btn @click="decrement()">-</btn>
            <btn @click="reset()">Reset</btn>
        </div>
    </card>
    
    <card>
        <h3>History</h3>
        <div id="history"></div>
    </card>
</view>

<style>
.app {
    max-width: 600px;
    margin: 50px auto;
    font-family: Arial, sans-serif;
}

.card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
}

.buttons {
    display: flex;
    gap: 10px;
    justify-content: center;
}

btn {
    padding: 10px 20px;
    font-size: 16px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

btn:hover {
    background: #0056b3;
}

h2 {
    font-size: 48px;
    margin: 20px 0;
    color: #007bff;
}
</style>

<script>
@state counter = 0
@state history = []

function increment() {
    counter++;
    updateDisplay();
}

function decrement() {
    counter--;
    updateDisplay();
}

function reset() {
    history.push(`Counter was ${counter}`);
    counter = 0;
    updateDisplay();
}

function updateDisplay() {
    document.getElementById("counter-value").textContent = counter;
    document.getElementById("history").innerHTML = 
        history.map(h => `<p>• ${h}</p>`).join('');
}
</script>
"""

COUNTER_BACKEND = """@config {
    port: 5000,
    database: "counter.db"
}

@model CounterEvent {
    id: number,
    value: number,
    action: string,
    timestamp: datetime
}

@route GET "/api/counter" {
    SELECT * FROM counter_events ORDER BY timestamp DESC LIMIT 10
}

@route POST "/api/counter" {
    INSERT INTO counter_events (value, action, timestamp)
    VALUES (?, ?, datetime('now'))
}
"""

# Example 3: Todo App
TODO_FRONTEND = """<view class="todo-app">
    <h1>📝 Todo Application</h1>
    
    <card class="input-section">
        <div class="input-group">
            <input type="text" @bind="newTodo" placeholder="Add a new todo..." />
            <btn @click="addTodo()">Add</btn>
        </div>
    </card>
    
    <card class="stats">
        <p>Total: <span id="total">0</span></p>
        <p>Completed: <span id="completed">0</span></p>
    </card>
    
    <card class="todo-list">
        <h2>Todos</h2>
        <div id="todos"></div>
    </card>
</view>

<style>
.todo-app {
    max-width: 700px;
    margin: 50px auto;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.input-group {
    display: flex;
    gap: 10px;
}

input {
    flex: 1;
    padding: 10px 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}

btn {
    padding: 10px 20px;
    background: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}

btn:hover {
    background: #218838;
}

.todo-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    background: #f9f9f9;
    margin: 8px 0;
    border-radius: 4px;
    border-left: 4px solid #007bff;
}

.todo-item.completed {
    opacity: 0.6;
    text-decoration: line-through;
}

.todo-actions {
    display: flex;
    gap: 5px;
}

.todo-actions btn {
    padding: 5px 10px;
    font-size: 12px;
}

.delete-btn {
    background: #dc3545;
}

.delete-btn:hover {
    background: #c82333;
}

.complete-btn {
    background: #28a745;
}

.complete-btn:hover {
    background: #218838;
}

.stats {
    background: #f0f0f0;
}

.stats p {
    margin: 8px 0;
    font-weight: bold;
}
</style>

<script>
@state newTodo = ""
@state todos = []

async function addTodo() {
    if (!newTodo.trim()) return;
    
    const response = await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: newTodo })
    });
    
    const todo = await response.json();
    todos.push(todo);
    newTodo = "";
    renderTodos();
}

async function toggleComplete(id) {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;
    
    const response = await fetch(`/api/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !todo.completed })
    });
    
    const updated = await response.json();
    const index = todos.findIndex(t => t.id === id);
    todos[index] = updated;
    renderTodos();
}

async function deleteTodo(id) {
    await fetch(`/api/todos/${id}`, { method: 'DELETE' });
    todos = todos.filter(t => t.id !== id);
    renderTodos();
}

function renderTodos() {
    const completed = todos.filter(t => t.completed).length;
    document.getElementById("total").textContent = todos.length;
    document.getElementById("completed").textContent = completed;
    
    document.getElementById("todos").innerHTML = todos.map(todo =>
        `<div class="todo-item ${todo.completed ? 'completed' : ''}">
            <span>${todo.text}</span>
            <div class="todo-actions">
                <btn class="complete-btn" onclick="toggleComplete(${todo.id})">
                    ${todo.completed ? '↩' : '✓'}
                </btn>
                <btn class="delete-btn" onclick="deleteTodo(${todo.id})">✕</btn>
            </div>
        </div>`
    ).join('');
}

// Load todos on startup
async function loadTodos() {
    const response = await fetch('/api/todos');
    todos = await response.json();
    renderTodos();
}

loadTodos();
</script>
"""

TODO_BACKEND = """@config {
    port: 5000,
    database: "todos.db"
}

@model Todo {
    id: number,
    text: string,
    completed: boolean,
    created_at: datetime,
    updated_at: datetime
}

@route GET "/api/todos" {
    SELECT * FROM todos ORDER BY created_at DESC
}

@route GET "/api/todos/:id" {
    SELECT * FROM todos WHERE id = :id
}

@route POST "/api/todos" {
    INSERT INTO todos (text, completed, created_at, updated_at)
    VALUES (?, false, datetime('now'), datetime('now'))
}

@route PUT "/api/todos/:id" {
    UPDATE todos SET completed = ?, updated_at = datetime('now') 
    WHERE id = :id
}

@route DELETE "/api/todos/:id" {
    DELETE FROM todos WHERE id = :id
}

@middleware log_request {
    print("Request received")
}
"""

# Example 4: Core Language Algorithm
NEXUS_ALGORITHM = """
~context fibonacci n {
    ? n <= 1 => n
    ? n > 1 => {
        (n - 1) => n1
        (n - 2) => n2
        fibonacci n1 => fib1
        fibonacci n2 => fib2
        (fib1 ++ fib2) => result
        result
    }
}

10 => input
fibonacci input => sequence
"""

# Example 5: Data Processing
NEXUS_DATA_PROCESSING = """
[| 1, 2, 3, 4, 5 |] => numbers

~context processArray arr {
    arr => data
    data ++ 10 => adjusted
    adjusted => filtered
    filtered
}

numbers => nums
processArray nums => result
"""

# Function to generate project files
def generate_example_project(project_name: str, example_type: str):
    """Generate complete example project"""
    
    examples = {
        "hello": (HELLO_WORLD_FRONTEND, HELLO_WORLD_BACKEND),
        "counter": (COUNTER_FRONTEND, COUNTER_BACKEND),
        "todo": (TODO_FRONTEND, TODO_BACKEND),
    }
    
    if example_type not in examples:
        print(f"Unknown example: {example_type}")
        return
    
    frontend, backend = examples[example_type]
    
    print(f"Generating {example_type} example: {project_name}")
    
    # Create directories
    import os
    from pathlib import Path
    
    base = Path(project_name)
    base.mkdir(exist_ok=True)
    (base / "src").mkdir(exist_ok=True)
    (base / "public").mkdir(exist_ok=True)
    
    # Write files
    with open(base / "src" / "index.nxs", "w") as f:
        f.write(frontend)
    
    with open(base / "src" / "api.nxsjs", "w") as f:
        f.write(backend)
    
    # Create nxs.json
    import json
    config = {
        "name": project_name,
        "version": "1.0.0",
        "description": f"Nexus {example_type} example",
        "entry": {
            "frontend": "src/index.nxs",
            "backend": "src/api.nxsjs"
        },
        "output": {
            "frontend": "dist/index.html",
            "backend": "dist/app.py"
        },
        "dependencies": {},
        "scripts": {
            "dev": "nexus dev",
            "build": "nexus build"
        }
    }
    
    with open(base / "nxs.json", "w") as f:
        json.dump(config, f, indent=2)
    
    # Create README
    readme = f"""# {project_name} - Nexus {example_type.title()} Example

A simple Nexus application demonstrating {example_type} functionality.

## Getting Started

```bash
# Build the project
nexus build

# Start development server
nexus dev

# Open http://localhost:5000 in your browser
```

## Project Structure

- `src/index.nxs` - Frontend UI components
- `src/api.nxsjs` - Backend API routes
- `dist/` - Compiled output
- `nxs.json` - Project configuration

## Commands

```bash
nexus dev              # Start development server
nexus build            # Build for production
nexus nxs install      # Install dependencies
nexus deploy           # Deploy to production
```

---

Built with [Nexus](https://nexus.dev)
"""
    
    with open(base / "README.md", "w") as f:
        f.write(readme)
    
    print(f"✅ Example created at {project_name}/")
    print(f"   cd {project_name}")
    print(f"   nexus dev")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Nexus Example Generator")
        print()
        print("Usage: python examples.py <example-type> [project-name]")
        print()
        print("Available examples:")
        print("  hello    - Hello World application")
        print("  counter  - Counter application")
        print("  todo     - Todo application")
        print()
        print("Examples:")
        print("  python examples.py hello my-hello")
        print("  python examples.py counter my-counter")
        print("  python examples.py todo my-todo")
        return
    
    example_type = sys.argv[1]
    project_name = sys.argv[2] if len(sys.argv) > 2 else f"nexus-{example_type}"
    
    generate_example_project(project_name, example_type)


if __name__ == "__main__":
    main()
