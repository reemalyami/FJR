
import ply.lex as lex
import ply.yacc as yacc
import sys

tokens=[
        'INT',
        'FLOAT',
        'NAME',
        'PRINT',
        'PLUS',
        'MINUS',
        'MULTIPLY',
        'DIVIDE',
        'EQUALS',
        ]


t_PLUS=r'\+'
t_MINUS=r'\-'
t_MULTIPLY=r'\*'
t_DIVIDE=r'\/'
t_EQUALS=r'\='


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value=float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value=int(t.value)
    return t


def t_PRINT(t):
    r'["print"][" "a-zA-Z_#_0-9]*'
    t.value = t.value.lstrip("print")
    t.value = t.value.lstrip(" ")
   # if (t.value == 1):
     #   t.value=int(t.value)
    t.type='PRINT'
    return t

def t_Name(t):
    r'["#"][" "a-zA-Z_][" "a-zA-Z_0-9]*'
    t.value = t.value.lstrip("var")
    t.value = t.value.lstrip(" ")
    t.type='NAME'
    return t

t_ignore=r' '

def t_error(t):
    print('Illegal characters!')
    t.lexer.skip(1)
    
lexer= lex.lex()
precedence=(
        
        ('left','PLUS','MINUS'),
        ('left','MULTIPLY','DIVIDE')
        
        )
    
def p_calc(p):
    #calc is p[0]
    #var assign p[1]
    #empty p[2]
   '''
   calc : expression
        | var_assign
        | empty
        
   '''
   print(run(p[1]))

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
    
    '''
    p[0]=('=',p[1],p[3])
    

def p_expression(p):
   '''
   expression : expression MULTIPLY expression
              | expression DIVIDE expression
              | expression PLUS expression
              | expression MINUS expression
              

   '''
   
   p[0] = (p[2],p[1],p[3])
   
def p_expression_int_float(p):
   '''
   expression : INT
              | FLOAT     

   '''
   p[0] = p[1] 
   
def p_expression_var(p):
   '''
   expression : NAME
   '''
   p[0] =  ('var', p[1])
   
   
def p_expression_print(p):
   '''
   expression : PRINT
         
   '''
   p[0] =  ('text', p[1])

      
def p_error(p):
    
    print('syntax error')
    
    
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None
    
parser = yacc.yacc()
#env will save all valus that assign to the variable
env={}

def run(p):
    global env
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '=':
            env[p[1]] = run(p[2])
            print(env)
            # retrieve value of variable
        elif p[0] == 'var':
            if p[1] not in env:
                return "Undeclared variable found!"
            else:
                return env[p[1]]
            
        elif p[0] == 'text':
            if p[1] not in env:
                return p[1]
            else:
                return env[p[1]]

    
    else:
        return p
    
while True:
    try:
        s = input('>> ')
        
    except EOFError:
        break
    parser.parse(s)
    
