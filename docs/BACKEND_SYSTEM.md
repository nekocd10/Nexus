# Nexus Backend System (.nxsjs)

## Overview

`.nxsjs` files define the complete backend of a Nexus application using **decorators** and **configuration**. This is a completely different language from JavaScript - it uses Nexus syntax exclusively.

## File Structure

```
src/
├── api.nxsjs          # Main backend entry point
├── api/
│   ├── users.nxsjs    # User service
│   ├── posts.nxsjs    # Post service
│   └── payments.nxsjs # Payment service
└── models/
    └── schema.nxsjs   # Data models
```

## Core Decorators

### Application & Environment

```nexus
@config {
    port: 5000,
    host: "0.0.0.0",
    database: "nexus.db",
    redis: "redis://localhost:6379",
    environment: "production",
    debug: false
}

@env {
    DATABASE_URL: "...",
    API_KEY: "...",
    SECRET: "..."
}

@profile "production" { ... }
@profile "development" { ... }
@profile "testing" { ... }

@feature "new-ui" { enabled: true }
@flag "beta-api" { enabled: false }
```

### HTTP Routes

```nexus
@route GET "/api/users" {
    return database.query("SELECT * FROM users")
}

@route GET "/api/users/:id" {
    user = database.query("SELECT * FROM users WHERE id = ?", :id)
    return user
}

@route POST "/api/users" @validate @auth {
    new_user = request.body
    return database.insert("users", new_user)
}

@route PUT "/api/users/:id" @auth {
    return database.update("users", :id, request.body)
}

@route DELETE "/api/users/:id" @auth @permission("admin") {
    database.delete("users", :id)
    return { status: 204 }
}

@route PATCH "/api/users/:id" @auth {
    return database.partial_update("users", :id, request.body)
}
```

### Data Models

```nexus
@model User {
    id: number,
    name: string,
    email: string,
    password: string,
    created_at: date,
    updated_at: date
}

@model Post {
    id: number,
    user_id: number,
    title: string,
    content: string,
    published: boolean
}

@model Comment {
    id: number,
    post_id: number,
    user_id: number,
    text: string,
    created_at: date
}
```

### Middleware

```nexus
@middleware auth {
    token = request.headers["authorization"]
    if !token {
        return { error: "Unauthorized" }
    }
    request.user = verify_token(token)
}

@middleware errorHandler {
    try {
        next()
    } catch error {
        log.error(error.message)
        return { status: 500, error: error.message }
    }
}

@middleware corsHandler {
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE"
}

@middleware requestLogger {
    start_time = now()
    result = next()
    duration = now() - start_time
    log.info("Request completed", {
        path: request.path,
        method: request.method,
        duration_ms: duration
    })
    return result
}
```

### Validation & Sanitization

```nexus
@validate {
    schema: {
        name: { type: "string", required: true },
        email: { type: "string", pattern: "email", required: true },
        age: { type: "number", min: 18 }
    }
}

@schema User {
    name: string,
    email: string @unique,
    age: number
}

@sanitize {
    remove_html: true,
    trim_whitespace: true,
    escape_special_chars: true
}
```

### Services & Modules

```nexus
@service UserService {
    def create_user(name, email) {
        user = { name: name, email: email }
        return database.insert("users", user)
    }
    
    def get_user(id) {
        return database.query("SELECT * FROM users WHERE id = ?", id)
    }
}

@service EmailService {
    def send_email(to, subject, body) {
        return smtp.send({
            to: to,
            subject: subject,
            html: body
        })
    }
}

@module paymentModule {
    def process_payment(amount, currency) {
        // Payment logic
    }
}
```

### Background Jobs & Tasks

```nexus
@task ProcessEmails {
    cron: "0 * * * *",
    queue: "emails",
    retry: 3,
    timeout: 60000
    
    emails = database.query("SELECT * FROM emails WHERE sent = false")
    for email in emails {
        send_email(email.to, email.subject, email.body)
        database.update("emails", email.id, { sent: true })
    }
}

@task CleanupExpiredSessions {
    cron: "0 2 * * *",
    queue: "maintenance",
    timeout: 30000
    
    database.query("DELETE FROM sessions WHERE expires_at < NOW()")
}

@worker ProcessPayments {
    queue: "payments",
    concurrency: 5,
    timeout: 120000
}

@queue emails {
    max_retries: 3,
    visibility_timeout: 300
}
```

### Security & Authorization

```nexus
@auth {
    strategy: "jwt",
    secret: env.JWT_SECRET,
    algorithms: ["HS256"]
}

@permission "admin" {
    check: fn(user) => user.is_admin
}

@permission "premium" {
    check: fn(user) => user.subscription == "premium"
}

@role "admin" {
    permissions: ["read", "write", "delete", "manage_users"]
}

@role "user" {
    permissions: ["read", "write"]
}

@policy "data_owner" {
    check: fn(user, resource) => user.id == resource.user_id
}

@rateLimit(100, 60000) {
    // 100 requests per minute
}

@cors {
    origins: ["https://app.nexus.dev", "https://localhost:3000"],
    methods: ["GET", "POST", "PUT", "DELETE"],
    credentials: true
}

@csrf {
    enabled: true,
    token_name: "x-csrf-token"
}
```

### Caching & Performance

```nexus
@cache {
    ttl: 3600,
    backend: "redis",
    key_prefix: "api_"
}

@cache GET "/api/posts" {
    ttl: 1800
}

@optimize {
    compression: true,
    minify: true,
    lazy_load: true
}

@index "posts" on ["user_id", "created_at"] { ... }

@parallel {
    max_workers: 4,
    timeout: 10000
}

@cluster {
    nodes: ["node1", "node2", "node3"],
    strategy: "round_robin"
}

@loadBalance {
    strategy: "least_connections",
    health_check_interval: 10000
}
```

### Error Handling & Resilience

```nexus
@error {
    on NotFoundError {
        return { status: 404, error: "Not found" }
    }
    
    on ValidationError {
        return { status: 400, error: "Validation failed" }
    }
    
    on ServerError {
        log.error(error)
        return { status: 500, error: "Internal error" }
    }
}

@retry {
    max_attempts: 3,
    backoff: "exponential",
    initial_delay: 1000,
    max_delay: 10000
}

@fallback {
    return { status: 503, error: "Service unavailable" }
}

@timeout 30000 { ... }

@circuitBreaker {
    failure_threshold: 5,
    success_threshold: 2,
    timeout: 60000
}
```

### Observability

```nexus
@log {
    level: "info",
    format: "json",
    transports: ["console", "file"]
}

@trace {
    enabled: true,
    sample_rate: 0.1,
    backend: "jaeger"
}

@metric {
    enabled: true,
    backend: "prometheus",
    interval: 60000
}

@audit {
    log_all_writes: true,
    log_sensitive_reads: true
}

@health {
    endpoints: ["/health", "/healthz"],
    checks: ["database", "redis", "disk_space"]
}
```

### Database & Transactions

```nexus
@repository UserRepository {
    def find_by_email(email) {
        return database.query("SELECT * FROM users WHERE email = ?", email)
    }
    
    def find_active() {
        return database.query("SELECT * FROM users WHERE active = true")
    }
}

@transaction {
    isolation: "READ_COMMITTED",
    timeout: 5000
    
    // Transaction logic
}

@migration {
    version: "20240124_001",
    up: {
        sql: "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(255))"
    },
    down: {
        sql: "DROP TABLE users"
    }
}

@seed {
    model: "users",
    data: [
        { name: "Alice", email: "alice@nexus.dev" },
        { name: "Bob", email: "bob@nexus.dev" }
    ]
}
```

### Deployment & Infrastructure

```nexus
@config {
    environment: "production"
}

@deploy {
    target: "docker",
    registry: "ghcr.io/myorg",
    auto_scaling: true
}

@region "us-east-1" {
    replicas: 3,
    auto_scale: { min: 1, max: 10 }
}

@region "eu-west-1" {
    replicas: 2,
    auto_scale: { min: 1, max: 5 }
}

@resource {
    cpu: "500m",
    memory: "512Mi"
}

@limit {
    max_connections: 1000,
    max_request_size: 10485760
}
```

### Testing & Quality

```nexus
@test "User Creation" {
    user = UserService.create_user("Alice", "alice@nexus.dev")
    assert user.id > 0
    assert user.name == "Alice"
}

@test "User Retrieval" {
    user = UserService.get_user(1)
    assert user != null
    assert user.email == "alice@nexus.dev"
}

@mock {
    database: { ... },
    smtp: { ... }
}

@benchmark {
    iterations: 1000,
    timeout: 60000
}
```

## Complete Example

```nexus
@config {
    port: 5000,
    database: "postgres://localhost/nexus_app",
    redis: "redis://localhost:6379"
}

@model User {
    id: number,
    name: string,
    email: string,
    created_at: date
}

@service UserService {
    def create_user(name, email) {
        user = { name: name, email: email, created_at: now() }
        return database.insert("users", user)
    }
}

@middleware auth {
    token = request.headers["authorization"]
    request.user = verify_token(token)
}

@route POST "/api/users" @validate @auth {
    user = UserService.create_user(
        request.body.name,
        request.body.email
    )
    return { status: 201, data: user }
}

@route GET "/api/users/:id" @cache(3600) {
    user = database.query("SELECT * FROM users WHERE id = ?", :id)
    return { status: 200, data: user }
}

@task SendWelcomeEmails {
    cron: "0 * * * *",
    retry: 3
    
    new_users = database.query("SELECT * FROM users WHERE welcomed = false")
    for user in new_users {
        send_email(user.email, "Welcome!")
        database.update("users", user.id, { welcomed: true })
    }
}

@health {
    database_ok = database.ping()
    return { status: database_ok ? "healthy" : "unhealthy" }
}
```

## Key Differences from Traditional Backends

| Feature | Nexus .nxsjs | Traditional |
|---------|--------------|-------------|
| Language | Pure Nexus | JavaScript, Python, Go, etc. |
| Decorators | @route, @model, @middleware | Framework-specific |
| Configuration | Built-in | External files |
| Type System | Nexus types | Language types |
| Async | Native support | Promises/async-await |
| Clustering | Built-in | Manual setup |

## Important Notes

- `.nxsjs` is **NOT JavaScript** - it's pure Nexus syntax
- `.nxsjs` is **NOT compiled to Python** - it stays as Nexus
- All decorators are **first-class language features**
- Files are bundled as-is to `dist/api.nxsjs`
- No conversions or transformations occur

## Building Backend Projects

```bash
# Create new project
nexus new my-app

# Build backend
nexus build

# Verify backend in dist/
cat dist/api.nxsjs  # Pure Nexus code
```

All `.nxsjs` files remain in pure Nexus format with complete backend functionality!
