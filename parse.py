# CLASS WHICH HELP IN PARSING OUR RESULTS
import lexer,nodes
from lexer import *
from nodes import *

class ParseResult(object):
    def __init__(self):
        self.error = None
        self.node = None
        self.last_register_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.last_register_advance_count = 1
        self.advance_count += 1

    def register(self,res):
        self.last_register_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node
    
    def try_register(self,res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self,node):
        self.node = node
        return self

    def failure(self,error):
        self.error = error
        return self


# PARSING THROUGH THE TOKENS WE OBTAINED

class Parser(object):
    def __init__(self,tokens):
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = self.tokens[self.token_idx]

    def next(self):
        self.token_idx += 1
        self.update_current_token()

    def parse(self):
        result = self.statements()
        
        if not result.error and self.current_token.type != EOF:
            if type(result.node).__name__ == 'ForNode':
                if(result.node.var_name.type == ID): return result.failure(InvalidSyntaxError(result.node.pos_start,result.node.pos_end,f"Expected keyword-> FOR | TO | THEN | VAR"))
                else: return result.failure(InvalidSyntaxError(result.node.pos_start,result.node.pos_end,f"Expected keyword-> STRIDE"))
            
            elif type(result.node).__name__ == 'VarAccessNode':
                if(result.node.var_token.type == ID): return result.failure(InvalidSyntaxError(result.node.pos_start,result.node.pos_end,f"Place a relevant keyword"))
            
            return result.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Pass a recognizable Token"))
        return result
    
    def reverse(self, amount=1):
        self.token_idx -= amount
        self.update_current_token()
        return self.current_token

    def update_current_token(self):
        if self.token_idx >= 0 and self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]

# HIGHEST PRIORITY TO LOWEST(according to grammar rules)
    def base(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (INTEGER,FLOAT):
            res.register_advancement()
            self.next()
            return res.success(NumNode(token))
        
        elif token.type in (STRING):
            res.register_advancement()
            self.next()
            return res.success(StringNode(token))
        
        elif token.type == ID:
            res.register_advancement()
            self.next()
            return res.success(VarAccessNode(token))
        
        elif token.type == LPAREN:
            res.register_advancement()
            self.next()
            expression = res.register(self.expression())
            if res.error: return res

            if self.current_token.type == RPAREN:
                res.register_advancement()
                self.next()
                return res.success(expression)
            else:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected ) "))
            
        elif token.type == LSQ:
            list_expression = res.register(self.list_expression())
            if res.error: return res
            else:
                return res.success(list_expression)
            
        elif token.matches(KEYWORD,'IF'):
            if_expression = res.register(self.if_expression())
            if res.error: return res
            else:
                return res.success(if_expression)
            
        elif token.matches(KEYWORD,'FOR'):
            for_expression = res.register(self.for_expression())
            if res.error: return res
            else:
                return res.success(for_expression)
            
        elif token.matches(KEYWORD,'WHILE'):
            while_expression = res.register(self.while_expression())
            if res.error: return res
            else:
                return res.success(while_expression)
            
        elif token.matches(KEYWORD,'FUNC'):
            func_def = res.register(self.func_def())
            if res.error: return res
            else:
                return res.success(func_def)
            
        
        return res.failure(InvalidSyntaxError(token.pos_start,token.pos_end,"EXPECTED int, float, identifier, '+', '-', '(', '[', IF', 'FOR', 'WHILE', 'FUNC'"))



    def if_expression(self):
        res = ParseResult()
        all_cases = res.register(self.if_expression_cases('IF'))
        if res.error: return res
        cases,else_case = all_cases
        return res.success(IfNode(cases,else_case))
    
    
    def if_expression_cases(self,case_key):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(KEYWORD,case_key):
            return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,f"Expected '{case_key}'"))
        
        res.register_advancement()
        self.next()

        expression1 = res.register(self.expression())
        if res.error: return res

        if self.current_token.matches(KEYWORD,'THEN'):
            res.register_advancement()
            self.next()

            if self.current_token.type == NEWLINE:
                res.register_advancement()
                self.next()

                statements = res.register(self.statements())
                if res.error: return res
                cases.append((expression1, statements, True))

                if self.current_token.matches(KEYWORD, 'END'):
                    res.register_advancement()
                    self.next()
                else:
                    all_cases = res.register(self.elif_or_else_expression())
                    if res.error: return res
                    new_cases, else_case = all_cases
                    cases.extend(new_cases)
            else:
                expression2 = res.register(self.statement())
                if res.error: return res
                cases.append((expression1,expression2,False))

                all_cases = res.register(self.elif_or_else_expression())
                if res.error: return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)

            return res.success((cases,else_case))
        
    
    def elif_or_else_expression(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_token.matches(KEYWORD, 'ELIF'):
            all_cases = res.register(self.elif_expression())
            if res.error: return res
            cases,else_case = all_cases
        else:
            else_case = res.register(self.else_expression())
            if res.error: return res
        
        return res.success((cases,else_case))
    

    def elif_expession(self):
        return self.if_expression_cases('ELIF')
    

    def else_expression(self):
        res = ParseResult()
        else_case = None

        if self.current_token.matches(KEYWORD, 'ELSE'):
            res.register_advancement()
            self.next()

            if self.current_token.type == NEWLINE:
                res.register_advancement()
                self.next()

                statements = res.register(self.statements())
                if res.error: return res
                else_case = (statements,True)

                if self.current_token.matches(KEYWORD, 'END'):
                    res.register_advancement()
                    self.next()
                else:
                    return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected 'END'"))
            else:
                expr = res.register(self.statement())
                if res.error: return res
                else_case = (expr,False)

        return res.success(else_case)
        


    def for_expression(self):
        res = ParseResult()

        if not self.current_token.matches(KEYWORD,'FOR'):
            return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected 'FOR'"))
        
        res.register_advancement()
        self.next()

        if self.current_token.type != ID:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected Identifier"))
        
        var_name = self.current_token
        
        res.register_advancement()
        self.next()

        if self.current_token.type != EQUAL:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected equal to"))
        
        res.register_advancement()
        self.next()

        start_val = res.register(self.expression())
        if res.error: return res

        if not self.current_token.matches(KEYWORD,'TO'):
            return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected 'TO'"))
        
        res.register_advancement()
        self.next()

        end_val = res.register(self.expression())
        if res.error: return res

        if self.current_token.matches(KEYWORD,'STRIDE'):
            res.register_advancement()
            self.next()

            stride_val = res.register(self.expression())
            if res.error: return res
        else:
            if self.current_token.value.lower()=='stride': return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected 'STRIDE'"))

            stride_val = None

        if not self.current_token.matches(KEYWORD,'THEN'):
            return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected 'THEN'"))
        
        res.register_advancement()
        self.next()

        if self.current_token.type == NEWLINE:
            res.register_advancement()
            self.next()

            expression = res.register(self.statements())
            if res.error: return res

            if not self.current_token.matches(KEYWORD,'END'):
                return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected 'END'"))
            
            res.register_advancement()
            self.next()

            return res.success(ForNode(var_name,start_val,end_val,stride_val,expression,True))

        expression = res.register(self.statement())
        if res.error: return res

        return res.success(ForNode(var_name,start_val,end_val,stride_val,expression,False))


    def while_expression(self):
        res = ParseResult()

        if not self.current_token.matches(KEYWORD,'WHILE'):
            return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected 'WHILE'"))
        
        res.register_advancement()
        self.next()

        condition = res.register(self.expression())
        if res.error: return res

        if not self.current_token.matches(KEYWORD,'THEN'):
            return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected 'THEN'"))
        
        res.register_advancement()
        self.next()

        if self.current_token.type == NEWLINE:
            res.register_advancement()
            self.next()

            expression = res.register(self.statements())
            if res.error: return res

            if not self.current_token.matches(KEYWORD,'END'):
                return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected 'END'"))
            
            res.register_advancement()
            self.next()

            return res.success(WhileNode(condition,expression,True))

        expression = res.register(self.statement())
        if res.error: return res

        return res.success(WhileNode(condition,expression,False))
    

    def func_def(self):
        res = ParseResult()

        if not self.current_token.matches(KEYWORD,'FUNC'):
            return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected 'FUNC'"))
        
        res.register_advancement()
        self.next()

        if self.current_token.type == ID:
            var_name = self.current_token
            res.register_advancement()
            self.next()

            if self.current_token.type != LPAREN:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected '('"))
        else:
            var_name = None

            if self.current_token.type != LPAREN:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected identifier or '('"))
            
        res.register_advancement()
        self.next()
        args = []

        if self.current_token.type == ID:
            args.append(self.current_token)
            res.register_advancement()
            self.next()

            while self.current_token.type == COMMA:
                res.register_advancement()
                self.next()

                if self.current_token.type != ID:
                    return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected a valid parameter"))
                
                args.append(self.current_token)
                res.register_advancement()
                self.next()

            if self.current_token.type != RPAREN:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected ')'"))
            
        else:
            if self.current_token.type != RPAREN:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected identifier or ')'"))
            
        res.register_advancement()
        self.next()

        if self.current_token.type == ARROW:
            res.register_advancement()
            self.next()
            expression = res.register(self.expression())
            if res.error: return res

            return res.success(FuncDefNode(var_name,args,expression,True))
        
        if self.current_token.type == NEWLINE:
            res.register_advancement()
            self.next()

            expression = res.register(self.statements())
            if res.error: return res

            if not self.current_token.matches(KEYWORD,'END'):
                return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected 'END'"))
            
            res.register_advancement()
            self.next()

            return res.success(FuncDefNode(var_name,args,expression,False))
        
        return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected '->' or new line"))
    

    def list_expression(self):
        res = ParseResult()
        elements = []
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.type != LSQ:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected '['"))
        
        res.register_advancement()
        self.next()

        if self.current_token.type == RSQ:
            res.register_advancement()
            self.next()
        else:
            elements.append(res.register(self.expression()))
            if res.error:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected ']', 'VAR', 'IF', 'FOR', 'WHILE', 'FUNC', int, float, identifier, '+', '-', '(', '[' or 'NOT'"))
                
            while self.current_token.type == COMMA:
                res.register_advancement()
                self.next()

                elements.append(res.register(self.expression()))
                if res.error: return res

            if self.current_token.type != RSQ:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected ',' or ']'"))
                
            res.register_advancement()
            self.next()

        return res.success(ListNode(elements,pos_start,self.current_token.pos_end.copy()))
        
    

    def call(self):
        res = ParseResult()
        base = res.register(self.base())
        if res.error: return res

        if self.current_token.type == LPAREN:
            args = []
            res.register_advancement()
            self.next()

            if self.current_token.type == RPAREN:
                res.register_advancement()
                self.next()
            else:
                args.append(res.register(self.expression()))
                if res.error:
                    return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'FUNC', int, float, identifier, '+', '-', '(', '[' or 'NOT'"))
                
                while self.current_token.type == COMMA:
                    res.register_advancement()
                    self.next()

                    args.append(res.register(self.expression()))
                    if res.error: return res

                if self.current_token.type != RPAREN:
                    return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected ',' or ')'"))
                
                res.register_advancement()
                self.next()

            return res.success(CallFuncNode(base,args))
        
        return res.success(base)
    

    def power(self):
        res = ParseResult()
        left = res.register(self.call())
        if res.error: return res

        while self.current_token.type == POW:
            op = self.current_token
            res.register_advancement()
            self.next()
            right = res.register(self.factor())
            if res.error: return res
            left = BinOpNode(left,op,right)

        return res.success(left)
    

    def factor(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (PLUS,MINUS):
            res.register_advancement()
            self.next()
            if res.error: return res
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryNode(token,factor))
        
        return self.power()
    
        
    def term(self):
        res = ParseResult()
        left = res.register(self.factor())
        if res.error: return res

        while self.current_token.type in (MUL,DIV,COLON,MODULO):
            op = self.current_token
            res.register_advancement()
            self.next()
            right = res.register(self.factor())
            if res.error: return res
            left = BinOpNode(left,op,right)

        return res.success(left)
    

    def arith_expression(self):
        res = ParseResult()

        left = res.register(self.term())
        if res.error: return res

        while self.current_token.type in (PLUS,MINUS):
            op = self.current_token
            res.register_advancement()
            self.next() 
            right = res.register(self.term())
            if res.error: return res
            left = BinOpNode(left,op,right)

        return res.success(left)


    def comp_expression(self):
        res = ParseResult()

        if self.current_token.matches(KEYWORD,'NOT'):
            op = self.current_token
            res.register_advancement()
            self.next()
            
            node = res.register(self.comp_expression())
            if res.error: return res
            else:
                return res.success(UnaryNode(op,node))
            
        left = res.register(self.arith_expression())
        if res.error: return res

        while self.current_token.type in (DEQUAL,NOTEQUAL,LT,GT,LTE,GTE):
            op = self.current_token
            res.register_advancement()
            self.next()
            right = res.register(self.arith_expression())
            if res.error: return res
            left = BinOpNode(left,op,right)

        node = res.register(res.success(left))
        if res.error: return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected int, float, identifier, '+', '-', '(', '[', 'IF', 'FOR', 'WHILE', 'FUNC' or 'NOT'"))

        return res.success(node)


    def expression(self):
        res = ParseResult()

        if self.current_token.matches(KEYWORD,'VAR'):
            res.register_advancement()
            self.next()

            if self.current_token.type != ID:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected Identifier"))
            
            var_name = self.current_token
            res.register_advancement()
            self.next()

            if self.current_token.type != EQUAL:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected Equals sign"))
            
            res.register_advancement()
            self.next()
            expression = res.register(self.expression())

            if res.error: return res
            return res.success(VarAssignNode(var_name,expression))


        left = res.register(self.comp_expression())
        if res.error: return res

        while (self.current_token.type,self.current_token.value) in ((KEYWORD,'AND'),(KEYWORD,'OR')):
            op = self.current_token
            res.register_advancement()
            self.next()
            right = res.register(self.comp_expression())
            if res.error: return res
            left = BinOpNode(left,op,right)

        node = res.register(res.success(left))
        if res.error: return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Expected 'VAR', 'IF', 'FOR', 'WHILE', 'FUNC', int, float, identifier, '+', '-', '(', '[' or 'NOT'"))
                     
        return res.success(node)
    

    def statement(self):
        res = ParseResult()
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.matches(KEYWORD,'RETURN'):
            res.register_advancement()
            self.next()

            expression = res.try_register(self.expression())
            if not expression: self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expression,pos_start,self.current_token.pos_start.copy()))
        
        expression = res.register(self.expression())
        if res.error: return res.failure(InvalidSyntaxError(self.current_token.pos_start,self.current_token.pos_end,"Exppected 'RETURN', 'VAR', 'IF', 'FOR', 'WHILE', 'END', 'FUNC', int, float, identifier, '+', '-', '(', '[' or 'NOT'"))

        return res.success(expression)
    

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_token.pos_start.copy()

        while self.current_token.type == NEWLINE:
            res.register_advancement()
            self.next()

        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        more_statements = True

        while True:
            new_lines = 0
            while self.current_token.type == NEWLINE:
                res.register_advancement()
                self.next()
                new_lines += 1
            if new_lines == 0:
                more_statements = False

            if not more_statements: break

            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(statements,pos_start,self.current_token.pos_end.copy()))
    

    