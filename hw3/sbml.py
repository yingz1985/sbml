#Ying Zhang 110864972

class SemanticError(Exception):
    pass

class Node:
    def __init__(self):
        print("init node")

    def evaluate(self):
        return 0

    def execute(self):
        return 0

class BooleanNode(Node):
    def __init__(self, v):
        if v=='True':
            self.value = True
        else:
            self.value = False

    def evaluate(self):
        return self.value

    # def execute(self):
    #     return str(self.value).lower()

class StringNode(Node):
    def __init__(self, v):
        self.value = v[1:-1]

    def evaluate(self):
        return self.value

    # def execute(self):
    #     return "'"+self.value+"'"

class TupleNode(Node):
    def __init__(self, v):
        self.value = v

    def evaluate(self):
        return self.value

class ListNode(Node):
    def __init__(self, v):
        self.value = v

    def evaluate(self):
        return self.value


class NumberNode(Node):
    def __init__(self, v):
        try:
            if ('.' in v):
                self.value = float(v)
            else:
                self.value = int(v)
        except ValueError:
            print("value too large %d")
            self.value = 0

    def evaluate(self):
        return self.value
    # def execute(self):
    #     return self.value

#below are operations that can be done to nodes
class PrintNode(Node):
    def __init__(self, v):
        self.v = v.evaluate()

    def evaluate(self):
        if (isinstance(self.v, str)):
            print("'" + self.v + "'")
        else:
            print(self.v)

    def execute(self):
        self.evaluate()

class UminusNumberNode(Node):
    def __init__(self, v):
        self.value = v.evaluate()
    def uminus(self):
        try:
            self.value = -self.value
        except:
            raise SemanticError

    def evaluate(self):
        return self.value
    # def execute(self):
    #     return self.value


class BopNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        if (self.op == '+'):
            return self.v1.evaluate() + self.v2.evaluate()
        elif (self.op == '-'):
            return self.v1.evaluate() - self.v2.evaluate()
        elif (self.op == '*'):
            return self.v1.evaluate() * self.v2.evaluate()
        elif (self.op == 'mod'):
            return self.v1.evaluate() % self.v2.evaluate()
        elif(self.op=='**'):
            return self.v1.evaluate() ** self.v2.evaluate()
        else:
            if(self.v2.evaluate()==0):
                raise SemanticError #div by zero error
            elif (self.op == '/'):
                return self.v1.evaluate() / self.v2.evaluate()
            elif (self.op == 'div'):
                return self.v1.evaluate() // self.v2.evaluate()

    def execute(self):
        return self.evaluate()

class CompareopNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op
    def evaluate(self):
        if (self.op == '>'):
            return self.v1.evaluate() > self.v2.evaluate()
        elif (self.op == '<'):
            return self.v1.evaluate() < self.v2.evaluate()
        elif (self.op == '>='):
            return self.v1.evaluate() >= self.v2.evaluate()
        elif (self.op == '<='):
            return self.v1.evaluate() <= self.v2.evaluate()
        elif (self.op == '=='):
            return self.v1.evaluate() == self.v2.evaluate()
        elif (self.op == '<>'):
            return not(self.v1.evaluate() == self.v2.evaluate())

class NotopNode(Node):
    def __init__(self, v):
        self.v = v

    def evaluate(self):
        return not(self.v.evaluate())

class AndORNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op
    def evaluate(self):
        if (self.op == 'andalso'):
            return self.v1.evaluate() and self.v2.evaluate()
        elif (self.op == 'orelse'):
            return self.v1.evaluate() or self.v2.evaluate()

class InNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1.evaluate()
        self.v2 = v2.evaluate()
        self.op = op
    def evaluate(self):
        if (self.op == 'in'):
            return self.v1 in self.v2

class IndexNode(Node):
    def __init__(self, list, index,startWith1):
        self.list = list.evaluate()
        self.index = index.evaluate()-startWith1

    def evaluate(self):
        return self.list[self.index]

class ConcatNode(Node):
    def __init__(self, hd,tl):
        self.hd=hd.evaluate()
        self.tl = tl.evaluate()

    def concat(self):
        self.tl.insert(0, self.hd)

    def evaluate(self):
        return self.tl
        #insert head at the beginning of list



tokens = (
    'NUMBER','STRING',
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


def t_NUMBER(t):
    r'(\d+[.](\d*)?|[.]\d+)([eE][-]?\d+)?|\d+'

    try:
        t.value = NumberNode(t.value)
    except:
        print("value too large")
        t.value = 0
    return t

#single or double quote surrouding plus match any set of escape characters
def t_STRING(t):
    r'\"(\\\"|\\\'|\\\t|\\\\|\\n|[^\\\"])*\"|\'(\\\"|\\\\|\\\'|\\\t|\\n|[^\\\'])*\''
    t.value = StringNode(t.value)  #value without surrounding quotes
    return t

def t_BOOLEAN(t):
    r'(True|False)'
    t.value = BooleanNode(t.value)
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

def p_statement_expr(t):
    'statement : expression SEMICOLON'
    t[0] = PrintNode(t[1])
    #print node returns nothing


def match_int(t):
    if (type(t[1].evaluate()) == int and type(t[3].evaluate()) == int):
        return True
    else:
        return False

def match_float(t):
    if (type(t[1].evaluate()) == float and type(t[3].evaluate()) == float):
        return True
    else:
        return False

def match_nums(t):
    if(match_int(t)):
        return True
    elif(match_float(t)):
        return True
    elif (type(t[1].evaluate())==float and type(t[3].evaluate())==int):
        return True
    elif (type(t[1].evaluate())==int and type(t[3].evaluate())==float):
        return True
    else:
        return False

def type_match(t):
    if(len(t)<3):
        return True
    if(type(t[1].evaluate())==type(t[3].evaluate())):
        return True
    else:
        return match_nums(t)

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression INTDIV expression
                  | expression MOD expression
                  | expression POW expression
                  | expression DIVIDE expression
                  | expression TIMES expression'''

    if (type_match(t) == False or type(t[1].evaluate()) == tuple):  # does not support tuple addition
        raise SemanticError
    if t[2] == '+': #supports strings, and lists
        t[0] = BopNode(t[2],t[1],t[3])
    else:
        op = ['-','*','/','**']
        if (match_nums(t)):
            if t[2] in op:
                t[0] = BopNode(t[2],t[1],t[3])
            else:
                if (not match_int(t)):
                    raise SemanticError
                elif t[2] == "div":
                    t[0] = BopNode(t[2],t[1],t[3])
                elif t[2] == "mod":
                    t[0] = BopNode(t[2],t[1],t[3])

        else:
            raise SemanticError

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_in(t):
    '''expression : expression IN expression'''
    if(type(t[3].evaluate())==list):
        t[0] = InNode(t[2],t[1],t[3])
    elif (type(t[3].evaluate())==str and type(t[1].evaluate())==str):
        t[0] = InNode(t[2],t[1],t[3])
    else:
        raise SemanticError

def p_expression_not(t):
    'expression : NOT expression'
    if (not type(t[2].evaluate()) == bool):  # must be boolean types
        raise SemanticError
        # doesn ot support lists

    t[0] = NotopNode(t[2])

def p_expression_bool(t):
    '''expression : expression AND expression
                  | expression OR expression'''

    if(not (type_match(t) or isinstance(t[1],bool)) ):
        raise SemanticError
    else:
        t[0] = AndORNode(t[2], t[1], t[3])

def p_expression_compare(t):
    '''expression : expression GREATER expression
                | expression GREATEREQU expression
                | expression SMALLER expression
                | expression SMALLEREQU expression
                | expression EQUALS expression
                | expression NEQUALS expression'''
    if(not type_match(t)):
        raise SemanticError
    elif(type(t[1].evaluate())==list or type(t[1].evaluate())==tuple):
        raise SemanticError
    else:
        t[0] = CompareopNode(t[2],t[1],t[3])

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    # if(isinstance(t[2].evaluate(),int) or isinstance(t[2].evaluate(),float)):
    t[0] = UminusNumberNode(t[2])
    t[0].uminus()



def p_tuple(t):
    '''tuple : LPAREN elements RPAREN
            | LPAREN RPAREN'''
    if(len(t)==3):
        t[0] = TupleNode(())
    else:
        t[0] = TupleNode(tuple(t[2]))


#a list can be empty or contains one or more elements separated by commas
def p_list(t):
    '''list : LBRACKET elements RBRACKET
            | LBRACKET RBRACKET '''
    if(len(t)==3):
        t[0] = ListNode([])
    else:
        t[0] = ListNode(t[2])



#inner structure for lists, can be converted to tuples
def p_comma_sep_elements(t):
    '''elements : elements COMMA expression
            | expression
    '''

    if len(t) == 2:
        t[0] = [t[1].evaluate()]
    else:
        t[0] = t[1] + [t[3].evaluate()]


def p_concat(t):
    '''expression : expression CONCAT expression'''
    if(not type(t[3].evaluate())==list):
        raise SemanticError
    else:
        t[0] = ConcatNode(t[1],t[3])
        t[0].concat()

def p_index_list(t):
    'expression : expression LBRACKET expression RBRACKET'
    if(not ( (type(t[1].evaluate())==list or type(t[1].evaluate())==str) and type(t[3].evaluate())==int ) ):   #list is an expression, the general form

        raise SemanticError
    try:
        index = int(t[3].evaluate())
    except:

        raise SemanticError

    if(index>=len(t[1].evaluate()) or index<-len(t[1].evaluate())):    #-1 is last element, and goes backwards

        raise SemanticError
    else:
        t[0] = IndexNode(t[1],t[3],0)

        #index is currently not in brackets, but list is

#i(tuple)
def p_index_tuple(t):
    'expression : INDEX expression expression'
    if(not (isinstance(t[3].evaluate(),tuple) and isinstance(t[2].evaluate(),int))):
        raise SemanticError
    try:
        index = int(t[2].evaluate())
    except:
        raise SemanticError
    if(index>len(t[3].evaluate()) or index<1):
        raise SemanticError
    else:
        t[0] = IndexNode(t[3],t[2],1)  #index starts at 1 in sbml, but 0 in python, adjusted

def p_expression_boolean(t):
    '''expression : BOOLEAN
                | list
                | tuple
                | STRING
                | NUMBER'''
    t[0] = t[1]

def p_error(t):
    raise SyntaxError


import ply.yacc as yacc

yacc.yacc()

import sys

if (len(sys.argv) != 2):
    sys.exit("Usage: python3 sbml.py inputFileName.txt")

fd = open(sys.argv[1], 'r')

# for line in fd:
#     code += line.strip()
#
# try:
#     lex.input(code)
#     while True:
#         token = lex.token()
#         if not token: break
#         #print(token)
#
#     ast = yacc.parse(code)
#     ast.execute()
#
# except SemanticError:
#     print("SEMANTIC ERROR")
# except SyntaxError:
#     print("SYNTAX ERROR")
# except:
#     pass

# lex.input(code)
for line in fd:
    code = line.strip()
    if not code:
        continue
    # token = lex.token()
    # if not token: break
        #print(token)
    try:
        ast = yacc.parse(code)
        ast.execute()

    except SemanticError:
        print("SEMANTIC ERROR")
    except SyntaxError:
        print("SYNTAX ERROR")
    except:
        pass