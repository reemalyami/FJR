import ply.lex as lex
import ply.yacc as yacc
import sys
import speech_recognition as sr
import pyttsx3 

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
t_ignore=r' '

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
    t.type='PRINT'
    return t

def t_Name(t):
    r'["#"][" "a-zA-Z_][" "a-zA-Z_0-9]*'
    t.value = t.value.lstrip("var")
    t.value = t.value.lstrip(" ")
    t.type='NAME'
    return t



def t_error(t):
    print('Illegal characters!')
    t.lexer.skip(1)
    
lexer= lex.lex()
precedence=(
        
        ('lef t','PLUS','MINUS'),
        ('left','MULTIPLY','DIVIDE')
        
        )
    
def p_calc(p):
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
    r = sr.Recognizer()     
    with sr.Microphone()as source:
        
        r.adjust_for_ambient_noise(source, duration=2)
        print('You Can Code')
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print ('You said: {}'.format(text))
        aInput = text.lower()
        
        
    except EOFError:
        break
    except:
        print('we couldnt hear you')
    if aInput == 'exit':
        quit()
    else:
        parser.parse(aInput)
    
