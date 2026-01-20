"""
Nexus Frontend Language (.nxs)
Compiles to JavaScript/HTML for browser
Supports HTML syntax + EJS + custom GUI components
"""

import re
import os
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class NxsComponent:
    name: str
    props: Dict[str, str]
    children: List[Any]
    content: str = ""


class NxsParser:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.tokens = []
        self.scripts = []
        self.styles = []
    
    def parse(self) -> str:
        """Parse .nxs frontend code and return HTML/JS"""
        # Extract scripts and styles first
        self.extract_blocks()
        
        # Replace custom syntax with standard
        html = self.compile_custom_tags(self.source)
        html = self.compile_ejs_syntax(html)
        html = self.compile_html_syntax(html)
        
        # Wrap with boilerplate
        return self.generate_html(html)
    
    def extract_blocks(self):
        """Extract <script> and <style> blocks"""
        # Extract scripts
        script_matches = re.findall(r'<script\s*([^>]*)>(.*?)</script>', self.source, re.DOTALL | re.IGNORECASE)
        for attrs, content in script_matches:
            self.scripts.append((attrs, content.strip()))
        
        # Extract styles
        style_matches = re.findall(r'<style\s*([^>]*)>(.*?)</style>', self.source, re.DOTALL | re.IGNORECASE)
        for attrs, content in style_matches:
            self.styles.append((attrs, content.strip()))
        
        # Remove them from source for processing
        self.source = re.sub(r'<script\s*[^>]*>.*?</script>', '', self.source, flags=re.DOTALL | re.IGNORECASE)
        self.source = re.sub(r'<style\s*[^>]*>.*?</style>', '', self.source, flags=re.DOTALL | re.IGNORECASE)
    
    def compile_ejs_syntax(self, source: str) -> str:
        """Support EJS template syntax like <%= %>, <% %>, <%- %>"""
        # <%= expression %> - escaped output
        source = re.sub(
            r'<%=\s*([^%]*?)\s*%>',
            lambda m: f'{{{{ {m.group(1)} }}}}',
            source
        )
        
        # <%- expression %> - unescaped output
        source = re.sub(
            r'<%-\s*([^%]*?)\s*%>',
            lambda m: f'{{{{ {m.group(1)} | safe }}}}',
            source
        )
        
        # <% code %> - execute code (for loops, conditions, etc)
        source = re.sub(
            r'<%\s*([^%]*?)\s*%>',
            lambda m: f'<!-- {m.group(1)} -->',
            source
        )
        
        return source
    
    def compile_html_syntax(self, source: str) -> str:
        """Support standard HTML syntax"""
        # HTML is kept as-is, just pass through
        return source
    
    def compile_custom_tags(self, source: str) -> str:
        """Convert custom tags to HTML"""
        result = source
        
        # Custom GUI components
        result = self.replace_button(result)
        result = self.replace_input(result)
        result = self.replace_view(result)
        result = self.replace_card(result)
        result = self.replace_state(result)
        result = self.replace_bind(result)
        result = self.replace_event(result)
        
        return result
    
    def replace_button(self, source: str) -> str:
        """<button>text</button> or <btn>text</btn>"""
        # Replace <btn> tags
        source = re.sub(
            r'<btn\s+([^>]*)>([^<]*)</btn>',
            lambda m: f'<button class="nxs-btn" {m.group(1)}>{m.group(2)}</button>',
            source,
            flags=re.IGNORECASE | re.DOTALL
        )
        # Add button styles to <btn>
        source = re.sub(
            r'<button\s+([^>]*)>([^<]*)</button>',
            lambda m: f'<button class="nxs-btn" {m.group(1)}>{m.group(2)}</button>',
            source
        )
        return source
    
    def replace_input(self, source: str) -> str:
        """<input> custom syntax"""
        source = re.sub(
            r'<input\s+([^>]*)/>',
            lambda m: f'<input class="nxs-input" {m.group(1)} />',
            source,
            flags=re.IGNORECASE
        )
        return source
    
    def replace_view(self, source: str) -> str:
        """<view> is like <div> with flexbox"""
        source = re.sub(
            r'<view\s+([^>]*)>',
            lambda m: f'<div class="nxs-view" {m.group(1)}>',
            source,
            flags=re.IGNORECASE
        )
        source = source.replace('</view>', '</div>')
        return source
    
    def replace_card(self, source: str) -> str:
        """<card> is a styled container"""
        source = re.sub(
            r'<card\s+([^>]*)>',
            lambda m: f'<div class="nxs-card" {m.group(1)}>',
            source,
            flags=re.IGNORECASE
        )
        source = source.replace('</card>', '</div>')
        return source
    
    def replace_state(self, source: str) -> str:
        """@state name="value" becomes state variable"""
        # Extract state declarations
        states = re.findall(r'@state\s+(\w+)="([^"]*)"', source)
        state_vars = '\n    '.join([f"let {name} = '{value}';" for name, value in states])
        
        # Remove state declarations from HTML
        source = re.sub(r'@state\s+\w+="[^"]*"\s*\n?', '', source)
        
        return source
    
    def replace_bind(self, source: str) -> str:
        """@bind variable="stateName" binds input to state"""
        source = re.sub(
            r'@bind\s+(\w+)="(\w+)"',
            lambda m: f'data-bind="{m.group(2)}" id="bind-{m.group(2)}"',
            source
        )
        return source
    
    def replace_event(self, source: str) -> str:
        """@click="functionName()" or @change="functionName()"  """
        source = re.sub(
            r'@click="([^"]*)"',
            lambda m: f'onclick="{m.group(1)}"',
            source
        )
        source = re.sub(
            r'@change="([^"]*)"',
            lambda m: f'onchange="{m.group(1)}"',
            source
        )
        source = re.sub(
            r'@input="([^"]*)"',
            lambda m: f'oninput="{m.group(1)}"',
            source
        )
        return source
    
    def generate_html(self, compiled: str) -> str:
        """Generate complete HTML with styles and script"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus App</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
        }}
        
        .nxs-view {{
            display: flex;
            flex-direction: column;
        }}
        
        .nxs-card {{
            background: white;
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 8px;
        }}
        
        .nxs-btn {{
            background: #007AFF;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.2s;
        }}
        
        .nxs-btn:hover {{
            background: #0051D5;
        }}
        
        .nxs-input {{
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 16px;
            width: 100%;
        }}
        
        .nxs-input:focus {{
            outline: none;
            border-color: #007AFF;
            box-shadow: 0 0 0 3px rgba(0,122,255,0.1);
        }}
    </style>
</head>
<body>
    <div id="app">
{compiled}
    </div>
    
    <script>
        // Nexus Runtime
        const nxsState = {{}};
        
        function nxsStateUpdate(key, value) {{
            nxsState[key] = value;
            const bound = document.querySelector(`[data-bind="${{key}}"]`);
            if (bound) {{
                if (bound.type === 'text' || bound.type === 'input') {{
                    bound.value = value;
                }} else {{
                    bound.textContent = value;
                }}
            }}
        }}
        
        function nxsStateGet(key) {{
            return nxsState[key];
        }}
        
        // Bind input elements to state
        document.querySelectorAll('[data-bind]').forEach(el => {{
            const key = el.getAttribute('data-bind');
            if (el.type) {{
                el.addEventListener('input', (e) => {{
                    nxsStateUpdate(key, e.target.value);
                }});
            }}
        }});
    </script>
</body>
</html>"""


class NxsCompiler:
    def __init__(self, filepath: str):
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.source = f.read()
    
    def compile(self) -> str:
        """Compile .nxs to HTML"""
        parser = NxsParser(self.source)
        return parser.parse()
    
    def write_output(self, output_path: str):
        """Write compiled output"""
        html = self.compile()
        with open(output_path, 'w') as f:
            f.write(html)
        print(f"✓ Compiled {self.filepath} -> {output_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python nxs_frontend.py <input.nxs> [output.html]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.nxs', '.html')
    
    compiler = NxsCompiler(input_file)
    compiler.write_output(output_file)
