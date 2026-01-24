# Nexus Multi-File Project Support

## ✅ Multiple .nxs and .nxsjs Files Fully Supported

Projects can contain **unlimited** `.nxs` (frontend) and `.nxsjs` (backend) files, and the build system will automatically discover and bundle them all.

---

## Project Structure Example

```
myapp/
├── src/
│   ├── index.nxs              ← Main frontend entry
│   ├── components/
│   │   ├── navbar.nxs         ← Reusable component
│   │   ├── sidebar.nxs        ← Reusable component
│   │   ├── footer.nxs         ← Reusable component
│   │   └── modal.nxs          ← Reusable component
│   ├── api/
│   │   ├── users.nxsjs        ← User endpoints
│   │   ├── posts.nxsjs        ← Post endpoints
│   │   ├── auth.nxsjs         ← Auth endpoints
│   │   └── comments.nxsjs     ← Comment endpoints
│   └── api.nxsjs              ← Main backend entry
├── dist/                       ← Auto-generated on build
│   ├── index.nxs              ← Bundled main
│   ├── components/
│   │   ├── navbar.nxs
│   │   ├── sidebar.nxs
│   │   ├── footer.nxs
│   │   └── modal.nxs
│   ├── api/
│   │   ├── users.nxsjs
│   │   ├── posts.nxsjs
│   │   ├── auth.nxsjs
│   │   └── comments.nxsjs
│   ├── app.py                 ← Compiled main backend
│   ├── index.html             ← HTML loader
│   └── nexus-runtime.js       ← Runtime environment
├── nxs.json
├── README.md
└── ...
```

---

## Build System Behavior

### Frontend (.nxs) Files
```
src/index.nxs                    → dist/index.nxs
src/components/navbar.nxs        → dist/components/navbar.nxs
src/components/sidebar.nxs       → dist/components/sidebar.nxs
src/components/footer.nxs        → dist/components/footer.nxs
```

**Key Features:**
- ✅ All `.nxs` files discovered recursively
- ✅ Directory structure preserved
- ✅ Format stays as Nexus (NOT converted to HTML)
- ✅ Custom tags preserved: `<view>`, `<card>`, `<btn>`, etc.

### Backend (.nxsjs) Files
```
src/api.nxsjs                    → dist/app.py (main compiled backend)
src/api/users.nxsjs             → dist/api/users.nxsjs
src/api/posts.nxsjs             → dist/api/posts.nxsjs
src/api/auth.nxsjs              → dist/api/auth.nxsjs
```

**Key Features:**
- ✅ Main entry point (`src/api.nxsjs`) compiled to `dist/app.py`
- ✅ Additional `.nxsjs` files bundled as-is to `dist/api/`
- ✅ Allows modular backend structure
- ✅ Each file can define its own routes, models, middleware

---

## Build Command

```bash
nexus build
```

Output:
```
🏗️  Building project...
  📦 Bundling frontend...
    ✓ Bundled src/index.nxs → dist/index.nxs
    ✓ Bundled src/components/navbar.nxs → dist/components/navbar.nxs
    ✓ Bundled src/components/sidebar.nxs → dist/components/sidebar.nxs
    ✓ Bundled src/components/footer.nxs → dist/components/footer.nxs
  🔧 Compiling backend...
    ✓ Compiled src/api.nxsjs → dist/app.py
    ✓ Compiled src/api/users.nxsjs → dist/api/users.nxsjs
    ✓ Compiled src/api/posts.nxsjs → dist/api/posts.nxsjs
    ✓ Compiled src/api/auth.nxsjs → dist/api/auth.nxsjs
  📋 Copying Nexus runtime...
    ✓ Copied nexus-runtime.js
  📋 Generating HTML loader...
    ✓ Generated dist/index.html
✅ Build complete!
```

---

## Format Preservation

**Important:** All `.nxs` files maintain Nexus format - **NO HTML conversion**

### Example: navbar.nxs
```xml
<!-- src/components/navbar.nxs -->
<card class="navbar">
    <h2>Navigation</h2>
    <btn @click="goHome()">Home</btn>
    <btn @click="goAbout()">About</btn>
</card>
```

After build, `dist/components/navbar.nxs` contains **identical** content:
```xml
<!-- dist/components/navbar.nxs -->
<card class="navbar">
    <h2>Navigation</h2>
    <btn @click="goHome()">Home</btn>
    <btn @click="goAbout()">About</btn>
</card>
```

✅ Format unchanged - NO `<div>`, `<button>`, or HTML tag mapping

---

## Use Cases

### Component-Based Architecture
```
src/components/
├── Header.nxs
├── Footer.nxs
├── Sidebar.nxs
├── Card.nxs
├── Button.nxs
└── Modal.nxs
```

### Modular Backend
```
src/api/
├── auth.nxsjs         (Authentication routes)
├── users.nxsjs        (User CRUD operations)
├── posts.nxsjs        (Post management)
├── comments.nxsjs     (Comment system)
└── notifications.nxsjs (Notifications)
```

### Shared Utilities
```
src/
├── utils.nxs          (Helper functions)
├── types.nxs          (Type definitions)
├── constants.nxs      (Constants)
└── ...
```

---

## Testing Results

### Multi-File Test Summary
✅ **Source files:** 4 `.nxs` + 4 `.nxsjs` = 8 total  
✅ **Bundled files:** 4 `.nxs` + 3 `.nxsjs` (main compiled) = 7 total  
✅ **Format preserved:** All files maintain Nexus format  
✅ **Directory structure:** Preserved during bundling  

---

## Build Configuration (nxs.json)

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "entry": {
    "frontend": "src/index.nxs",
    "backend": "src/api.nxsjs"
  },
  "output": {
    "frontend": "dist/index.nxs",
    "backend": "dist/app.py"
  },
  "dependencies": {},
  "devDependencies": {}
}
```

The build system automatically discovers ALL `.nxs` and `.nxsjs` files - no manual configuration needed!

---

## How It Works

1. **Discovery Phase**
   - Recursively scan `src/` for `*.nxs` files
   - Recursively scan `src/` for `*.nxsjs` files

2. **Frontend Bundling**
   - Copy all `.nxs` files to `dist/`
   - Preserve directory structure
   - Keep Nexus format (no conversion)

3. **Backend Compilation**
   - Compile main entry (`src/api.nxsjs`) to Python
   - Compile additional `.nxsjs` files to `dist/api/`
   - Maintain modularity

4. **Assets**
   - Copy runtime files
   - Generate HTML loader
   - Copy static assets

---

## ✨ Features

| Feature | Status | Details |
|---------|--------|---------|
| Multiple `.nxs` files | ✅ | Unlimited frontend files |
| Multiple `.nxsjs` files | ✅ | Unlimited backend files |
| Component reuse | ✅ | `src/components/` structure |
| Modular backend | ✅ | Separate API route files |
| Format preservation | ✅ | No HTML conversion |
| Directory structure | ✅ | Maintained in dist/ |
| Auto-discovery | ✅ | No config needed |
| Recursive bundling | ✅ | Nested directories work |

---

## Status

**FULLY OPERATIONAL** ✨

Multiple file projects are completely supported with:
- ✅ Automatic file discovery
- ✅ Recursive bundling  
- ✅ Format preservation
- ✅ Directory structure maintenance
- ✅ No manual configuration required
