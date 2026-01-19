"""
Nexus Bundler
Custom webpack-like bundler for Nexus projects
Handles code bundling, minification, and optimization
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Any
import hashlib


class NexusBundler:
    """Main bundler class"""
    
    def __init__(self, entry_point: str, output_path: str = "dist/bundle.js"):
        self.entry_point = entry_point
        self.output_path = output_path
        self.modules = {}
        self.dependencies = {}
        self.bundle_cache = {}
    
    def bundle(self) -> str:
        """Create a bundle from entry point"""
        print(f"📦 Bundling {self.entry_point}...")
        
        # Build dependency graph
        self.build_dependency_graph(self.entry_point)
        
        # Generate bundle
        bundle_code = self.generate_bundle()
        
        # Write bundle
        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, 'w') as f:
            f.write(bundle_code)
        
        print(f"✓ Bundle created: {self.output_path}")
        return bundle_code
    
    def build_dependency_graph(self, file_path: str, visited: Set[str] = None):
        """Build a dependency graph of all imports"""
        if visited is None:
            visited = set()
        
        if file_path in visited:
            return
        visited.add(file_path)
        
        if not Path(file_path).exists():
            print(f"  ⚠️  File not found: {file_path}")
            return
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse imports
        imports = self.extract_imports(content)
        
        self.modules[file_path] = {
            "content": content,
            "imports": imports
        }
        
        # Recursively process dependencies
        for imp in imports:
            dep_path = self.resolve_import(imp, file_path)
            if dep_path:
                self.build_dependency_graph(dep_path, visited)
    
    def extract_imports(self, content: str) -> List[str]:
        """Extract import statements"""
        imports = []
        
        # Nexus import syntax
        for match in re.finditer(r'@import\s+["\']([^"\']+)["\']', content):
            imports.append(match.group(1))
        
        # JavaScript import syntax
        for match in re.finditer(r'import\s+.*?\s+from\s+["\']([^"\']+)["\']', content):
            imports.append(match.group(1))
        
        # Require syntax
        for match in re.finditer(r'require\(["\']([^"\']+)["\']\)', content):
            imports.append(match.group(1))
        
        return imports
    
    def resolve_import(self, imp: str, current_file: str) -> str:
        """Resolve import path"""
        current_dir = Path(current_file).parent
        
        # Check if it's a relative import
        if imp.startswith('.'):
            resolved = (current_dir / imp).resolve()
            
            # Try different extensions
            for ext in ['.nxs', '.js', '.py', '.nxsjs', '']:
                test_path = Path(str(resolved) + ext)
                if test_path.exists():
                    return str(test_path)
            
            return None
        
        # Check node_modules
        node_modules_path = Path.cwd() / "node_modules" / imp
        if node_modules_path.exists():
            return str(node_modules_path)
        
        # Check nxs_modules
        nxs_modules_path = Path.cwd() / "nxs_modules" / imp
        if nxs_modules_path.exists():
            return str(nxs_modules_path)
        
        # Built-in modules
        return None
    
    def generate_bundle(self) -> str:
        """Generate the final bundle"""
        modules_code = "const __modules = {};\n"
        
        module_map = {}
        for i, (file_path, module_info) in enumerate(self.modules.items()):
            module_map[file_path] = i
            
            # Escape module content
            content = module_info['content'].replace('\\', '\\\\').replace('`', '\\`')
            modules_code += f'__modules[{i}] = `{content}`;\n'
        
        # Create module loader
        loader_code = """
const __loaded = {};
const __require = (id) => {
    if (__loaded[id]) return __loaded[id];
    const module = { exports: {} };
    const code = __modules[id];
    if (code) {
        const fn = new Function('module', 'exports', '__require', code);
        fn(module, module.exports, __require);
    }
    __loaded[id] = module.exports;
    return module.exports;
};
"""
        
        # Entry point
        entry_id = module_map.get(self.entry_point, 0)
        entry_code = f"\n__require({entry_id});\n"
        
        return modules_code + loader_code + entry_code
    
    def minify(self, code: str) -> str:
        """Minify code"""
        # Remove comments
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        
        # Remove whitespace
        code = re.sub(r'\s+', ' ', code)
        code = re.sub(r'\s*([{}();,])\s*', r'\1', code)
        
        return code.strip()


class NexusCodeSplitter:
    """Code splitting for better performance"""
    
    def __init__(self, bundler: NexusBundler):
        self.bundler = bundler
        self.chunks = {}
    
    def create_chunks(self, chunk_config: Dict[str, List[str]]) -> Dict[str, str]:
        """Create code chunks based on configuration"""
        chunks = {}
        
        for chunk_name, files in chunk_config.items():
            chunk_modules = {}
            
            for file_path in files:
                if file_path in self.bundler.modules:
                    chunk_modules[file_path] = self.bundler.modules[file_path]
            
            if chunk_modules:
                chunks[chunk_name] = self._generate_chunk(chunk_modules)
        
        return chunks
    
    def _generate_chunk(self, modules: Dict) -> str:
        """Generate a chunk from modules"""
        chunk_code = "// Chunk\n"
        
        for file_path, module_info in modules.items():
            chunk_code += f"\n// {file_path}\n"
            chunk_code += module_info['content'] + "\n"
        
        return chunk_code


class NexusAssetOptimizer:
    """Optimize assets like images and CSS"""
    
    @staticmethod
    def optimize_css(css_content: str) -> str:
        """Optimize CSS"""
        # Remove comments
        css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
        
        # Remove whitespace
        css_content = re.sub(r'\s+', ' ', css_content)
        css_content = re.sub(r'\s*([{}:;,])\s*', r'\1', css_content)
        
        return css_content.strip()
    
    @staticmethod
    def optimize_html(html_content: str) -> str:
        """Optimize HTML"""
        # Remove comments
        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
        
        # Remove extra whitespace but preserve important spacing
        html_content = re.sub(r'>\s+<', '><', html_content)
        
        return html_content.strip()


class NexusSourceMap:
    """Generate source maps for debugging"""
    
    def __init__(self, bundle_path: str):
        self.bundle_path = bundle_path
        self.mappings = []
    
    def add_mapping(self, bundle_line: int, bundle_col: int, source_file: str, 
                   source_line: int, source_col: int):
        """Add a source map entry"""
        self.mappings.append({
            "bundle": (bundle_line, bundle_col),
            "source": (source_file, source_line, source_col)
        })
    
    def generate(self) -> Dict[str, Any]:
        """Generate source map JSON"""
        return {
            "version": 3,
            "file": self.bundle_path,
            "mappings": self.mappings,
            "sourceRoot": ""
        }
    
    def save(self, output_path: str):
        """Save source map to file"""
        with open(output_path, 'w') as f:
            json.dump(self.generate(), f, indent=2)


class NexusManifest:
    """Generate a manifest for asset versioning"""
    
    def __init__(self):
        self.files = {}
    
    def add_file(self, file_path: str):
        """Add a file to manifest"""
        if Path(file_path).exists():
            with open(file_path, 'rb') as f:
                content_hash = hashlib.md5(f.read()).hexdigest()[:8]
            
            self.files[file_path] = content_hash
    
    def generate(self) -> Dict[str, str]:
        """Generate manifest"""
        return self.files
    
    def save(self, output_path: str):
        """Save manifest to file"""
        with open(output_path, 'w') as f:
            json.dump(self.generate(), f, indent=2)


def bundle_project(config_path: str = "nxs.json"):
    """Bundle an entire project"""
    if not Path(config_path).exists():
        print(f"❌ {config_path} not found")
        return
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Bundle frontend if exists
    frontend_entry = config.get("entry", {}).get("frontend")
    if frontend_entry and Path(frontend_entry).exists():
        print("📦 Bundling frontend...")
        bundler = NexusBundler(frontend_entry, "dist/bundle.js")
        bundler.bundle()
    
    # Bundle backend if exists
    backend_entry = config.get("entry", {}).get("backend")
    if backend_entry and Path(backend_entry).exists():
        print("📦 Bundling backend...")
        bundler = NexusBundler(backend_entry, "dist/app.js")
        bundler.bundle()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Nexus Bundler")
        print()
        print("Usage: python nxs_bundler.py <entry> [output]")
        sys.exit(1)
    
    entry = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "dist/bundle.js"
    
    bundler = NexusBundler(entry, output)
    bundler.bundle()
