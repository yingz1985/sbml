#Ying Zhang   110864972
import sys
import math
tokens = (
    'INTEGER','REAL','STRING',
    'LBRACKET','RBRACKET','COMMA',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS','NEQUALS','POW',
    'LPAREN', 'RPAREN','AND','OR','NOT','IN',
    'SMALLER','GREATER','SMALLEREQU','GREATEREQU',
    'MOD','INTDIV','CONCAT','INDEX','BOOLEAN','SEMICOLON',
)#EQUAL taken out, NAME taken out

t_ignore = " \t"
t_LBRACKET = '\['
t_RBRACKET = '\]'
t_COMMA = ','
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'=='
t_NEQUALS = r'<>'
t_POW = r'\*\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SMALLER = r'<'
t_GREATER = r'>'
t_SMALLEREQU = r'<='
t_GREATEREQU = r'>='
#t_EQUAL = r'='
t_CONCAT = r'::'
t_INDEX = r'[#]'
t_SEMICOLON = r';'

#t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

#float is 0+ digits . 0+ digits, allowing exponents
#in my language, 123. is equivalent to 123.0
#need to define real before integers
#3.0 will get recognized as 3 and .0 otherwise
def t_REAL(t):
    r'(\d+[.](\d*)?|[.]\d+)([eE][-]?\d+)?'

    try:
        t.value = float(t.value)
    except:
        print("Real value too large %f",t.value)
        t.value = 0
    return t

#positive numbers don't get the preceding +, but negative numbers do
def t_INTEGER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

#single or double quote surrouding plus match any set of escape characters
def t_STRING(t):
    r'\"(\\\"|\\\'|\\\t|\\\\|\\n|[^\\\"])*\"|\'(\\\"|\\\\|\\\'|\\\t|\\n|[^\\\'])*\''
    t.value = t.value[1:-1]  #value without surrounding quotes
    return t

def t_BOOLEAN(t):
    r'(true|false)'
    if(t.value=="true"):
        t.value = True
    else:
        t.value = False
    return t

def t_IN(t):
    r'in'
    return t

def t_AND(t):
    r'andalso'
    return t

def t_OR(t):
    r'orelse'
    return t

def t_NOT(t):
    r'not'
    return t

def t_MOD(t):
    r'mod'
    return t

def t_INTDIV(t):
    r'div'
    return t


def t_error(t):
    print("SYNTAX ERROR")
    raise SyntaxError


# Build the lexer
import ply.lex as lex

lex.lex()

# Parsing rules

precedence = (

    ('left','OR'),
    ('left','AND'),
    ('right','NOT'),
    ('left', 'GREATER', 'GREATEREQU','SMALLER', 'SMALLEREQU','EQUALS','NEQUALS'),
    ('right', 'CONCAT'),
    ('left','IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE','MOD','INTDIV'),
    ('right','POW'),
    ('nonassoc','LBRACKET','RBRACKET'),
    ('left','INDEX'),
    ('nonassoc','UMINUS'),
)
#equal is an assignment, out of precedence
# dictionary of names
# names = {}
#
# def p_statement_assign(t):
#     'statement : NAME EQUAL expression'
#     names[t[1]] = t[3]

def print_element(element):
    if (isinstance(element, str)):
        return "'" + str(element) + "'"
    elif (isinstance(element, bool)):
        if (element == True):
            return "true"
        else:
            return "false"
    elif (isinstance(element,list) ):
        return print_list(True,element)
    elif isinstance(element,tuple):
        return print_list(False,element)
    else:
        return str(element)

def print_list(list,elements):
    string = ""
    if list:
        string+="["
    else:
        string +="("

    for i in range(len(elements)):
        if(i==len(elements)-1):
            string += print_element(elements[i])
        else:
            string+= print_element(elements[i])+", "
    if list:
        string += "]"
    else:
        string += ")"

    return string

def p_statement_expr(t):
    'statement : expression SEMICOLON'
    if(isinstance(t[1],list)):
        print( print_list(True,list(t[1])) )
    elif isinstance(t[1],tuple):
        print( print_list(False,tuple(t[1])) )
    else:
        print(t[1])

# def p_statement_tup(t):
#     'statement : tuple'
#     print(t[1])

def p_expression_int(t):
    'expression : INTEGER'
    t[0] = t[1]
def p_expression_real(t):
    'expression : REAL'
    t[0] = t[1]

def match_int(t):
    if (type(t[1]) == int and type(t[3]) == int):
        return True
    else:
        return False
def match_float(t):
    if (type(t[1]) == float and type(t[3]) == float):
        return True
    else:
        return False

def match_nums(t):
    if(match_int(t)):
        return True
    elif(match_float(t)):
        return True
    elif (type(t[1])==float and type(t[3])==int):
        return True
    elif (type(t[1])==int and type(t[3])==float):
        return True
    else:
        return False

def type_match(t):
    if(len(t)<3):
        return True
    if(type(t[1])==type(t[3])):
        return True
    else:
        return match_nums(t)

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_add(t):
    'expression : expression PLUS expression'

    if(type_match(t)==False or type(t[1])==tuple):  #does not support tuple addition
        print("SEMANTIC ERROR")
        raise ValueError
    #if t[2] == '+':
    t[0] = t[1] + t[3]


def p_expression_minus(t):
    'expression : expression MINUS expression'
    if (match_nums(t)):
        t[0] = t[1] - t[3]
    else:
        print("SEMANTIC ERROR")
        raise ValueError
def p_expression_intop(t):
    '''expression :  expression INTDIV expression
                  | expression MOD expression '''
    if(not match_int(t)):
        print("SEMANTIC ERROR")
        raise ValueError
    elif t[2] == "div":
        if (t[3] == 0):
            print("DIV BY ZERO Exception")
            raise ValueError
        t[0] = t[1] // t[3]
    elif t[2] == "mod":
        t[0] = t[1] % t[3]


def p_expression_binop(t):
    '''expression :  expression TIMES expression
                  | expression DIVIDE expression
                  | expression POW expression
                  '''
    if(not match_nums(t)):  #check that they're number types
        print("SEMANTIC ERROR")
        raise ValueError

    if t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        if(t[3]==0):
            print("DIV BY ZERO")
            raise ZeroDivisionError
        else:
            t[0] = t[1] / t[3]
    elif t[2] == "**":
        t[0] = t[1]**t[3]


def p_expression_in(t):
    '''expression : expression IN expression'''
    if( type(t[3])==list):
        t[0] = t[1] in t[3]
    elif (type(t[3])==str and type(t[1])==str):
        t[0] = t[1] in t[3]
    else:
        print("SEMANTIC ERROR")
        raise ValueError

def p_expression_not(t):
    'expression : NOT expression'
    if (not type(t[2]) == bool):  # must be boolean types
        print("SEMANTIC ERROR")
        # doesn ot support lists
        raise ValueError

    if (t[1] == 'not'):
        t[0] = not (t[2])


def p_expression_bool(t):
    '''expression : expression AND expression
                    | expression OR expression'''

    if(not type_match(t)):
        print("SEMANTIC ERROR")
        raise ValueError


    if(t[2]=='andalso'):
        t[0] = (t[1] and t[3])
    elif(t[2]=='orelse'):
        t[0] = t[1] or t[3]


def p_expression_compare(t):
    '''expression : expression GREATER expression
                | expression GREATEREQU expression
                | expression SMALLER expression
                | expression SMALLEREQU expression
                | expression EQUALS expression
                | expression NEQUALS expression'''
    if(not type_match(t)):
        print("SEMANTIC ERROR")
        raise ValueError
    elif(type(t[1])==list or type(t[1])==tuple):
        print("SEMANTIC ERROR")
        #doesn ot support lists nor tuples
        raise ValueError


    if (t[2] == '>'):
        t[0] = t[1] > t[3]
    elif (t[2] == '>='):
        t[0] = t[1] >= t[3]
    elif (t[2] == '<'):
        t[0] = t[1] < t[3]
    elif (t[2] == '<='):
        t[0] = t[1] <= t[3]
    elif (t[2] == '=='):
        t[0] = t[1] == t[3]
    elif (t[2] == '<>'):
        t[0] = not(t[1] == t[3])

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    if(isinstance(t[2],int) or isinstance(t[2],float)):
        t[0] = -t[2]
    else:
        print("SEMANTIC ERROR")
        raise ValueError


def p_expression_boolean(t):
    'expression : BOOLEAN'
    t[0] = t[1]

def p_expression_list(t):
    'expression : list'
    t[0] = t[1]

def p_expression_tuple(t):
     'expression : tuple'
     t[0] = t[1]
#
# def p_expression_name(t):
#     'expression : NAME'
#     try:
#         t[0] = names[t[1]]
#     except LookupError:
#         print("SEMANTIC ERROR")
#         raise ValueError


#inner structure for lists, can be converted to tuples
def p_comma_sep_elements(t):
    '''elements : elements COMMA expression
            | expression
    '''

    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]

# #recursively define
# def p_comma_sep_tup(t):
#     '''tup : tup COMMA expression
#                 | expression
#         '''
#     if len(t) == 2:
#         t[0] = (t[1],)
#     else:
#         t[0] = t[1] + (t[3],)

def p_tuple(t):
    '''tuple : LPAREN elements RPAREN
            | LPAREN RPAREN'''
    if(len(t)==3):
        t[0] = ()
    else:
        t[0] = tuple(t[2])




#a list can be empty or contains one or more elements separated by commas
def p_list(t):
    '''list : LBRACKET elements RBRACKET
            | LBRACKET RBRACKET '''
    if(len(t)==3):
        t[0] = []
    else:
        t[0] = t[2]


def p_expression_string(t):
    'expression : STRING '
    t[0] = t[1]

def p_concat(t):
    '''expression : expression CONCAT expression'''
    if(not type(t[3])==list):
        print("SEMANTIC ERROR")
        raise SyntaxError
    l = list(t[3])
    l.insert(0, t[1])
    t[0] = l

def p_index_list(t):
    'expression : expression LBRACKET expression RBRACKET'
    if(not (type(t[1])==list or type(t[1])==str) ):   #list is an expression, the general form
        print("SEMANTIC ERROR")
        raise ValueError
    elif(not type(t[3])==int):
        print("SEMANTIC ERROR")
        raise ValueError
    try:
        index = int(t[3])
    except:
        print("SEMANTIC ERROR")
        raise ValueError

    if(abs(index)>=len(t[1]) ):    #-1 is last element, and goes backwards
        print("SEMANTIC ERROR")
        raise ValueError
    else:
        t[0] = t[1][index]

        #index is currently not in brackets, but list is

# def p_index_tup(t):
#     'expression : INDEX expression tuple'
#     try:
#         index = int(t[2])
#     except:
#         print("SEMANTIC ERROR")
#         raise ValueError
#
#     if(index>len(t[3]) or index<1):
#         print("SEMANTIC ERROR")
#         raise ValueError
#     else:
#         t[0] = t[3][index-1]  #index starts at 1 in sbml, but 0 in python, adjusted

#i(tuple)
def p_index_tuple(t):
    'expression : INDEX expression LPAREN expression RPAREN'
    if(not type(t[4])==tuple):
        print("SEMANTIC ERROR")
        raise ValueError
    elif(not type(t[2])==int):
        print("SEMANTIC ERROR")
        raise ValueError
    try:
        index = int(t[2])
    except:
        print("SEMANTIC ERROR")
        raise ValueError
    if(index>len(t[4]) or index<1):
        print("SEMANTIC ERROR")
        raise ValueError
    else:
        t[0] = t[4][index-1]  #index starts at 1 in sbml, but 0 in python, adjusted




def p_error(t):
    print("SYNTAX ERROR")
    raise SyntaxError

import ply.yacc as yacc

yacc.yacc()
if(len(sys.argv)!=2):
    print("Usage: python3 sbml.py inputFileName.txt")
    exit(0)
file_name = sys.argv[1]
file = open(file_name,'r') #open file name for reading


for line in file:
    #line = line.replace(";\n","\n")
    if(line=="\n"):
        continue    #has nothing else to parse..
    # elif(not (line.endswith(";") or line.endswith(";\n"))):
    #     print("SYNTAX ERROR")   #syntax error if it doesnt end with semicolon
    #     continue
    try:
        yacc.parse(line)
    except:
        continue #donothing, either semantic or syntatatic err is caught


# while 1:
#     try:
#         s = input('calc > ')  # Use raw_input on Python 2
#     except EOFError:
#         break
#     try:
#         yacc.parse(s)
#     except:
#         continue
