# Programa do analisador lexico
# Desenvolvido por: 
# Arthur de Sousa Costa - 20100515
# Arthur Medeiros Machado de Souza - 20100517
# Felipe Del Corona Losso - 19200418
#

import ply.lex as lex
from prettytable import PrettyTable
import ply.yacc as yacc
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
    'else' : 'ELSE',
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
    'SIGNAL',
    'IDENT',
    'COMPARISON',
    'MATH',
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
t_SIGNAL        = r'\+|-'
t_MATH          = r'/|%|\*'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACE        = r'{'
t_RBRACE        = r'}'
t_LBRACKET      = r'\['
t_RBRACKET      = r'\]'
t_COMPARISON    = r'<=|>=|==|!=|<|>'
t_EQUAL         = r'='
t_SEMICOLON     = r';'
t_COLON         = r','
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

error_token_list = []
error_production_list = []

def p_program(p):
    '''program : statement
               | funclist
               | epsilon'''

def p_funclist(p):
    '''funclist : funcdef funclistaux'''

def p_funclistaux(p):
    '''funclistaux : funclist
                   | epsilon'''

def p_funcdef(p):
    '''funcdef : DEF IDENT LPAREN paramlist RPAREN LBRACE statelist RBRACE'''

def p_paramlist(p):
    '''paramlist : type IDENT paramlistaux
                 | epsilon'''

def p_paramlistaux(p):
    '''paramlistaux : COLON paramlist
                    | epsilon'''

def p_statelist(p):
    '''statelist : statement statelistaux'''

def p_statelistaux(p):
    '''statelistaux : statelist
                     | epsilon'''

def p_statement(p):
    '''statement : vardecl SEMICOLON
                 | atribstat SEMICOLON
                 | printstat SEMICOLON
                 | readstat SEMICOLON
                 | returnstat SEMICOLON
                 | ifstat
                 | forstat
                 | LBRACE statelist RBRACE
                 | BREAK SEMICOLON
                 | SEMICOLON'''

def p_forstat(p):
    '''forstat : FOR LPAREN atribstat SEMICOLON expression SEMICOLON atribstat RPAREN'''

def p_ifstat(p):
    '''ifstat : IF LPAREN expression RPAREN statement ifstataux'''

def p_ifstataux(p):
    '''ifstataux : ELSE statement 
                 | epsilon'''

def p_returnstat(p):
    '''returnstat : RETURN'''

def p_printstat(p):
    '''printstat : PRINT expression'''

def p_readstat(p):
    '''readstat : READ expression'''

def p_atribstat(p):
    '''atribstat : lvalue EQUAL atribstat2'''

def p_atribstat2(p):
    '''atribstat2 : expression
                  | allocexpression
                  | funccall'''

def p_funccall(p):
    '''funccall : IDENT LPAREN paramlistcall RPAREN'''

def p_paramlistcall(p):
    '''paramlistcall : IDENT paramlistcallaux
                     | epsilon'''

def p_paramlistcallaux(p):
    '''paramlistcallaux : COLON paramlistcall
                        | epsilon'''

def p_allocexpression(p):
    '''allocexpression : NEW type numexpressionvectoraux'''

def p_expression(p):
    '''expression : numexpression expressionaux'''

def p_expressionaux(p):
    '''expressionaux : COMPARISON numexpression
                     | epsilon'''

def p_numexpressionvector(p):
    '''numexpressionvector : LBRACKET numexpression RBRACKET numexpressionvectoraux'''

def p_numexpressionvectoraux(p):
    '''numexpressionvectoraux : numexpressionvector
                              | epsilon'''

def p_numexpression(p):
    '''numexpression : term numexpressionaux'''

def p_numexpressionaux(p):
    '''numexpressionaux : numexpression2
                        | epsilon'''

def p_numexpression2(p):
    '''numexpression2 : SIGNAL term numexpressionaux'''

def p_term(p):
    '''term : unaryexpr termaux'''

def p_termaux(p):
    '''termaux : term2 
               | epsilon'''

def p_term2(p):
    '''term2 : MATH unaryexpr termaux'''

def p_unaryexpr(p):
    '''unaryexpr : SIGNAL factor
                 | factor'''

def p_factor(p):
    '''factor : INTCONST
              | STRINGCONST
              | FLOATCONST
              | NULL
              | lvalue
              | LPAREN numexpression RPAREN'''

def p_lvalue(p):
    '''lvalue : IDENT numexpressionvectoraux'''

def p_vardecl(p):
    '''vardecl : type IDENT vardeclaux'''

def p_vardeclaux(p):
    '''vardeclaux : vardecl2
                  | epsilon'''

def p_vardecl2(p):
    '''vardecl2 : LBRACKET INTCONST RBRACKET vardeclaux'''

def p_type(p):
    '''type : INT typeaux
            | FLOAT typeaux 
            | STRING typeaux'''

def p_typeaux(p):
    '''typeaux : type2
               | epsilon'''

def p_type2(p):
    '''type2 : LBRACKET RBRACKET typeaux'''

def p_epsilon(p):
    'epsilon :'
    pass

def p_error(p):
    if p:
        print(f'Token inesperado: \'{p.value}\' na linha {p.lineno}')
    else :
        print(f'Token inesperado: epsilon na linha {p.lineno}')

def error_handler(p):
    error_production_list.insert(0, p)

# Tratamento de erro
def t_error(t):
    print(f'Caracter Ilegal: \'{t.value[0]}\' na linha {t.lineno} coluna {find_column(data, t)}')
    t.lexer.skip(1)

# Função para achar a coluna de um token, só utilizada para erros
def find_column(input, token):
     lineStart = input.rfind('\n', 0, token.lexpos) + 1
     return (token.lexpos - lineStart) + 1
 
lexer = lex.lex()
parser = yacc.yacc()
parser.defaulted_states = {}

parser.parse(data)

for (p, t) in zip(error_production_list, error_token_list):
    print(f'Erro: token inesperado \'{t}\' na produção {p}')
