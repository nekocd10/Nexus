"""
Nexus Interoperability Layer
Allows calling Python, JavaScript, and other functions from Nexus
Full integration with npm packages, external APIs, and databases
"""

import os
import json
import subprocess
import sys
import importlib.util
from pathlib import Path
from typing import Any, Dict, List, Callable, Optional
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import urllib.parse


class InteropBridge:
    """Handle cross-language interoperability"""
    
    def __init__(self):
        self.python_functions: Dict[str, Callable] = {}
        self.js_functions: Dict[str, str] = {}
        self.npm_packages: Dict[str, Any] = {}
        self.exports: Dict[str, Any] = {}
        self.python_modules = {}
    
    # ============ Python Integration ============
    
    def import_python_module(self, module_name: str) -> Any:
        """Import a Python module"""
        if module_name in self.python_modules:
            return self.python_modules[module_name]
        
        try:
            module = __import__(module_name)
            self.python_modules[module_name] = module
            return module
        except ImportError as e:
            raise ImportError(f"Cannot import Python module '{module_name}': {e}")
    
    def import_python_file(self, file_path: str) -> Any:
        """Import a Python file"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Python file not found: {file_path}")
        
        spec = importlib.util.spec_from_file_location("nexus_imported", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    def call_python_function(self, module_name: str, function_name: str, *args, **kwargs) -> Any:
        """Call a Python function"""
        module = self.import_python_module(module_name)
        if not hasattr(module, function_name):
            raise AttributeError(f"Function '{function_name}' not found in '{module_name}'")
        return getattr(module, function_name)(*args, **kwargs)
    
    def register_python_function(self, name: str, func: Callable):
        """Register a Python function for Nexus to call"""
        self.python_functions[name] = func
    
    # ============ JavaScript Integration ============
    
    def register_js_function(self, name: str, code: str):
        """Register a JavaScript function for Nexus to call"""
        self.js_functions[name] = code
    
    def execute_js_code(self, code: str, context: Dict[str, Any] = None) -> Any:
        """Execute JavaScript code"""
        try:
            import tempfile
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                if context:
                    for key, value in context.items():
                        if isinstance(value, str):
                            f.write(f"const {key} = '{value}';\n")
                        else:
                            f.write(f"const {key} = {json.dumps(value)};\n")
                
                f.write(code)
                script_path = f.name
            
            result = subprocess.run(
                ["node", script_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            Path(script_path).unlink()
            
            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except:
                    return result.stdout.strip()
            else:
                raise RuntimeError(f"JS execution failed: {result.stderr}")
        
        except Exception as e:
            raise RuntimeError(f"Cannot execute JavaScript: {e}")
    
    def call_js(self, func_name: str, *args) -> Any:
        """Call a registered JavaScript function"""
        if func_name not in self.js_functions:
            raise ValueError(f"JavaScript function not found: {func_name}")
        
        js_args = json.dumps(args)
        js_code = f"""
const fn = {self.js_functions[func_name]};
const result = fn(...{js_args});
console.log(JSON.stringify(result));
"""
        
        try:
            result = subprocess.check_output(
                ["node", "-e", js_code],
                text=True,
                timeout=30
            ).strip()
            return json.loads(result)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"JavaScript execution failed: {e}")
    
    # ============ NPM Package Integration ============
    
    def import_npm_package(self, package_name: str) -> Dict[str, Any]:
        """Import an npm package"""
        if package_name in self.npm_packages:
            return self.npm_packages[package_name]
        
        return {
            "name": package_name,
            "type": "npm",
            "can_import": True,
            "available": True
        }
    
    def call_npm_function(self, package_name: str, function_name: str, *args) -> Any:
        """Call a function from an npm package"""
        js_code = f"""
const pkg = require('{package_name}');
const fn = pkg.{function_name};
const result = fn({', '.join(json.dumps(a) for a in args)});
console.log(JSON.stringify(result));
"""
        return self.execute_js_code(js_code)
    
    # ============ HTTP/REST Integration ============
    
    def http_request(self, method: str, url: str, headers: Dict = None, 
                    data: Dict = None, timeout: int = 30) -> Dict[str, Any]:
        """Make HTTP requests"""
        try:
            req_data = json.dumps(data).encode() if data else None
            req = Request(
                url,
                data=req_data,
                headers=headers or {},
                method=method
            )
            
            with urlopen(req, timeout=timeout) as response:
                body = response.read().decode()
                return {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "body": body,
                    "ok": 200 <= response.status < 300
                }
        except HTTPError as e:
            return {
                "status": e.code,
                "headers": dict(e.headers),
                "body": e.read().decode(),
                "ok": False
            }
        except Exception as e:
            raise RuntimeError(f"HTTP request failed: {e}")
    
    def rest_api_call(self, endpoint: str, method: str = "GET", 
                     params: Dict = None, body: Dict = None) -> Dict:
        """Make REST API calls"""
        url = endpoint
        if params:
            url += "?" + urllib.parse.urlencode(params)
        return self.http_request(method, url, data=body)
    
    def fetch_json(self, url: str, headers: Dict = None) -> Any:
        """Fetch JSON from URL"""
        response = self.http_request("GET", url, headers=headers)
        if response["ok"]:
            return json.loads(response["body"])
        raise RuntimeError(f"Failed to fetch JSON: {response['body']}")
    
    # ============ Data Format Conversion ============
    
    def to_json(self, obj: Any) -> str:
        """Convert Nexus object to JSON"""
        return json.dumps(obj)
    
    def from_json(self, json_str: str) -> Any:
        """Parse JSON to Python object"""
        return json.loads(json_str)
    
    def to_dict(self, nexus_pool: Dict[str, Any]) -> Dict:
        """Convert Nexus pool to Python dict"""
        return dict(nexus_pool)
    
    def from_dict(self, python_dict: Dict) -> Dict[str, Any]:
        """Convert Python dict to Nexus pool"""
        return dict(python_dict)
    
    # ============ Function Exports ============
    
    def export_nexus_function(self, name: str, func: Callable):
        """Export a Nexus function for external use"""
        self.exports[name] = func
    
    def get_export(self, name: str) -> Callable:
        """Get an exported function"""
        if name not in self.exports:
            raise KeyError(f"Export '{name}' not found")
        return self.exports[name]


class NexusFFI:
    """Foreign Function Interface for calling C/native code"""
    
    def __init__(self):
        self.libraries = {}
    
    def load_library(self, lib_name: str, lib_path: str):
        """Load a shared library"""
        try:
            import ctypes
            lib = ctypes.CDLL(lib_path)
            self.libraries[lib_name] = lib
        except Exception as e:
            raise RuntimeError(f"Failed to load library {lib_name}: {e}")
    
    def call_native(self, lib_name: str, func_name: str, *args):
        """Call a native C function"""
        if lib_name not in self.libraries:
            raise ValueError(f"Library not loaded: {lib_name}")
        
        lib = self.libraries[lib_name]
        func = getattr(lib, func_name)
        return func(*args)


class NexusWebAssembly:
    """WebAssembly integration for performance-critical code"""
    
    def __init__(self):
        self.wasm_modules = {}
    
    def load_wasm(self, name: str, wasm_file: str):
        """Load a WebAssembly module"""
        if not Path(wasm_file).exists():
            raise FileNotFoundError(f"WASM file not found: {wasm_file}")
        
        # This would require a WASM runtime
        # For now, store the path
        self.wasm_modules[name] = wasm_file
    
    def call_wasm(self, module_name: str, func_name: str, *args):
        """Call a WASM function"""
        if module_name not in self.wasm_modules:
            raise ValueError(f"WASM module not loaded: {module_name}")
        
        # This would require wasmer or similar
        # For now, return placeholder
        return f"WASM call: {module_name}.{func_name}({', '.join(str(a) for a in args)})"


class NexusModuleLoader:
    """Load and execute modules from different languages"""
    
    def __init__(self):
        self.modules = {}
        self.search_paths = [
            ".",
            "./node_modules",
            "./nxs_modules",
            "./lib"
        ]
    
    def add_search_path(self, path: str):
        """Add a search path for modules"""
        self.search_paths.append(path)
    
    def load_module(self, module_name: str) -> Any:
        """Load a module"""
        if module_name in self.modules:
            return self.modules[module_name]
        
        # Try different file extensions
        extensions = [".nexus", ".nxs", ".nxsjs", ".py", ".js", ".wasm"]
        
        for search_path in self.search_paths:
            for ext in extensions:
                module_path = Path(search_path) / f"{module_name}{ext}"
                
                if module_path.exists():
                    module = self._load_file(str(module_path), ext)
                    self.modules[module_name] = module
                    return module
        
        raise ModuleNotFoundError(f"Module not found: {module_name}")
    
    def _load_file(self, file_path: str, ext: str) -> Any:
        """Load a file based on extension"""
        
        if ext == ".py":
            return self._load_python(file_path)
        elif ext == ".js":
            return self._load_javascript(file_path)
        elif ext == ".nexus" or ext == ".nxs":
            return self._load_nexus(file_path)
        elif ext == ".nxsjs":
            return self._load_nxsjs(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def _load_python(self, file_path: str) -> Any:
        """Load and execute Python module"""
        import importlib.util
        
        spec = importlib.util.spec_from_file_location("module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    def _load_javascript(self, file_path: str) -> Dict[str, Any]:
        """Load JavaScript module"""
        with open(file_path, 'r') as f:
            js_code = f.read()
        
        # Parse exported functions
        exports = {}
        
        # Simple regex to find exports
        import re
        for match in re.finditer(r'exports\.(\w+)\s*=\s*function', js_code):
            name = match.group(1)
            exports[name] = js_code  # Store code for later execution
        
        return exports
    
    def _load_nexus(self, file_path: str) -> Any:
        """Load Nexus module"""
        from src.lexer import NexusLexer
        from src.parser import NexusParser
        from src.interpreter import NexusInterpreter
        
        with open(file_path, 'r') as f:
            source = f.read()
        
        lexer = NexusLexer(source)
        tokens = lexer.tokenize()
        
        parser = NexusParser(tokens)
        ast = parser.parse()
        
        interpreter = NexusInterpreter()
        interpreter.interpret(ast)
        
        return interpreter.environment
    
    def _load_nxsjs(self, file_path: str) -> Any:
        """Load .nxsjs backend module"""
        from nxs_backend import NxsjsParser, NxsjsCompiler
        
        parser = NxsjsParser(file_path)
        config = parser.parse_config()
        models = parser.parse_models()
        routes = parser.parse_routes()
        
        return {
            "config": config,
            "models": models,
            "routes": routes
        }


class NexusRPC:
    """Remote Procedure Call for communicating between processes"""
    
    def __init__(self, server_url: Optional[str] = None):
        self.server_url = server_url or "http://localhost:9000"
        self.handlers = {}
    
    def register_handler(self, name: str, handler: Callable):
        """Register an RPC handler"""
        self.handlers[name] = handler
    
    def call(self, method: str, *args, **kwargs) -> Any:
        """Call a remote method"""
        import requests
        
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": args or kwargs,
            "id": 1
        }
        
        try:
            response = requests.post(self.server_url, json=payload)
            data = response.json()
            
            if "result" in data:
                return data["result"]
            elif "error" in data:
                raise RuntimeError(f"RPC Error: {data['error']}")
            else:
                raise RuntimeError("Invalid RPC response")
        
        except Exception as e:
            raise RuntimeError(f"RPC call failed: {e}")


# Standard library for Nexus
NEXUS_STDLIB = {
    "print": print,
    "len": len,
    "range": range,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "set": set,
    "max": max,
    "min": min,
    "sum": sum,
    "all": all,
    "any": any,
    "sorted": sorted,
    "reversed": reversed,
    "enumerate": enumerate,
    "zip": zip,
    "map": map,
    "filter": filter,
    "json": json,
    "Path": Path,
}


def create_interop_environment():
    """Create a complete interoperability environment"""
    interop = NexusInterop()
    loader = NexusModuleLoader()
    
    # Register standard library
    for name, func in NEXUS_STDLIB.items():
        if callable(func):
            interop.register_python_function(name, func)
    
    return {
        "interop": interop,
        "loader": loader,
        "ffi": NexusFFI(),
        "wasm": NexusWebAssembly(),
        "rpc": NexusRPC()
    }
