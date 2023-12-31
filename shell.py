import interpreter,lexer,parse
from lexer import *
from parse import *
from interpreter import *


while True:
    text = input('norm >')
    if text.strip() == "": continue
    result,error = interpreter.run('<stdin>',text)

    if error: print(error.err_as_str())

    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))