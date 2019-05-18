#Ying Zhang 110864972

class SemanticError(Exception):
    pass


#names = {}


class Node:
    def __init__(self):
        print("init node")

    def evaluate(self):
        return 0

    def execute(self):
        return 0


class Stack():
    def __init__(self):
        self.stack = [{}] #initially one dictionary space for main vars
    def size(self):
        return len(self.stack)
    def main(self):
        return self.stack[0]
    def pop(self):
        self.stack.pop()

    def push(self,):
        self.stack.append({})#add new dictionary stack space for function

    def current(self):
        return self.stack[-1]   #return last dictionary, current space
    #uhh probably don't need peek for our purposes, will see later
    def assign(self,name,value):
        self.current()[name] = value

    #semantic error if args length and vals length do not match
    #assign local variables
    def make_new_stack_frame(self,args,vals):
        self.push()
        current = self.current()    #current stack frame

        if len(args)==len(vals):
            for i in range(len(args)):
                current[args[i].var()] = vals[i]
        else:

            raise SemanticError

stack = Stack()

class BooleanNode(Node):
    def __init__(self, v):
        if v=='True':
            self.value = True
        else:
            self.value = False

    def evaluate(self):
        return self.value

    def execute(self):
        return self.evaluate()

class StringNode(Node):
    def __init__(self, v):
        self.value = v[1:-1]

    def evaluate(self):
        return self.value

    def execute(self):
        return self.evaluate()


class TupleNode(Node):
    def __init__(self, v):
        self.value = v

    def evaluate(self):
        return tuple(self.value.evaluate())

    def execute(self):
        return self.evaluate()

class ListNode(Node):
    def __init__(self, v):
        self.value = v

    def evaluate(self):
        return self.value.evaluate()

    def execute(self):
        return self.evaluate()

class ElementNode(Node):
    def __init__(self, e):
        if e is None:
            self.e = []
        else:
            self.e = [e] #make a list structure
        # self.result = []

    def add(self,e):
        self.e = self.e + [e]

    def evaluate(self):
        result = []
        # if self.result == []:
        for i in range(len(self.e)):
            result.append( self.e[i].evaluate())

        return result

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

    def execute(self):
        return self.evaluate()

class NameNode(Node):
    def __init__(self, name):
        self.name = name
    def var(self):
        return self.name
    def evaluate(self):
        names = stack.current()

        if self.name in names:
            return names[self.name]
        else:

            raise SemanticError

    def execute(self):
        return self.evaluate()

#FUN NAME LPAREN args RPAREN EQUAL scope expression SEMICOLON'
class FunctionNode(Node):
    def __init__(self, name,args,block,output):
        global stack
        self.name = name
        self.args = args
        self.block = block
        self.output = output
        self.self_calling()   #can also call on the function itself from main

    def self_calling(self):

        stack.current()[self.name.var()] = self

    def evaluate(self,vals):
        #vals is in the form of element node, expressions sep by comma
        stack.make_new_stack_frame(self.args,vals.evaluate())
        #create new stack space and populate it with arguments
        # self.self_calling()


        self.block.execute()


        # if self.output.var() in stack.current():
        #     output = stack.current()[self.output.var()]
        # else:
        #     raise SemanticError

        output = self.output.evaluate()
        stack.pop()
        return output

    def execute(self,vals):
        return self.evaluate(vals)

class CallFuncNode(Node):
    def __init__(self,func,args):
        self.function = func
        self.args = args

    def evaluate(self):

        current_stack = stack.main()
        if self.function.var() in current_stack:
            func = current_stack[self.function.var()]
            return func.execute(self.args)
        else:

            raise SemanticError


    def execute(self):

        return self.evaluate()

#below are operations that can be done to nodes
class PrintNode(Node):
    def __init__(self, v):
        self.v = v

    def evaluate(self):
        # if (isinstance(self.v, str)):
        #     print("'" + self.v + "'")
        # else:
        print(self.v.evaluate())
        #we will no longer differentiate between strings and numbers

    def execute(self):

        self.evaluate()

class AssignNode(Node):
    def __init__(self,List,key,expression,boo):
        global stack
        self.boo = boo
        if self.boo:
            self.List = List
            self.key = key
        else:

            self.key = key.var()
        self.expression = expression


    def evaluate(self):
        if self.boo==True:
            L = self.List.evaluate()
            K = self.key.evaluate()
            if(not strictly_int(self.key)):

                raise SemanticError
        else:
            L = stack.current()
            K = self.key

        # self.expression = self.expression.evaluate()

        try:

            L[K] = self.expression.evaluate()


        except:
            raise SemanticError



    def execute(self):

        self.evaluate()

class BlockNode(Node):
    def __init__(self,s):
        self.st = s


    def evaluate(self):

        for statement in self.st:

            statement.execute()


    def execute(self):
        self.evaluate()


class IfNode(Node):
    def __init__(self,condition,if_statement,else_statement):

        self.condition = condition
        self.if_statement = if_statement
        self.else_statement = else_statement


    def evaluate(self):

        if (type(self.condition.evaluate()) != bool):
            raise SemanticError
        if(self.condition.evaluate()):
            self.if_statement.evaluate()
        else:
            if(self.else_statement!=None):
                self.else_statement.evaluate()


    def execute(self):
        self.evaluate()

class LoopNode(Node):
    def __init__(self,condition,block):
        self.condition = condition
        self.block = block


    def evaluate(self):
        if (type(self.condition.evaluate()) != bool):
            raise SemanticError


        while(self.condition.evaluate()==True):

            self.block.execute()


    def execute(self):
        self.evaluate()

class UminusNumberNode(Node):
    def __init__(self, v):
        self.value = v

    def evaluate(self):
        try:
            return -self.value.evaluate()
        except:
            raise SemanticError

    def execute(self):
        return self.evaluate()


class BopNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        try:
            a = self.v1
            b = self.v2

            c = type(a.evaluate())

            if (not type_match(a, b)):

                raise SemanticError
            elif (c==tuple or c==bool):

                raise SemanticError
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
                if(b.evaluate()==0 or not match_nums(a,b)):

                    raise SemanticError #div by zero error
                elif (self.op == '/'):
                    return self.v1.evaluate() / self.v2.evaluate()
                elif (self.op == 'div'):
                    return self.v1.evaluate() // self.v2.evaluate()
        except :
            raise SemanticError

    def execute(self):
        return self.evaluate()

class CompareopNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op
    def evaluate(self):
        if (not type_match(self.v1,self.v2)):
            raise SemanticError
        elif (type(self.v1.evaluate()) == list or type(self.v1.evaluate()) == tuple or type(self.v1.evaluate()) == bool):
            raise SemanticError
        else:
            try:
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
            except:

                raise SemanticError

    def execute(self):
        return self.evaluate()

class NotopNode(Node):
    def __init__(self, v):
        self.v = v

    def evaluate(self):
        if (not type(self.v.evaluate()) == bool):  # must be boolean types
            raise SemanticError
        return not(self.v.evaluate())

    def execute(self):
        return self.evaluate()

class AndORNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op
    def evaluate(self):

        x = self.v1.evaluate()
        y = self.v2.evaluate()

        if (not (type_match(self.v1,self.v2) and isinstance(x, bool))):
            raise SemanticError
        if (self.op == 'andalso'):
            return x and y
        elif (self.op == 'orelse'):
            return x or y

    def execute(self):
        return self.evaluate()

class InNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        try:
            return self.v1.evaluate() in self.v2.evaluate()
        except:
            raise SemanticError
    def execute(self):
        return self.evaluate()

class IndexNode(Node):
    def __init__(self, list, index,startWith1):
        self.list = list
        self.index = index
        self.pos = startWith1


    def evaluate(self):
        if (not strictly_int(self.index)):
            raise SemanticError
        try:
            return self.list.evaluate()[self.index.evaluate()-self.pos]
        except:
            raise SemanticError
    def execute(self):
        return self.execute()


class ConcatNode(Node):
    def __init__(self, hd,tl):
        self.hd=hd
        self.tl = tl

    def concat(self):
        if (not type(self.tl.evaluate()) == list):

            raise SemanticError
        else:

            # self.tl.evaluate().insert(0, self.hd.evaluate())
            #
            m = [self.hd.evaluate()] + self.tl.evaluate()

            return m

    def evaluate(self):
        return self.concat()
        #insert head at the beginning of list

    def execute(self):
        return self.evaluate()


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
    'fun'   : 'FUN',
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

lex.lex(debug=0)

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
    ('nonassoc','LPAREN','RPAREN'),
    ('nonassoc','LBRACKET','RBRACKET'),
    ('left','INDEX'),
)
def p_program(t):
    '''program : main
                | function_list main'''
    if len(t)==2:
        t[0] = t[1]
    else:
        t[0] = t[2]

def p_function(t):
    'function : FUN NAME LPAREN args RPAREN EQUAL scope expression SEMICOLON'
    t[0] = FunctionNode(t[2],t[4],t[7],t[8])

# def p_function1(t):
#     'function : FUN NAME LPAREN RPAREN EQUAL scope expression SEMICOLON'
#     t[0] = FunctionNode(t[2], [], t[7], t[8])
#     #empty arg function

def p_main_stack(t):
    ''' main : LBRACE block RBRACE
                | LBRACE RBRACE'''
    if len(t)==3:
        t[0] = BlockNode([])
    else:
        t[0] = BlockNode(t[2]) #a list of statements

def p_function_defs(t):
    '''function_list : function_list function
                | function'''
    if len(t)==2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[2]]



def p_arg_list(t):
    '''args : args COMMA NAME
                    | NAME
            '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1]+[t[3]]


def p_statements(t):
    '''statement :  assign_statement
    |               print_statement
    |               if_statement
    |               while_statement
    |               scope
    |               expression SEMICOLON'''
    t[0] = t[1]



def p_func_call(t):
    'expression : NAME LPAREN elements RPAREN '

    t[0] = CallFuncNode(t[1],t[3])


# def p_func_call1(t):
#     'expression : NAME LPAREN RPAREN '
#
#     t[0] = CallFuncNode(t[1],ElementNode(None))

# def p_state(t):
#     'statement : expression SEMICOLON'
#     t[1].evaluate() #check if errors occurred
#     t[0] = None


def p_scope(t):
    '''scope : LBRACE RBRACE
            | LBRACE block RBRACE'''
    if len(t)==3:
        t[0] = BlockNode([])
    else:
        t[0] = BlockNode(t[2]) #a list of statements


def p_block(t):
    '''block : block statement
            | statement

    '''
    if len(t) == 2:
        s = t[1]
        if s is not None:
            t[0] = [t[1]]
        else:
            t[0] = []
    else:
        s = t[2]
        if s is not None:
            t[0] = t[1] + [t[2]]
        else:
            t[0] = t[1]



# def p_empty(p):
#     'empty :'
#     pass



def p_statement_assign(t):
    'assign_statement : NAME EQUAL expression SEMICOLON'
    #5 = 4 is a syntax error, cant assign to literal in python

    t[0] = AssignNode(None,t[1],t[3],False)
    # t[0].evaluate()

def p_list_assign(t):
    'assign_statement : expression LBRACKET expression RBRACKET EQUAL expression SEMICOLON'
    t[0] = AssignNode(t[1], t[3], t[6],True)
    # t[0].evaluate()

#print node returns nothing

def p_statement_expr(t):
    '''print_statement : PRINT LPAREN expression RPAREN SEMICOLON
                | PRINT LPAREN RPAREN SEMICOLON'''

    if len(t)>5:
        t[0] = PrintNode(t[3])
    else:
        t[0] = PrintNode(StringNode(""))#print an empty line



#LBRACE block RBRACE
def p_if_statement(t):
    '''if_statement : IF LPAREN expression RPAREN scope
                    | IF LPAREN expression RPAREN scope ELSE scope '''


    if(len(t)==6):
        t[0] = IfNode(t[3],t[5],None)
    else:
        t[0] = IfNode(t[3],t[5],t[7])

    # t[0].execute()


def p_while_statement(t):
    '''while_statement : WHILE LPAREN expression RPAREN scope '''

    # if (type(condition) != bool):
    #     raise SemanticError
    # else:
    t[0] = LoopNode(t[3],t[5])

    # t[0].execute()



def match_int(a,b):
    if (strictly_int(a) and strictly_int(b)):
        return True
    else:
        return False

def match_float(a,b):
    if (type(a.evaluate()) == float and type(b.evaluate()) == float):
        return True
    else:
        return False

def match_nums(a,b):
    if(match_int(a,b)):
        return True
    elif(match_float(a,b)):
        return True
    elif (type(a.evaluate())==float and strictly_int(b)):
        return True
    elif (strictly_int(a) and type(b.evaluate())==float):
        return True
    else:
        return False

def type_match(a,b):

    if(type(a.evaluate())==type(b.evaluate())):
        return True
    else:
        return match_nums(a,b)

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression INTDIV expression
                  | expression MOD expression
                  | expression POW expression
                  | expression DIVIDE expression
                  | expression TIMES expression'''
    t[0] = BopNode(t[2], t[1], t[3])


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_in(t):
    '''expression : expression IN expression'''

    t[0] = InNode(t[2], t[1], t[3])


def p_expression_not(t):
    'expression : NOT expression'

        # doesn ot support lists

    t[0] = NotopNode(t[2])

def p_expression_bool(t):
    '''expression : expression AND expression
                  | expression OR expression'''
    #supported only for booleans

    t[0] = AndORNode(t[2], t[1], t[3])

def p_expression_compare(t):
    '''expression : expression GREATER expression
                | expression GREATEREQU expression
                | expression SMALLER expression
                | expression SMALLEREQU expression
                | expression EQUALS expression
                | expression NEQUALS expression'''

    t[0] = CompareopNode(t[2],t[1],t[3])

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'

    t[0] = UminusNumberNode(t[2])



def p_tuple(t):
    '''tuple : LPAREN elements RPAREN
            | LPAREN RPAREN'''
    if(len(t)==3):
        t[0] = TupleNode(ElementNode())
    else:
        t[0] = TupleNode(t[2])


#a list can be empty or contains one or more elements separated by commas
def p_list(t):
    '''list : LBRACKET elements RBRACKET
            | LBRACKET RBRACKET '''
    if(len(t)==3):
        t[0] = ListNode(ElementNode(None))  #with empty elements
    else:
        t[0] = ListNode(t[2])



#inner structure for lists, can be converted to tuples
def p_comma_sep_elements(t):
    '''elements : elements COMMA expression
            | expression
    '''
    if len(t) == 2:
        t[0] = ElementNode(t[1])
    else:
        t[1].add(t[3])
        t[0] = t[1]


def p_concat(t):
    '''expression : expression CONCAT expression'''
    t[0] = ConcatNode(t[1],t[3])
    # t[0].concat()

def p_index_list(t):
    'expression : expression LBRACKET expression RBRACKET'

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

    t[0] = IndexNode(t[3],t[2],1)  #index starts at 1 in sbml, but 0 in python, adjusted

#
# def p_index_exp(t):
#     'expression : INDEX expression LPAREN expression RPAREN'
#     t[0] = IndexNode(t[4], t[2], 1)


def p_expression_boolean(t):
    '''expression : BOOLEAN
                | NAME
                | list
                | tuple
                | STRING
                | NUMBER'''
    t[0] = t[1]

def p_error(t):
    raise SyntaxError


import ply.yacc as yacc

yacc.yacc(debug=0)#debug=0

import sys

if (len(sys.argv) != 2):
    sys.exit("Usage: python3 sbml.py inputFileName.txt")

fd = open(sys.argv[1], 'r')
code = ""
for line in fd:
    code += line.strip()

# print(code)

try:
    # lex.input(code)
    # while True:
    #     token = lex.token()
    #     if not token:
    #         break
    #     print(token)

    ast = yacc.parse(code)



    ast.execute()

except SemanticError:
    print("SEMANTIC ERROR")
except SyntaxError:
    print("SYNTAX ERROR")
# except:
#     print("exception")
#     pass

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