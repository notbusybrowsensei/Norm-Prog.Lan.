# DECLARATIONS

EOF,INTEGER,FLOAT,PLUS,MINUS,MUL,DIV,LPAREN,RPAREN,ID,KEYWORD,EQUAL,DEQUAL,NOTEQUAL,LT,GT,LTE,GTE,COMMA,ARROW,STRING,LSQ,RSQ,POW,NEWLINE,COLON,MODULO = "EOF","INTEGER","FLOAT","PLUS","MINUS","MUL","DIV","(",")","ID","KEYWORD","EQUAL","DEQUAL","NOTEQUAL","LT","GT","LTE","GTE","COMMA","ARROW","STRING","LSQ","RSQ","POW","NEWLINE","COLON","MODULO"

TYPES = [PLUS,MINUS,MUL,DIV,LPAREN,RPAREN,EQUAL]
SIGNS = ['+','-','*','/','(',')','=']

KEYWORDS = ['VAR','AND','OR','NOT','IF','ELSE','ELIF','THEN','WHILE','FOR','TO','STRIDE','FUNC','END','RETURN']


# CREATING TOKEN CLASS(holds type,value and position of a token)

class Token(object):
    def __init__(self,type,value,pos_start=None,pos_end=None):
        self.type = type
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.next()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self,type,value):
        return self.type == type and self.value == value

    def __str__(self):
        type = self.type
        value = repr(self.value)

        return f"Token({type},{value})"
    
    def __repr__(self):
        return self.__str__()


# ERRORS(getting position at which error occured along with its details)

class Error(object):
    def __init__(self,pos_start,pos_end,error,info):
        self.error = error
        self.info = info
        self.pos_start = pos_start
        self.pos_end = pos_end

    def err_as_str(self):
        result = f"{self.error}: {self.info}"
        result += f"\n File {self.pos_start.fname}, line {self.pos_start.line+1}"
        return result
    
class InvalidCharError(Error):
    def __init__(self,pos_start,pos_end,info):
        super().__init__(pos_start,pos_end,"Invalid Character",info)

class InvalidSyntaxError(Error):
    def __init__(self,pos_start,pos_end,info):
        super().__init__(pos_start,pos_end,"Invalid Syntax",info)

class RuntimeError(Error):
    def __init__(self,pos_start,pos_end,info,context):
        super().__init__(pos_start,pos_end,"Runtime Error",info)
        self.context = context

    def as_string(self):
        result  = self.generate_traceback()
        result += f"{self.error}: {self.info}"
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result

class ExpectedCharError(Error):
    def __init__(self,pos_start,pos_end,info):
        super().__init__(pos_start,pos_end,"Expected Character Error",info)

    

# GETTING POSITION OF TOKENS

class Position(object):
    def __init__(self,index,line,column,fname,ftxt):
        self.index = index
        self.line = line
        self.column = column
        self.fname = fname
        self.ftxt = ftxt

    def next(self,current_char=None):
        self.index += 1
        self.column += 1

        if current_char == '\n':
            self.line += 1
            self.column = 0

        return self
    
    def copy(self):
        return Position(self.index,self.line,self.column,self.fname,self.ftxt)
    
    
# MAKING A LEXER(getting a list of tokens found in our input)    

class Lexer(object):
    def __init__(self,fname,text):
        self.fname = fname
        self.text = text
        self.position = Position(0,0,0,fname,text)
        self.current_char = self.text[self.position.index]
        self.flag1 = 0
        self.flag2 = 0

    def ignore_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.next()

    def ignore_comment(self):
        self.next()
        while self.current_char != '\n':
            self.next()

        self.next()

    def next(self):
        self.position.next(self.current_char)

        if self.position.index > len(self.text)-1:
            self.current_char = None
        else:
            self.current_char = self.text[self.position.index]

    def check_op(self):
        if self.current_char == '+':
            self.flag1 = 0
            self.flag2 = 0
            return 1
        
        elif self.current_char == '*':
            self.flag1 = 2
            self.flag2 = 2
            return 1
        
        elif self.current_char == '/':
            self.flag1 = 3
            self.flag2 = 3
            return 1
        
        elif self.current_char == '(':
            self.flag1 = 4
            self.flag2 = 4
            return 1
        
        elif self.current_char == ')':
            self.flag1 = 5
            self.flag2 = 5
            return 1
        

    def digit_dot(self):
        count = 0
        if self.current_char.isdigit(): count += 1
        if self.current_char == '.': count+=1

        if count == 1: return 1
        else: return 0

        
    def get_full_int(self):
        number = ''
        dots = 0
        pos_start = self.position.copy()

        while self.current_char is not None and self.digit_dot():
            if self.current_char == '.':
                if dots == 1: break
                dots += 1
            number += self.current_char
            self.next()

        if dots == 0: return Token(INTEGER,int(number),pos_start,self.position)
        else: return Token(FLOAT,float(number),pos_start,self.position)

        
    def make_id(self):
        name = ''
        pos_start = self.position

        while self.current_char is not None and self.current_char.isalnum():
            name += self.current_char
            self.next()

        if name in KEYWORDS:
            return Token(KEYWORD,name,pos_start,self.position)
        else:
            return Token(ID,name,pos_start,self.position)

    def make_not_equal(self):
        pos_start = self.position.copy()
        self.next()
        if self.current_char == '=':
            self.next()
            return Token(NOTEQUAL,'==',pos_start,self.position),None
        
        self.next()
        return None,ExpectedCharError(pos_start,self.position,f"'=' after '!'")
    
    def make_equal(self):
        pos_start = self.position.copy()
        self.next()
        if self.current_char == '=':
            self.next()
            return Token(DEQUAL,'==',pos_start,self.position)
        else:
            return Token(EQUAL,'=',pos_start,self.position)
        
    def make_less_than(self):
        pos_start = self.position.copy()
        self.next()
        if self.current_char == '=':
            self.next()
            return Token(LTE,'<=',pos_start,self.position)
        else:
            return Token(LT,'<',pos_start,self.position)
        
    def make_greater_than(self):
        pos_start = self.position.copy()
        self.next()
        if self.current_char == '=':
            self.next()
            return Token(GTE,'>=',pos_start,self.position)
        else:
            return Token(GT,'>',pos_start,self.position)
        

    def minus_or_arrow(self):
        token = Token(MINUS,'-',pos_start=self.position)
        pos_start = self.position.copy()
        self.next()

        if self.current_char == '>':
            self.next()
            token = Token(ARROW,'->',pos_start,self.position)

        return token
    

    def get_string(self):
        string = ''
        pos_start = self.position.copy()
        self.next()

        while self.current_char is not None and self.current_char != '"':
            string += self.current_char
            self.next()

        self.next()
        return Token(STRING,string,pos_start,self.position)


    def next_token(self):
        text = self.text
        tokens = []

        while self.current_char is not None:

            if self.current_char in ' \t':
                self.next()

            elif self.current_char == "@":
                self.ignore_comment()

            elif self.current_char == ';' or self.current_char == '\n':
                tokens.append(Token(NEWLINE,'NEWLINE',pos_start=self.position))
                self.next()

            elif self.current_char.isdigit():
                tokens.append(self.get_full_int())

            elif self.current_char.isalpha():
                tokens.append(self.make_id())

            elif self.current_char == '!':
                token,error = self.make_not_equal()
                if error: return [],error
                tokens.append(token)

            elif self.current_char == '=':
                tokens.append(self.make_equal())

            elif self.current_char == '^':
                tokens.append(Token(POW,'^',pos_start=self.position))
                self.next()

            elif self.current_char == '<':
                tokens.append(self.make_less_than())

            elif self.current_char == '>':
                tokens.append(self.make_greater_than())

            elif self.current_char == ',':
                tokens.append(Token(COMMA,',',pos_start=self.position))
                self.next()

            elif self.current_char == ':':
                tokens.append(Token(COLON,':',pos_start=self.position))
                self.next()

            elif self.current_char == '"':
                tokens.append(self.get_string())

            elif self.current_char == '%':
                tokens.append(Token(MODULO,'%',pos_start=self.position))
                self.next()

            elif self.current_char == '-':
                tokens.append(self.minus_or_arrow())

            elif self.current_char == '[':
                tokens.append(Token(LSQ,'[',pos_start=self.position))
                self.next()

            elif self.current_char == ']':
                tokens.append(Token(RSQ,']',pos_start=self.position))
                self.next()
            
            elif self.check_op():
                self.next()
                tokens.append(Token(TYPES[self.flag1],SIGNS[self.flag2],pos_start=self.position))

            else:
                pos_start = self.position.copy()
                char = self.current_char
                self.next()
                return [],InvalidCharError(pos_start,self.position,char)

        tokens.append(Token(EOF,None,pos_start=self.position))
        return tokens,None