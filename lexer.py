# Programa do analisador lexico
# Desenvolvido por: 
# Arthur de Sousa Costa - 20100515
# Arthur Medeiros Machado de Souza - 20100517
# Felipe Del Corona Losso - 19200418
#
import ply.lex as lex
from prettytable import PrettyTable
import sys

#Tabelas de saidas
symbolTable = PrettyTable()
symbolTable.title = "Tabela de Símbolos"
symbolTable.field_names = ["Valor", "Linha", "Posição"]
tokenTable = PrettyTable()
tokenTable.title = "Tabela de Tokens"
tokenTable.field_names = ["Valor", "Tipo", "Linha", "Posição"]

# Leitura do arquivo de entrada 
with open(sys.argv[1], 'r') as my_file:
    data = my_file.read()

# Palavras reservadas
reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'def' : 'DEF',
    'for' : 'FOR',
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

# Tokens da linguagem
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
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'STRINGCONST',
    'INTCONST',
    'EQUAL',
    'FLOATCONST',
    'SEMICOLON',
    'COLON',
        ] + list(reserved.values())

# Regras para os tokens
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_MOD           = r'%'
t_DIVIDE        = r'/'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACE        = r'{'
t_RBRACE        = r'}'
t_LBRACKET      = r'\['
t_RBRACKET      = r'\]'
t_COMPARISON    = r'<|>|==|!=|<=|>='
t_EQUAL         = r'='
t_SEMICOLON     = r';'
t_COLON     = r','
t_STRINGCONST   = r'"+.+"'
t_FLOATCONST    = r'\d+\.\d+'
t_INTCONST      = r'\d+'

# Regra para o token de ident
def t_IDENT(t):
    r'[_A-Za-z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENT')
    return t

# Contagem de novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Comentarios
def t_COMMENT(t):
     r'\/\/.*'
     r'\/\*(.|\n)*\*\/'
     pass

# Tokens ignorados
t_ignore  = ' \t'
 
# Tratamento de erro
def t_error(t):
    print(f'Caracter Ilegal: \'{t.value[0]}\' na linha {t.lineno} coluna {find_column(data, t)}')
    t.lexer.skip(1)

# Função para achar a coluna de um token, só utilizada para erros
def find_column(input, token):
     lineStart = input.rfind('\n', 0, token.lexpos) + 1
     return (token.lexpos - lineStart) + 1
 
lexer = lex.lex()

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok: 
        break
    tokenTable.add_row([tok.value, tok.type, tok.lineno, tok.lexpos])

    if tok.type == "IDENT" :
        symbolTable.add_row([tok.value, tok.lineno, tok.lexpos])

print(tokenTable)
print(symbolTable)