import ply.lex as lex

reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'def' : 'DEF',
    'int' : 'INT',
    'float' : 'FLOAT',
    'string' : 'STRING',
    'break' : 'BREAK',
    'print' : 'PRINT',
    'read' : 'READ',
    'return' : 'RETURN',
    'new' : 'NEW',
    'null' : 'NULL',
 }

tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'IDENT',
    'COMPARISON',
    'DIVIDE',
    'MOD',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'STRINGCONST',
    'INTCONST',
    'EQUAL',
    'FLOATCONST',
    'SEMICOLON',
        ] + list(reserved.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_MOD     = r'%'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'{'
t_RBRACE  = r'}'
t_COMPARISON = r'<|>|==|!=|<=|>='
t_EQUAL = r'='
t_SEMICOLON = r';'
t_STRINGCONST = r'"+.+"'
t_FLOATCONST = r'\d+\.\d+'
t_INTCONST = r'\d+'

def t_IDENT(t):
    r'[_A-Za-z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENT')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'
 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
 
lexer = lex.lex()

data = '''
 def string x = "adsfde"
 return f
 "~~~"
 '''

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok: 
        break
    print(tok)