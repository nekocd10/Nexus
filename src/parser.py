"""
Nexus Language Parser
Builds AST from Nexus tokens
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from nexus_lexer import Token, TokenType, NexusLexer

# AST Node types for Nexus
@dataclass
class NexusNode:
    pass

@dataclass
class Program(NexusNode):
    statements: List[NexusNode]

@dataclass
class Literal(NexusNode):
    value: Any

@dataclass
class Identifier(NexusNode):
    name: str

@dataclass
class BinaryOp(NexusNode):
    left: NexusNode
    operator: str
    right: NexusNode

@dataclass
class ContextDef(NexusNode):
    name: str
    inputs: List[str]
    outputs: List[str]
    body: List[NexusNode]

@dataclass
class ReactionDef(NexusNode):
    name: str
    condition: Optional[NexusNode]
    body: List[NexusNode]

@dataclass
class GateDef(NexusNode):
    condition: NexusNode
    branches: List[tuple]  # List of (condition, body) pairs

@dataclass
class Flow(NexusNode):
    left: NexusNode
    direction: str  # '=>', '<=', '<>', '@>', '<@', '++>'
    right: NexusNode

@dataclass
class PoolLiteral(NexusNode):
    elements: List[NexusNode]

@dataclass
class KeyedPoolLiteral(NexusNode):
    pairs: List[tuple]  # List of (key, value) pairs

@dataclass
class VarDeclaration(NexusNode):
    mutable: bool  # True for @var, False for #var
    name: str
    value: Optional[NexusNode]

@dataclass
class Assignment(NexusNode):
    target: NexusNode
    value: NexusNode

class NexusParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]
    
    def peek_token(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]
    
    def advance(self):
        self.pos += 1
    
    def match(self, *types: TokenType) -> bool:
        return self.current_token().type in types
    
    def consume(self, token_type: TokenType, message: str = "") -> Token:
        if not self.match(token_type):
            raise SyntaxError(f"Expected {token_type}, got {self.current_token().type}. {message}")
        token = self.current_token()
        self.advance()
        return token
    
    def parse(self) -> Program:
        statements = []
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Optional[NexusNode]:
        # Context definition
        if self.match(TokenType.TILDE):
            self.advance()
            if self.match(TokenType.CONTEXT):
                return self.parse_context()
            elif self.match(TokenType.REACTION):
                return self.parse_reaction()
            elif self.match(TokenType.GATE):
                return self.parse_gate()
        
        # Variable declaration
        if self.match(TokenType.HASH, TokenType.AT):
            return self.parse_var_declaration()
        
        # Expression statement
        expr = self.parse_expression()
        return expr
    
    def parse_context(self) -> ContextDef:
        self.consume(TokenType.CONTEXT)
        name = self.consume(TokenType.IDENTIFIER).value
        
        inputs = []
        outputs = []
        
        if self.match(TokenType.AT):
            self.advance()
            if self.match(TokenType.IN):
                self.advance()
                self.consume(TokenType.COLON)
                inputs.append(self.consume(TokenType.IDENTIFIER).value)
                while self.match(TokenType.COMMA):
                    self.advance()
                    inputs.append(self.consume(TokenType.IDENTIFIER).value)
        
        if self.match(TokenType.AT):
            self.advance()
            if self.match(TokenType.OUT):
                self.advance()
                self.consume(TokenType.COLON)
                outputs.append(self.consume(TokenType.IDENTIFIER).value)
                while self.match(TokenType.COMMA):
                    self.advance()
                    outputs.append(self.consume(TokenType.IDENTIFIER).value)
        
        body = self.parse_block()
        return ContextDef(name, inputs, outputs, body)
    
    def parse_reaction(self) -> ReactionDef:
        self.consume(TokenType.REACTION)
        name = self.consume(TokenType.IDENTIFIER).value
        
        condition = None
        if self.match(TokenType.QUESTION):
            self.advance()
            condition = self.parse_expression()
        
        body = self.parse_block()
        return ReactionDef(name, condition, body)
    
    def parse_gate(self) -> GateDef:
        self.consume(TokenType.GATE)
        condition = self.parse_expression()
        
        branches = []
        
        if self.match(TokenType.QUESTION):
            self.advance()
            cond = self.parse_expression()
            self.consume(TokenType.FLOW_FORWARD)
            body = self.parse_expression()
            branches.append((cond, body))
            
            while self.match(TokenType.PIPE):
                self.advance()
                if self.match(TokenType.ELSE):
                    self.advance()
                    self.consume(TokenType.FLOW_FORWARD)
                    body = self.parse_expression()
                    branches.append(('else', body))
                else:
                    cond = self.parse_expression()
                    self.consume(TokenType.FLOW_FORWARD)
                    body = self.parse_expression()
                    branches.append((cond, body))
        
        return GateDef(condition, branches)
    
    def parse_var_declaration(self) -> VarDeclaration:
        mutable = False
        if self.match(TokenType.AT):
            self.advance()
            mutable = True
            self.consume(TokenType.IDENTIFIER)  # 'var'
        else:
            self.advance()  # #
            self.consume(TokenType.IDENTIFIER)  # 'var'
        
        name = self.consume(TokenType.IDENTIFIER).value
        value = None
        
        if self.match(TokenType.EQUAL):
            self.advance()
            value = self.parse_expression()
        
        return VarDeclaration(mutable, name, value)
    
    def parse_block(self) -> List[NexusNode]:
        statements = []
        
        # Optional brace or just parse statements
        if self.match(TokenType.LBRACE):
            self.advance()
            while not self.match(TokenType.RBRACE):
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            self.consume(TokenType.RBRACE)
        else:
            # Parse single statement or multiple indented statements
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return statements
    
    def parse_expression(self) -> NexusNode:
        return self.parse_flow()
    
    def parse_flow(self) -> NexusNode:
        left = self.parse_assignment()
        
        while self.match(TokenType.FLOW_FORWARD, TokenType.FLOW_BACKWARD, 
                         TokenType.FLOW_BOTH, TokenType.FLOW_CHANNEL,
                         TokenType.FLOW_CHANNEL_REV, TokenType.INCREMENT_FLOW):
            op_token = self.current_token()
            op = op_token.value
            self.advance()
            right = self.parse_assignment()
            left = Flow(left, op, right)
        
        return left
    
    def parse_assignment(self) -> NexusNode:
        expr = self.parse_or()
        
        if self.match(TokenType.EQUAL):
            self.advance()
            value = self.parse_expression()
            return Assignment(expr, value)
        
        return expr
    
    def parse_or(self) -> NexusNode:
        left = self.parse_and()
        
        while self.match(TokenType.PIPE):
            self.advance()
            right = self.parse_and()
            left = BinaryOp(left, '|', right)
        
        return left
    
    def parse_and(self) -> NexusNode:
        left = self.parse_comparison()
        
        return left
    
    def parse_comparison(self) -> NexusNode:
        left = self.parse_additive()
        
        while self.match(TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL,
                         TokenType.LESS, TokenType.GREATER,
                         TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op = self.current_token().value
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self) -> NexusNode:
        left = self.parse_multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.current_token().value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> NexusNode:
        left = self.parse_primary()
        
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.current_token().value
            self.advance()
            right = self.parse_primary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_primary(self) -> NexusNode:
        # Literals
        if self.match(TokenType.NUMBER):
            value = self.current_token().value
            self.advance()
            return Literal(value)
        
        if self.match(TokenType.STRING):
            value = self.current_token().value
            self.advance()
            return Literal(value)
        
        if self.match(TokenType.TRUE, TokenType.FALSE, TokenType.NULL):
            value = self.current_token().value
            self.advance()
            return Literal(value)
        
        # Identifiers
        if self.match(TokenType.IDENTIFIER):
            name = self.current_token().value
            self.advance()
            return Identifier(name)
        
        # Pool literal [| ... |]
        if self.match(TokenType.POOL_START):
            self.advance()
            elements = []
            if not self.match(TokenType.POOL_END):
                elements.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(TokenType.POOL_END):
                        break
                    elements.append(self.parse_expression())
            self.consume(TokenType.POOL_END)
            return PoolLiteral(elements)
        
        # Keyed pool literal [: ... :]
        if self.match(TokenType.KEYED_START):
            self.advance()
            pairs = []
            if not self.match(TokenType.KEYED_END):
                key = self.consume(TokenType.IDENTIFIER).value
                self.consume(TokenType.EQUAL)
                value = self.parse_expression()
                pairs.append((key, value))
                
                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(TokenType.KEYED_END):
                        break
                    key = self.consume(TokenType.IDENTIFIER).value
                    self.consume(TokenType.EQUAL)
                    value = self.parse_expression()
                    pairs.append((key, value))
            
            self.consume(TokenType.KEYED_END)
            return KeyedPoolLiteral(pairs)
        
        # Parenthesized expression
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr
        
        raise SyntaxError(f"Unexpected token: {self.current_token()}")


def parse_nexus(source: str) -> Program:
    lexer = NexusLexer(source)
    tokens = lexer.tokenize()
    parser = NexusParser(tokens)
    return parser.parse()


if __name__ == '__main__':
    code = '''
    ~context add_numbers
      @in: a, b
      @out: result
      result => a + b
    '''
    
    ast = parse_nexus(code)
    print(ast)
