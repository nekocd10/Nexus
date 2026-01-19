"""
Nexus Language Lexer
Tokenizes Nexus source code with unique syntax
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Unique Nexus Markers
    CONTEXT = auto()         # ~context
    REACTION = auto()        # ~reaction
    GATE = auto()            # ~gate
    RESONANCE = auto()       # ~resonance
    ASPECT = auto()          # #[aspect:]
    
    # Variable markers
    VAR_IMMUTABLE = auto()   # #var
    VAR_MUTABLE = auto()     # @var
    
    # Flow operators
    FLOW_FORWARD = auto()    # =>
    FLOW_BACKWARD = auto()   # <=
    FLOW_CHANNEL = auto()    # @>
    FLOW_CHANNEL_REV = auto() # <@
    FLOW_BOTH = auto()       # <>
    INCREMENT_FLOW = auto()  # ++>
    
    # Pool delimiters
    POOL_START = auto()      # [|
    POOL_END = auto()        # |]
    KEYED_START = auto()     # [:
    KEYED_END = auto()       # :]
    
    # Condition/branching
    QUESTION = auto()        # ?
    QUANTUM = auto()         # ?:
    PIPE = auto()            # |
    
    # State marker
    AT = auto()              # @
    HASH = auto()            # #
    TILDE = auto()           # ~
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    COLON = auto()
    DOT = auto()
    SEMICOLON = auto()
    EQUAL = auto()
    
    # Keywords
    IN = auto()             # @in:
    OUT = auto()            # @out:
    ELSE = auto()           # | else
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    POWER = auto()
    
    # Comparison
    EQUAL_EQUAL = auto()     # ==
    NOT_EQUAL = auto()       # !=
    LESS = auto()            # <
    GREATER = auto()         # >
    LESS_EQUAL = auto()      # <=
    GREATER_EQUAL = auto()   # >=
    
    # Special
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int

class NexusLexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        start_line, start_col = self.line, self.column
        num_str = ''
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            num_str += self.current_char()
            self.advance()
        
        value = float(num_str) if '.' in num_str else int(num_str)
        return Token(TokenType.NUMBER, value, start_line, start_col)
    
    def read_string(self, quote: str) -> Token:
        start_line, start_col = self.line, self.column
        self.advance()
        value = ''
        
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() == 'n':
                    value += '\n'
                elif self.current_char() == 't':
                    value += '\t'
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        self.advance()
        return Token(TokenType.STRING, value, start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line, start_col = self.line, self.column
        ident = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() in '_'):
            ident += self.current_char()
            self.advance()
        
        token_type = TokenType.IDENTIFIER
        value = ident
        
        if ident == 'context':
            token_type = TokenType.CONTEXT
        elif ident == 'reaction':
            token_type = TokenType.REACTION
        elif ident == 'gate':
            token_type = TokenType.GATE
        elif ident == 'resonance':
            token_type = TokenType.RESONANCE
        elif ident == 'true':
            token_type = TokenType.TRUE
            value = True
        elif ident == 'false':
            token_type = TokenType.FALSE
            value = False
        elif ident == 'null':
            token_type = TokenType.NULL
            value = None
        elif ident == 'else':
            token_type = TokenType.ELSE
        elif ident == 'in':
            token_type = TokenType.IN
        elif ident == 'out':
            token_type = TokenType.OUT
        
        return Token(token_type, value, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_comment()
                continue
            
            if self.current_char() is None:
                break
            
            line, col = self.line, self.column
            char = self.current_char()
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if char in '"\'':
                self.tokens.append(self.read_string(char))
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Multi-character operators
            if char == '=' and self.peek_char() == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.FLOW_FORWARD, '=>', line, col))
                continue
            
            if char == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.FLOW_BACKWARD, '<=', line, col))
                continue
            
            if char == '<' and self.peek_char() == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.FLOW_BOTH, '<>', line, col))
                continue
            
            if char == '@' and self.peek_char() == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.FLOW_CHANNEL, '@>', line, col))
                continue
            
            if char == '<' and self.peek_char() == '@':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.FLOW_CHANNEL_REV, '<@', line, col))
                continue
            
            if char == '+' and self.peek_char() == '+' and self.peek_char(2) == '>':
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.INCREMENT_FLOW, '++>', line, col))
                continue
            
            if char == '[' and self.peek_char() == '|':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.POOL_START, '[|', line, col))
                continue
            
            if char == '|' and self.peek_char() == ']':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.POOL_END, '|]', line, col))
                continue
            
            if char == '[' and self.peek_char() == ':':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.KEYED_START, '[:', line, col))
                continue
            
            if char == ':' and self.peek_char() == ']':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.KEYED_END, ':]', line, col))
                continue
            
            if char == '?' and self.peek_char() == ':':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.QUANTUM, '?:', line, col))
                continue
            
            if char == '=' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL_EQUAL, '==', line, col))
                continue
            
            if char == '!' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', line, col))
                continue
            
            if char == '<' and self.peek_char() != '=' and self.peek_char() != '@':
                self.advance()
                self.tokens.append(Token(TokenType.LESS, '<', line, col))
                continue
            
            if char == '>' and self.peek_char() != '=':
                self.advance()
                self.tokens.append(Token(TokenType.GREATER, '>', line, col))
                continue
            
            if char == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', line, col))
                continue
            
            if char == '>' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', line, col))
                continue
            
            # Single characters
            if char == '~':
                self.advance()
                self.tokens.append(Token(TokenType.TILDE, '~', line, col))
                continue
            
            if char == '@':
                self.advance()
                self.tokens.append(Token(TokenType.AT, '@', line, col))
                continue
            
            if char == '#':
                self.advance()
                self.tokens.append(Token(TokenType.HASH, '#', line, col))
                continue
            
            if char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', line, col))
                continue
            
            if char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', line, col))
                continue
            
            if char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', line, col))
                continue
            
            if char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', line, col))
                continue
            
            if char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', line, col))
                continue
            
            if char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', line, col))
                continue
            
            if char == '.':
                self.advance()
                self.tokens.append(Token(TokenType.DOT, '.', line, col))
                continue
            
            if char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', line, col))
                continue
            
            if char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL, '=', line, col))
                continue
            
            if char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, '+', line, col))
                continue
            
            if char == '-':
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, '-', line, col))
                continue
            
            if char == '*':
                self.advance()
                self.tokens.append(Token(TokenType.STAR, '*', line, col))
                continue
            
            if char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.SLASH, '/', line, col))
                continue
            
            if char == '%':
                self.advance()
                self.tokens.append(Token(TokenType.PERCENT, '%', line, col))
                continue
            
            if char == '?':
                self.advance()
                self.tokens.append(Token(TokenType.QUESTION, '?', line, col))
                continue
            
            if char == '|':
                self.advance()
                self.tokens.append(Token(TokenType.PIPE, '|', line, col))
                continue
            
            self.advance()
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

if __name__ == '__main__':
    code = '''
    ~context add_numbers
      @in: a, b
      @out: result
      result => a + b
    '''
    
    lexer = NexusLexer(code)
    tokens = lexer.tokenize()
    
    for token in tokens:
        print(f"{token.type.name:20} {str(token.value):20} Line {token.line}:{token.column}")
