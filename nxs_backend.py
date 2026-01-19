"""
Nexus Backend Language (.nxsjs)
Backend-only language with database, API, and file system support
Not JavaScript despite the name
"""

import json
import sqlite3
import re
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class NxsjsRoute:
    method: str
    path: str
    handler: str
    middleware: List[str]

class NxsjsParser:
    def __init__(self, source: str):
        self.source = source
        self.routes = []
        self.models = {}
        self.middleware = {}
        self.config = {}
    
    def parse(self) -> Dict[str, Any]:
        """Parse .nxsjs backend code"""
        self.parse_config()
        self.parse_models()
        self.parse_routes()
        self.parse_middleware()
        
        return {
            "routes": self.routes,
            "models": self.models,
            "middleware": self.middleware,
            "config": self.config
        }
    
    def parse_config(self):
        """Parse @config directives"""
        config_match = re.search(r'@config\s+{([^}]*)}', self.source, re.DOTALL)
        if config_match:
            config_str = config_match.group(1)
            # Parse simple key: value pairs
            for line in config_str.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip(',')
                    self.config[key] = value
    
    def parse_models(self):
        """Parse @model definitions"""
        model_pattern = r'@model\s+(\w+)\s*{([^}]*)}'
        for match in re.finditer(model_pattern, self.source, re.DOTALL):
            model_name = match.group(1)
            model_fields = match.group(2)
            
            fields = {}
            for line in model_fields.split('\n'):
                line = line.strip()
                if line and ':' in line:
                    field_name, field_type = line.split(':', 1)
                    fields[field_name.strip()] = field_type.strip().rstrip(',')
            
            self.models[model_name] = fields
    
    def parse_routes(self):
        """Parse @route definitions"""
        route_pattern = r'@route\s+(\w+)\s+"([^"]*)"\s*(?:@auth)?\s*{([^}]*)}'
        
        for match in re.finditer(route_pattern, self.source, re.DOTALL):
            method = match.group(1).upper()
            path = match.group(2)
            handler = match.group(3).strip()
            
            # Check for auth requirement
            is_auth = '@auth' in match.group(0)
            middleware_list = ['auth'] if is_auth else []
            
            self.routes.append({
                "method": method,
                "path": path,
                "handler": handler,
                "middleware": middleware_list,
                "auth": is_auth
            })
    
    def parse_middleware(self):
        """Parse @middleware definitions"""
        middleware_pattern = r'@middleware\s+(\w+)\s*{([^}]*)}'
        
        for match in re.finditer(middleware_pattern, self.source, re.DOTALL):
            name = match.group(1)
            code = match.group(2).strip()
            self.middleware[name] = code


class NxsjsCompiler:
    def __init__(self, filepath: str):
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.source = f.read()
    
    def compile(self) -> str:
        """Compile .nxsjs to Python Flask app"""
        parser = NxsjsParser(self.source)
        ast = parser.parse()
        
        return self.generate_flask_app(ast)
    
    def generate_flask_app(self, ast: Dict[str, Any]) -> str:
        """Generate Flask application code"""
        
        # Generate imports
        imports = """from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
"""
        
        # Generate database models
        models_code = self.generate_models(ast["models"])
        
        # Generate routes
        routes_code = self.generate_routes(ast["routes"])
        
        # Generate middleware
        middleware_code = self.generate_middleware(ast["middleware"])
        
        return f"""{imports}

app = Flask(__name__)
CORS(app)

# Configuration
{self.generate_config(ast["config"])}

# Database
def init_db():
    conn = sqlite3.connect('nexus.db')
    cursor = conn.cursor()
{models_code}
    conn.commit()
    conn.close()

# Middleware
{middleware_code}

# Routes
{routes_code}

if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', {ast['config'].get('port', '5000')}))
    app.run(debug=True, port=port)
"""
    
    def generate_config(self, config: Dict[str, str]) -> str:
        """Generate Flask config"""
        lines = []
        for key, value in config.items():
            if value.isdigit():
                lines.append(f"app.config['{key.upper()}'] = {value}")
            else:
                lines.append(f"app.config['{key.upper()}'] = '{value}'")
        return '\n'.join(lines) if lines else "pass"
    
    def generate_models(self, models: Dict[str, Dict]) -> str:
        """Generate database tables"""
        lines = []
        for model_name, fields in models.items():
            sql_fields = []
            for field_name, field_type in fields.items():
                sql_type = self.nxs_type_to_sql(field_type)
                sql_fields.append(f"        {field_name} {sql_type}")
            
            sql = f"""    cursor.execute('''
        CREATE TABLE IF NOT EXISTS {model_name.lower()} (
            id INTEGER PRIMARY KEY,
{',\\n'.join(sql_fields)}
        )
    ''')"""
            lines.append(sql)
        
        return '\n'.join(lines) if lines else "    pass"
    
    def nxs_type_to_sql(self, nxs_type: str) -> str:
        """Convert Nexus types to SQL"""
        type_map = {
            'string': 'TEXT',
            'number': 'INTEGER',
            'float': 'REAL',
            'bool': 'INTEGER',
            'datetime': 'TIMESTAMP',
            'json': 'TEXT'
        }
        return type_map.get(nxs_type.lower(), 'TEXT')
    
    def generate_routes(self, routes: List[Dict]) -> str:
        """Generate Flask routes"""
        lines = []
        for i, route in enumerate(routes):
            method = route["method"].lower()
            path = route["path"]
            func_name = f"route_{i}".replace('-', '_')
            
            decorator = f"@app.route('{path}', methods=['{route['method']}'])"
            
            lines.append(f"""{decorator}
def {func_name}():
    try:
        {route['handler']}
        return jsonify({{'success': True}})
    except Exception as e:
        return jsonify({{'error': str(e)}}), 500
""")
        
        return '\n'.join(lines) if lines else "pass"
    
    def generate_middleware(self, middleware: Dict[str, str]) -> str:
        """Generate middleware functions"""
        lines = []
        for name, code in middleware.items():
            lines.append(f"""def {name}():
    {code}
""")
        return '\n'.join(lines) if lines else "pass"


class NxsjsInterpreter:
    """Direct .nxsjs execution"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.source = f.read()
        self.db_conn = None
    
    def run(self):
        """Run .nxsjs directly"""
        print(f"Running {self.filepath}...")
        
        # Parse and execute
        parser = NxsjsParser(self.source)
        ast = parser.parse()
        
        # Initialize database
        self.init_database(ast)
        
        # Execute routes (in a real app, would start Flask)
        print(f"  Config: {ast['config']}")
        print(f"  Models: {list(ast['models'].keys())}")
        print(f"  Routes: {len(ast['routes'])} defined")
        print(f"  Middleware: {list(ast['middleware'].keys())}")
    
    def init_database(self, ast: Dict):
        """Initialize database"""
        self.db_conn = sqlite3.connect(':memory:')
        cursor = self.db_conn.cursor()
        
        for model_name, fields in ast['models'].items():
            # Create table
            pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python nxs_backend.py <input.nxsjs> [--compile|--run]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "--compile"
    
    if action == "--compile":
        output_file = input_file.replace('.nxsjs', '_app.py')
        compiler = NxsjsCompiler(input_file)
        python_code = compiler.compile()
        with open(output_file, 'w') as f:
            f.write(python_code)
        print(f"✓ Compiled {input_file} -> {output_file}")
    
    elif action == "--run":
        interpreter = NxsjsInterpreter(input_file)
        interpreter.run()
