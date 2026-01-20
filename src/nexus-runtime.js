/**
 * Nexus Browser Runtime
 * Parses and executes .nxs files directly in the browser
 * Supports state management, UI components, and reactivity
 */

console.log('✓ nexus-runtime.js loaded');

class NexusRuntime {
    constructor() {
        console.log('NexusRuntime constructor called');
        this.state = {};
        this.components = [];
        this.watchers = {};
        this.functions = {};
        this.context = {};
        this.ast = null;
        this.source = '';
        console.log('NexusRuntime initialized');
    }

    /**
     * Load and parse a .nxs file
     */
    async load(filePath) {
        console.log('NexusRuntime.load() called with:', filePath);
        try {
            console.log('Fetching file...');
            const response = await fetch(filePath);
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            this.source = await response.text();
            console.log('Loaded', this.source.length, 'bytes');
            console.log('Parsing...');
            this.ast = this.parse(this.source);
            console.log('Parsed successfully');
            return this.ast;
        } catch (error) {
            console.error(`Failed to load ${filePath}:`, error);
            throw error;
        }
    }

/**
 * Execute the loaded .nxs code
 */
    execute() {
        console.log('NexusRuntime.execute() called');
        if (!this.ast) {
            throw new Error('No code loaded. Call load() first.');
        }
        
        console.log('Setting up builtins...');
        this.setupBuiltins();
        console.log('Interpreting program...');
        this.interpretProgram(this.ast);
        console.log('Rendering UI...');
        this.renderUI();
        console.log('Execute complete');
    }

    /**
     * Parse Nexus code into an AST
     */
    parse(code) {
        const tokens = this.tokenize(code);
        return this.parseTokens(tokens);
    }

    /**
     * Tokenize Nexus code
     */
    tokenize(code) {
        const tokens = [];
        let i = 0;

        const whitespace = /\s/;
        const digit = /\d/;
        const letter = /[a-zA-Z_]/;
        const alphanumeric = /[a-zA-Z0-9_]/;

        while (i < code.length) {
            // Skip whitespace
            if (whitespace.test(code[i])) {
                i++;
                continue;
            }

            // Comments
            if (code[i] === '/' && code[i + 1] === '/') {
                while (i < code.length && code[i] !== '\n') i++;
                continue;
            }

            // Strings
            if (code[i] === '"' || code[i] === "'") {
                const quote = code[i];
                let str = '';
                i++;
                while (i < code.length && code[i] !== quote) {
                    if (code[i] === '\\') {
                        i++;
                        str += code[i];
                    } else {
                        str += code[i];
                    }
                    i++;
                }
                i++; // closing quote
                tokens.push({ type: 'STRING', value: str });
                continue;
            }

            // Numbers
            if (digit.test(code[i]) || (code[i] === '-' && digit.test(code[i + 1]))) {
                let num = '';
                if (code[i] === '-') num += '-', i++;
                while (i < code.length && (digit.test(code[i]) || code[i] === '.')) {
                    num += code[i];
                    i++;
                }
                tokens.push({ type: 'NUMBER', value: parseFloat(num) });
                continue;
            }

            // HTML/JSX tags - capture entire tag including content
            if (code[i] === '<' && (letter.test(code[i + 1]) || code[i + 1] === '/')) {
                let tagStart = i;
                let tagStr = '';
                
                // Find matching closing tag
                let depth = 0;
                let inTag = true;
                while (i < code.length) {
                    tagStr += code[i];
                    
                    if (code[i] === '<' && code[i + 1] !== '!') {
                        if (code[i + 1] === '/') depth--;
                        else if (!code.substring(i).match(/^<\w+[^>]*\/>/)) depth++;
                    }
                    if (code[i] === '>' && code[i - 1] !== '-') {
                        i++;
                        if (depth === 0) break;
                        continue;
                    }
                    i++;
                }
                
                tokens.push({ type: 'TAG', value: tagStr });
                continue;
            }

            // Operators and punctuation
            const twoCharOps = ['==', '!=', '<=', '>=', '&&', '||', '++', '--', '=>', '@'];
            const twoChar = code.substring(i, i + 2);
            if (twoCharOps.includes(twoChar)) {
                tokens.push({ type: 'OPERATOR', value: twoChar });
                i += 2;
                continue;
            }

            const singleCharOps = ['=', '+', '-', '*', '/', '%', '<', '>', '!', '&', '|', '(', ')', '{', '}', '[', ']', ',', '.', ':', ';'];
            if (singleCharOps.includes(code[i])) {
                tokens.push({ type: 'OPERATOR', value: code[i] });
                i++;
                continue;
            }

            // Identifiers and keywords
            if (letter.test(code[i])) {
                let ident = '';
                while (i < code.length && alphanumeric.test(code[i])) {
                    ident += code[i];
                    i++;
                }
                
                const keywords = ['var', 'let', 'const', 'func', 'if', 'else', 'for', 'while', 'context', 'reaction', 'pool', 'gate', 'return', 'true', 'false', 'null'];
                if (keywords.includes(ident)) {
                    tokens.push({ type: 'KEYWORD', value: ident });
                } else {
                    tokens.push({ type: 'IDENTIFIER', value: ident });
                }
                continue;
            }

            i++;
        }

        return tokens;
    }

    /**
     * Parse tokens into AST
     */
    parseTokens(tokens) {
        const statements = [];
        let i = 0;

        const peek = (offset = 0) => {
            const index = i + offset;
            return index < tokens.length ? tokens[index] : null;
        };
        const consume = () => tokens[i++];

        const parseStatement = () => {
            const token = peek();
            if (!token) return null;

            if (token.type === 'KEYWORD') {
                if (token.value === 'var' || token.value === 'let' || token.value === 'const') {
                    consume();
                    const nameToken = peek();
                    if (!nameToken) return null;
                    const name = consume().value;
                    const eqToken = peek();
                    if (eqToken && eqToken.value === '=') {
                        consume();
                        const value = parseExpression();
                        return { type: 'VARDECL', name, value };
                    }
                    return { type: 'VARDECL', name, value: { type: 'NULL', value: null } };
                }
                if (token.value === 'func') {
                    consume();
                    const nameToken = peek();
                    if (!nameToken) return null;
                    const name = consume().value;
                    const parenToken = peek();
                    if (parenToken && parenToken.value === '(') {
                        consume();
                        const params = [];
                        while (peek() && peek().value !== ')') {
                            const paramToken = peek();
                            if (paramToken && paramToken.type === 'IDENTIFIER') {
                                params.push(consume().value);
                            }
                            if (peek() && peek().value === ',') consume();
                        }
                        if (peek() && peek().value === ')') consume();
                        const braceToken = peek();
                        if (braceToken && braceToken.value === '{') {
                            consume();
                            const body = [];
                            while (peek() && peek().value !== '}') {
                                const stmt = parseStatement();
                                if (stmt) body.push(stmt);
                            }
                            if (peek() && peek().value === '}') consume();
                            return { type: 'FUNCDECL', name, params, body };
                        }
                    }
                }
                if (token.value === 'if') {
                    consume();
                    const condition = parseExpression();
                    const braceToken = peek();
                    if (braceToken && braceToken.value === '{') {
                        consume();
                        const thenBody = [];
                        while (peek() && peek().value !== '}') {
                            const stmt = parseStatement();
                            if (stmt) thenBody.push(stmt);
                        }
                        if (peek() && peek().value === '}') consume();
                        let elseBody = null;
                        if (peek() && peek().value === 'else') {
                            consume();
                            const elseBraceToken = peek();
                            if (elseBraceToken && elseBraceToken.value === '{') {
                                consume();
                                elseBody = [];
                                while (peek() && peek().value !== '}') {
                                    const stmt = parseStatement();
                                    if (stmt) elseBody.push(stmt);
                                }
                                if (peek() && peek().value === '}') consume();
                            }
                        }
                        return { type: 'IF', condition, thenBody, elseBody };
                    }
                }
                if (token.value === 'context') {
                    consume();
                    const nameToken = peek();
                    if (!nameToken) return null;
                    const name = consume().value;
                    const braceToken = peek();
                    if (braceToken && braceToken.value === '{') {
                        consume();
                        const body = [];
                        while (peek() && peek().value !== '}') {
                            const stmt = parseStatement();
                            if (stmt) body.push(stmt);
                        }
                        if (peek() && peek().value === '}') consume();
                        return { type: 'CONTEXT', name, body };
                    }
                }
            }

            if (token.type === 'TAG') {
                const tagValue = consume().value;
                return { type: 'JSX', tag: tagValue };
            }

            if (token.type === 'IDENTIFIER') {
                const name = consume().value;
                const nextToken = peek();
                if (nextToken && nextToken.value === '=') {
                    consume();
                    const value = parseExpression();
                    return { type: 'ASSIGN', name, value };
                }
                if (nextToken && nextToken.value === '(') {
                    consume();
                    const args = [];
                    while (peek() && peek().value !== ')') {
                        const arg = parseExpression();
                        if (arg) args.push(arg);
                        if (peek() && peek().value === ',') consume();
                    }
                    if (peek() && peek().value === ')') consume();
                    return { type: 'CALL', name, args };
                }
                return { type: 'IDENT', value: name };
            }

            return null;
        };

        const parseExpression = () => {
            const token = peek();
            if (!token) return null;
            
            if (token.type === 'STRING') {
                return { type: 'STRING', value: consume().value };
            }
            if (token.type === 'NUMBER') {
                return { type: 'NUMBER', value: consume().value };
            }
            if (token.type === 'IDENTIFIER') {
                return { type: 'IDENT', value: consume().value };
            }
            if (token.type === 'KEYWORD') {
                if (token.value === 'true') {
                    consume();
                    return { type: 'BOOL', value: true };
                }
                if (token.value === 'false') {
                    consume();
                    return { type: 'BOOL', value: false };
                }
                if (token.value === 'null') {
                    consume();
                    return { type: 'NULL', value: null };
                }
            }

            return null;
        };

        while (i < tokens.length) {
            try {
                const stmt = parseStatement();
                if (stmt) statements.push(stmt);
                else i++; // Skip to next token if parsing failed
            } catch (e) {
                console.error('Parse error at token', i, ':', tokens[i], e);
                i++;
            }
        }

        return { type: 'PROGRAM', body: statements };
    }

    /**
     * Setup built-in functions
     */
    setupBuiltins() {
        console.log('Setting up builtin functions');
        
        this.functions.println = (...args) => {
            console.log(...args);
        };

        this.functions.print = (...args) => {
            console.log(...args);
        };

        this.functions.alert = (msg) => {
            window.alert(msg);
        };

        this.functions.log = (...args) => {
            console.log(...args);
        };

        // Dynamic file loading
        this.functions.load = async (filePath) => {
            console.log('Loading file:', filePath);
            try {
                const runtime = new NexusRuntime();
                await runtime.load(filePath);
                runtime.execute();
                console.log('Loaded and executed:', filePath);
                return true;
            } catch (error) {
                console.error('Failed to load:', filePath, error);
                return false;
            }
        };

        // Import/require files
        this.functions.import = async (filePath) => {
            console.log('Importing:', filePath);
            return this.functions.load(filePath);
        };

        this.functions.require = async (filePath) => {
            console.log('Requiring:', filePath);
            return this.functions.load(filePath);
        };

        console.log('Builtins set up');
    }

    /**
     * Interpret the AST
     */
    interpretProgram(node, scope = {}) {
        if (node.type === 'PROGRAM') {
            for (const stmt of node.body) {
                this.interpretStatement(stmt, scope);
            }
            return;
        }

        this.interpretStatement(node, scope);
    }

    /**
     * Interpret a single statement
     */
    interpretStatement(node, scope = {}) {
        if (!node) return;

        switch (node.type) {
            case 'VARDECL': {
                const value = this.interpretExpression(node.value, scope);
                scope[node.name] = value;
                this.state[node.name] = value;
                break;
            }

            case 'ASSIGN': {
                const value = this.interpretExpression(node.value, scope);
                scope[node.name] = value;
                this.state[node.name] = value;
                this.notifyWatchers(node.name, value);
                break;
            }

            case 'CALL': {
                const func = this.functions[node.name] || scope[node.name];
                if (func && typeof func === 'function') {
                    const args = node.args.map(arg => this.interpretExpression(arg, scope));
                    return func(...args);
                }
                break;
            }

            case 'IF': {
                const condition = this.interpretExpression(node.condition, scope);
                if (condition) {
                    for (const stmt of node.thenBody) {
                        this.interpretStatement(stmt, scope);
                    }
                } else if (node.elseBody) {
                    for (const stmt of node.elseBody) {
                        this.interpretStatement(stmt, scope);
                    }
                }
                break;
            }

            case 'FUNCDECL': {
                scope[node.name] = (...args) => {
                    const funcScope = { ...scope };
                    for (let i = 0; i < node.params.length; i++) {
                        funcScope[node.params[i]] = args[i];
                    }
                    for (const stmt of node.body) {
                        this.interpretStatement(stmt, funcScope);
                    }
                };
                this.functions[node.name] = scope[node.name];
                break;
            }

            case 'CONTEXT': {
                this.context[node.name] = {};
                for (const stmt of node.body) {
                    this.interpretStatement(stmt, this.context[node.name]);
                }
                break;
            }

            case 'JSX': {
                this.components.push(node);
                break;
            }
        }
    }

    /**
     * Interpret an expression
     */
    interpretExpression(node, scope = {}) {
        if (!node) return null;

        switch (node.type) {
            case 'STRING':
                return node.value;
            case 'NUMBER':
                return node.value;
            case 'BOOL':
                return node.value;
            case 'NULL':
                return null;
            case 'IDENT':
                return scope[node.value] !== undefined ? scope[node.value] : this.state[node.value];
            default:
                return null;
        }
    }

    /**
     * Watch for state changes
     */
    watch(key, callback) {
        if (!this.watchers[key]) {
            this.watchers[key] = [];
        }
        this.watchers[key].push(callback);
    }

    /**
     * Notify watchers of state changes
     */
    notifyWatchers(key, value) {
        if (this.watchers[key]) {
            for (const callback of this.watchers[key]) {
                callback(value);
            }
        }
    }

    /**
     * Render UI with proper element creation
     */
    renderUI() {
        const app = document.getElementById('app');
        if (!app) return;

        // Clear previous content
        app.innerHTML = '';

        // Render all collected components
        for (const component of this.components) {
            if (component.type === 'JSX') {
                const element = this.createElementFromTag(component.tag);
                if (element) {
                    app.appendChild(element);
                }
            }
        }

        // Update state-bound elements
        this.updateBoundElements();
    }

    /**
     * Create DOM element from JSX/HTML tag string
     */
    createElementFromTag(tagString) {
        try {
            // Pre-process Nexus @ decorators
            let processed = tagString;
            
            // Convert @bind to data-bind
            processed = processed.replace(/@bind="([^"]*)"/g, 'data-bind="$1"');
            processed = processed.replace(/@bind='([^']*)'/g, "data-bind='$1'");
            
            // Convert @click to data-click
            processed = processed.replace(/@click="([^"]*)"/g, 'data-click="$1"');
            processed = processed.replace(/@click='([^']*)'/g, "data-click='$1'");
            
            // Convert @change to data-change
            processed = processed.replace(/@change="([^"]*)"/g, 'data-change="$1"');
            processed = processed.replace(/@change='([^']*)'/g, "data-change='$1'");
            
            // Convert @input to data-input
            processed = processed.replace(/@input="([^"]*)"/g, 'data-input="$1"');
            processed = processed.replace(/@input='([^']*)'/g, "data-input='$1'");
            
            // Create a temporary container
            const container = document.createElement('div');
            container.innerHTML = processed;
            
            // Extract the element
            let element = container.firstChild;
            
            if (!element) return null;

            // Handle custom Nexus component tags
            const tagName = element.tagName.toLowerCase();
            
            if (tagName === 'card') {
                const div = document.createElement('div');
                div.className = 'nxs-card';
                div.innerHTML = element.innerHTML;
                // Copy attributes
                Array.from(element.attributes).forEach(attr => {
                    if (attr.name.startsWith('data-')) {
                        div.setAttribute(attr.name, attr.value);
                    }
                });
                element = div;
            } 
            else if (tagName === 'view') {
                const div = document.createElement('div');
                div.className = 'nxs-view';
                div.innerHTML = element.innerHTML;
                Array.from(element.attributes).forEach(attr => {
                    if (attr.name.startsWith('data-')) {
                        div.setAttribute(attr.name, attr.value);
                    }
                });
                element = div;
            } 
            else if (tagName === 'text') {
                const span = document.createElement('span');
                span.className = 'nxs-text';
                span.textContent = element.textContent;
                Array.from(element.attributes).forEach(attr => {
                    if (attr.name.startsWith('data-')) {
                        span.setAttribute(attr.name, attr.value);
                    }
                });
                element = span;
            }
            else if (tagName === 'button' || tagName === 'btn') {
                if (!element.classList.contains('nxs-btn')) {
                    element.classList.add('nxs-btn');
                }
            }
            else if (tagName === 'input') {
                if (!element.classList.contains('nxs-input')) {
                    element.classList.add('nxs-input');
                }
            }

            return element;
        } catch (error) {
            console.error('Failed to create element from tag:', tagString, error);
            return null;
        }
    }

    /**
     * Update elements bound to state
     */
    updateBoundElements() {
        document.querySelectorAll('[data-bind]').forEach(el => {
            const key = el.getAttribute('data-bind');
            if (this.state[key] !== undefined) {
                if (el.type === 'text' || el.type === 'input') {
                    el.value = this.state[key];
                } else {
                    el.textContent = this.state[key];
                }
            }

            // Set up change listeners for two-way binding
            if (el.type === 'text' || el.type === 'input') {
                el.addEventListener('input', (e) => {
                    this.state[key] = e.target.value;
                    this.notifyWatchers(key, e.target.value);
                });
            }
        });

        // Handle @click / data-click handlers
        document.querySelectorAll('[data-click]').forEach(el => {
            const funcName = el.getAttribute('data-click');
            // Remove function call syntax if present (e.g., "handleClick()" -> "handleClick")
            const cleanFuncName = funcName.replace(/\(.*\)$/, '');
            if (this.functions[cleanFuncName]) {
                el.addEventListener('click', () => {
                    this.functions[cleanFuncName]();
                });
            }
        });

        // Handle @change handlers
        document.querySelectorAll('[data-change]').forEach(el => {
            const funcName = el.getAttribute('data-change').replace(/\(.*\)$/, '');
            if (this.functions[funcName]) {
                el.addEventListener('change', () => {
                    this.functions[funcName]();
                });
            }
        });

        // Handle @input handlers
        document.querySelectorAll('[data-input]').forEach(el => {
            const funcName = el.getAttribute('data-input').replace(/\(.*\)$/, '');
            if (this.functions[funcName]) {
                el.addEventListener('input', () => {
                    this.functions[funcName]();
                });
            }
        });
    }
}

// Export for use in HTML
window.NexusRuntime = NexusRuntime;
