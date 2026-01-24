"""
Nexus Language Interpreter
Executes Nexus AST
"""

from src.parser import *
from typing import Any, Dict, List, Optional
import sys

class NexusEnvironment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
    
    def define(self, name: str, value: Any, mutable: bool = True):
        self.vars[name] = {'value': value, 'mutable': mutable}
    
    def get(self, name: str) -> Any:
        if name in self.vars:
            return self.vars[name]['value']
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: Any):
        if name in self.vars:
            if not self.vars[name]['mutable']:
                raise RuntimeError(f"Cannot modify immutable binding: {name}")
            self.vars[name]['value'] = value
            return
        if self.parent:
            self.parent.set(name, value)
            return
        self.vars[name] = {'value': value, 'mutable': True}

class NexusContext:
    def __init__(self, name: str, inputs: List[str], outputs: List[str], 
                 body: List[NexusNode], closure: NexusEnvironment):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.body = body
        self.closure = closure
    
    def invoke(self, interpreter, args: Dict[str, Any]) -> Dict[str, Any]:
        context_env = NexusEnvironment(self.closure)
        
        # Bind inputs
        for param, arg in args.items():
            context_env.define(param, arg, mutable=True)
        
        # Execute body
        prev_env = interpreter.env
        interpreter.env = context_env
        results = {}
        
        try:
            for stmt in self.body:
                interpreter.visit(stmt)
            
            # Collect outputs
            for output_var in self.outputs:
                if output_var in context_env.vars:
                    results[output_var] = context_env.get(output_var)
        
        finally:
            interpreter.env = prev_env
        
        return results

class NexusInterpreter:
    def __init__(self):
        self.env = NexusEnvironment()
        self.contexts = {}
        self.setup_builtins()
    
    def setup_builtins(self):
        self.env.define('output', self.builtin_output, mutable=False)
        self.env.define('print', self.builtin_output, mutable=False)
        self.env.define('println', self.builtin_output, mutable=False)
        self.env.define('input', self.builtin_input, mutable=False)
        self.env.define('type_of', self.builtin_type_of, mutable=False)
        self.env.define('length', self.builtin_length, mutable=False)
    
    def builtin_output(self, value):
        print(value)
        return None
    
    def builtin_input(self, prompt=''):
        return input(str(prompt))
    
    def builtin_type_of(self, obj):
        if isinstance(obj, bool):
            return 'bool'
        elif isinstance(obj, int) or isinstance(obj, float):
            return 'num'
        elif isinstance(obj, str):
            return 'str'
        elif isinstance(obj, list):
            return 'pool'
        elif isinstance(obj, dict):
            return 'keyed_pool'
        elif obj is None:
            return 'null'
        return 'unknown'
    
    def builtin_length(self, obj):
        if isinstance(obj, (list, dict, str)):
            return len(obj)
        raise TypeError(f"No length for {type(obj).__name__}")
    
    def interpret(self, ast: Program) -> Any:
        result = None
        for stmt in ast.statements:
            result = self.visit(stmt)
        return result
    
    def visit(self, node: NexusNode) -> Any:
        if isinstance(node, Program):
            result = None
            for stmt in node.statements:
                result = self.visit(stmt)
            return result
        
        elif isinstance(node, Literal):
            return node.value
        
        elif isinstance(node, Identifier):
            return self.env.get(node.name)
        
        elif isinstance(node, PoolLiteral):
            return [self.visit(elem) for elem in node.elements]
        
        elif isinstance(node, KeyedPoolLiteral):
            result = {}
            for key, val_node in node.pairs:
                val = self.visit(val_node)
                result[key] = val
            return result
        
        elif isinstance(node, BinaryOp):
            return self.visit_binary_op(node)
        
        elif isinstance(node, VarDeclaration):
            value = self.visit(node.value) if node.value else None
            self.env.define(node.name, value, mutable=node.mutable)
            return value
        
        elif isinstance(node, Assignment):
            value = self.visit(node.value)
            if isinstance(node.target, Identifier):
                self.env.set(node.target.name, value)
            return value
        
        elif isinstance(node, ContextDef):
            context = NexusContext(node.name, node.inputs, node.outputs, node.body, self.env)
            self.contexts[node.name] = context
            self.env.define(node.name, context, mutable=False)
            return context
        
        elif isinstance(node, ReactionDef):
            # Reactions are stored for later execution
            return None
        
        elif isinstance(node, GateDef):
            return self.visit_gate(node)
        
        elif isinstance(node, Flow):
            return self.visit_flow(node)
        
        else:
            raise NotImplementedError(f"Node type {type(node).__name__} not implemented")
    
    def visit_binary_op(self, node: BinaryOp) -> Any:
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.operator == '+':
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            return left / right
        elif node.operator == '%':
            return left % right
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        elif node.operator == '<':
            return left < right
        elif node.operator == '>':
            return left > right
        elif node.operator == '<=':
            return left <= right
        elif node.operator == '>=':
            return left >= right
        elif node.operator == '|':
            return left or right
        else:
            raise ValueError(f"Unknown operator: {node.operator}")
    
    def visit_gate(self, node: GateDef) -> Any:
        base_condition = self.visit(node.condition)
        
        for pattern, body in node.branches:
            if pattern == 'else':
                return self.visit(body)
            
            cond = self.visit(pattern) if not isinstance(pattern, str) else pattern
            if cond == base_condition or self.is_truthy(cond):
                return self.visit(body)
        
        return None
    
    def visit_flow(self, node: Flow) -> Any:
        left = self.visit(node.left)
        
        # Forward flow: left result is used
        if node.direction == '=>':
            if isinstance(node.right, Identifier):
                # Try to call as function/context first
                try:
                    func = self.env.get(node.right.name)
                    if callable(func):
                        return func(left)
                    elif isinstance(func, NexusContext):
                        return func.invoke(self, {'input': left})
                    else:
                        # Assign result to variable
                        self.env.set(node.right.name, left)
                        return left
                except:
                    # Assign result to variable
                    self.env.set(node.right.name, left)
                    return left
            else:
                # Apply operation
                right = self.visit(node.right)
                return right
        
        # Increment flow
        elif node.direction == '++>':
            if isinstance(node.left, Identifier):
                current = self.env.get(node.left.name)
                next_val = current + 1
                self.env.set(node.left.name, next_val)
                return next_val
        
        # Other flows
        return self.visit(node.right)
    
    def is_truthy(self, value: Any) -> bool:
        if value is None or value is False:
            return False
        if value == 0 or value == '':
            return False
        return True


def run_nexus(source: str):
    from src.parser import parse_nexus
    ast = parse_nexus(source)
    interpreter = NexusInterpreter()
    return interpreter.interpret(ast)


if __name__ == '__main__':
    code = '''
    #var x = 10
    @var y = 20
    x => output
    '''
    
    run_nexus(code)
