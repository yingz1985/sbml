#Ying Zhang 110864972

class SemanticError(Exception):
    pass

names = {}
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
class NameNode(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        if self.name in names:
            return names[self.name]
        else:
            raise SemanticError


#below are operations that can be done to nodes
class PrintNode(Node):
    def __init__(self, v):
        self.v = v.evaluate()

    def evaluate(self):
        # if (isinstance(self.v, str)):
        #     print("'" + self.v + "'")
        # else:
        print(self.v)
        #we will no longer differentiate between strings and numbers

    def execute(self):
        self.evaluate()

class AssignNode(Node):
    def __init__(self,List,key,expression,boo):
        if boo:
            self.List = List.evaluate()
            self.key = key.evaluate()
        else:
            self.List = names
            self.key = key.name
        self.expression = expression.evaluate()

    #isnt applicable for printing
    def evaluate(self):
        self.List[self.key] = self.expression


    def execute(self):
        self.evaluate()

class BlockNode(Node):
    def __init__(self,statements):
        self.statements = statements

    #isnt applicable for printing
    def evaluate(self):
        for statement in self.statements:
            statement.execute()

    def execute(self):
        self.evaluate()

class LoopNode(Node):
    def __init__(self,condition,block):
        self.condition = condition.evaluate()
        self.block = block

    #isnt applicable for printings
    def evaluate(self):
        while(self.condition):
            self.block.evaluate()


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
        self.answer = False
    def exec(self):
        self.answer = self.v1 in self.v2
    def evaluate(self):
        return self.answer

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


reserved = {
    'if' : 'IF',
    # 'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'in' : 'IN',
    'andalso' : 'AND',
    'orelse' : 'OR',
    'div' : 'INTDIV',
    'mod' : "MOD",
    'not' : 'NOT',
    'True|False' : 'BOOLEAN',
    'print' : 'PRINT',
}

tokens = [
    'NUMBER','STRING','NAME',
    'LBRACKET','RBRACKET','COMMA',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS','NEQUALS','POW',
    'LPAREN', 'RPAREN',
    # 'AND', 'OR','NOT','IN',
    'SMALLER','GREATER','SMALLEREQU','GREATEREQU',
    # 'MOD','INTDIV','BOOLEAN'
    'CONCAT','INDEX','SEMICOLON','EQUAL','LBRACE','RBRACE',

]+list(reserved.values())#EQUAL taken out, NAME taken out


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
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SMALLER = r'<'
t_GREATER = r'>'
t_SMALLEREQU = r'<='
t_GREATEREQU = r'>='
t_EQUAL = r'='
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

def t_BOOLEAN(t):
    r'(True|False)'
    t.value = BooleanNode(t.value)
    return t
#single or double quote surrouding plus match any set of escape characters

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')  # Check for reserved words
    if t.type == 'NAME':
        t.value = NameNode(t.value)
    return t
#
# def t_IN(t):
#     r'in'
#     return t
#
# def t_AND(t):
#     r'andalso'
#     return t
#
# def t_OR(t):
#     r'orelse'
#     return t
#
# def t_NOT(t):
#     r'not'
#     return t
#
# def t_MOD(t):
#     r'mod'
#     return t
#
# def t_INTDIV(t):
#     r'div'
#     return t

def t_STRING(t):
    r'\"(\\\"|\\\'|\\\t|\\\\|\\n|[^\\\"])*\"|\'(\\\"|\\\\|\\\'|\\\t|\\n|[^\\\'])*\''
    t.value = StringNode(t.value)  #value without surrounding quotes
    return t

def t_error(t):
    raise SyntaxError


# Build the lexer
import ply.lex as lex

lex.lex()

# Parsing rules

precedence = (
    ('right','PRINT'),
    ('right','EQUAL'),
    ('left','OR'),
    ('left','AND'),
    ('right','NOT'),
    ('left', 'GREATER', 'GREATEREQU','SMALLER', 'SMALLEREQU','EQUALS','NEQUALS'),
    ('right', 'CONCAT'),
    ('left','IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE','MOD','INTDIV'),
    ('right','UMINUS'),
    ('right','POW'),
    ('nonassoc','LBRACKET','RBRACKET'),
    ('left','INDEX'),
)
def p_statements(t):
    '''statement : assign_statement
    |               print_statement
    |               if_statement
    |               while_statement
    |               scope'''
    t[0] = t[1]

def p_statement_assign(t):
    'assign_statement : NAME EQUAL expression SEMICOLON'
    #5 = 4 is a syntax error, cant assign to literal in python
    t[0] = AssignNode(names,t[1],t[3],False)
    t[0].evaluate()

def p_list_assign(t):
    'assign_statement : expression LBRACKET expression RBRACKET EQUAL expression SEMICOLON'

    if (type(t[1].evaluate())!=list or (not strictly_int(t[3])) ):
        raise SemanticError
    t[0] = AssignNode(t[1], t[3], t[6],True)
    t[0].evaluate()

def p_statement_expr(t):
    '''print_statement : PRINT LPAREN expression RPAREN SEMICOLON
                | PRINT LPAREN RPAREN SEMICOLON'''
    if len(t)>5:
        t[0] = PrintNode(t[3])
    else:
        t[0] = PrintNode(StringNode(""))#print an empty line

    t[0].execute()
    #print node returns nothing

def p_scope(t):
    '''scope : LBRACE RBRACE
            | LBRACE block RBRACE'''
    print("a block")
    if len(t)==3:
        t[0] = BlockNode()
    else:
        t[0] = t[3] #a list of statements

def p_block(t):
    '''block : statement
                | statement block
    '''

    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]

def p_if_statement(t):
    '''if_statement : IF LPAREN expression RPAREN block SEMICOLON
                    | IF LPAREN expression RPAREN block ELSE block SEMICOLON'''
    condition = t[3].evaluate()
    if(type(condition)!=bool):
        raise SemanticError
    if(condition):
        t[0] = t[5]
    elif(len(t)>6):
        t[0] = t[7]
def p_while_statement(t):
    '''while_statement : WHILE LPAREN expression RPAREN block SEMICOLON'''
    condition = t[3].evaluate()
    if (type(condition) != bool):
        raise SemanticError
    else:
        t[0] = LoopNode(t[3],t[5])



def match_int(t):
    if (strictly_int(t[1]) and strictly_int(t[3])):
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
    elif (type(t[1].evaluate())==float and strictly_int(t[3])):
        return True
    elif (strictly_int(t[1]) and type(t[3].evaluate())==float):
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

    if (type_match(t) == False or type(t[1].evaluate()) == tuple or type(t[1].evaluate())==bool):  # does not support tuple addition
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
    # print(t[1].evaluate()," in ",t[3].evaluate())
    if(type(t[3].evaluate())==list):
        t[0] = InNode(t[2],t[1],t[3])
        t[0].exec()
    elif (type(t[3].evaluate())==str and type(t[1].evaluate())==str):
        t[0] = InNode(t[2],t[1],t[3])
        t[0].exec()
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
    #supported only for booleans
    if(not (type_match(t) and isinstance(t[1].evaluate(),bool) ) ):
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
    elif(type(t[1].evaluate())==list or type(t[1].evaluate())==tuple or type(t[1].evaluate())==bool):
        raise SemanticError
    else:
        t[0] = CompareopNode(t[2],t[1],t[3])

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'

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
    if(not ( (type(t[1].evaluate())==list or type(t[1].evaluate())==str) and strictly_int(t[3]) ) ):   #list is an expression, the general form

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
def strictly_int(val):
    if isinstance(val.evaluate(), int) and not isinstance(val.evaluate(),bool):
        return True
    else:
        return False
#i(tuple)
def p_index_tuple(t):
    'expression : INDEX expression expression'
    if(not (isinstance(t[3].evaluate(),tuple) and strictly_int(t[2]) ) ):
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
                | NUMBER
                | NAME'''
    t[0] = t[1]

def p_error(t):
    raise SyntaxError


import ply.yacc as yacc

yacc.yacc()

import sys

if (len(sys.argv) != 2):
    sys.exit("Usage: python3 sbml.py inputFileName.txt")

fd = open(sys.argv[1], 'r')
code = ""
for line in fd:
    code += line.strip()

try:
    lex.input(code)
    while True:
        token = lex.token()
        if not token:
            break
        # print(token)

    ast = yacc.parse(code)
    # ast.execute()

except SemanticError:
    print("SEMANTIC ERROR")
except SyntaxError:
    print("SYNTAX ERROR")
except:
    pass

# for line in fd:
#     code = line.strip()
#     if not code:
#         continue
#
#     # lex.input(code)
#     # token = lex.token()
#     # if not token:
#     #     break
#     # print(token)
#     try:
#         ast = yacc.parse(code)
#
#         # ast.execute()
#         #don't always print
#     except SemanticError:
#         print("SEMANTIC ERROR")
#     except SyntaxError:
#         print("SYNTAX ERROR")
#     except:
#         pass