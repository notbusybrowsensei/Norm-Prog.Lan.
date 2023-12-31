# NODES(for creating an Abstract Syntax Tree)
    
class NumNode(object):
    def __init__(self,token):
        self.token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f"{self.token}"
    

class StringNode(object):
    def __init__(self,token):
        self.token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f"{self.token}"
    

class ListNode(object):
    def __init__(self,elements,pos_start,pos_end):
        self.elements = elements
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"{self.elements}"

    
class BinOpNode(object):
    def __init__(self,left,op,right):
        self.left = left
        self.op = op
        self.right = right
        self.pos_start = self.left.pos_start
        self.pos_end = self.right.pos_end

    def __repr__(self):
       return f"({self.left},{self.op},{self.right})" 
    
class UnaryNode(object):
    def __init__(self,op,node):
        self.op = op
        self.node = node
        self.pos_start = self.op.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f"{self.op},{self.node}"
    

class VarAccessNode(object):
    def __init__(self,var_token):
        self.var_token = var_token
        #self.value = token.value
        self.pos_start = var_token.pos_start
        self.pos_end = var_token.pos_end

    def __repr__(self):
        return f"{self.var_token}"


class VarAssignNode(object):
    def __init__(self,var_token,val_node):
        self.var_token = var_token
        self.val_node = val_node
        self.pos_start = var_token.pos_start
        self.pos_end = val_node.pos_end

    def __repr__(self):
        return f"{self.var_token},{self.val_node}"
    
    

class IfNode(object):
    def __init__(self,cases,else_case):
        self.cases = cases
        self.else_case = else_case
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases)-1])[0].pos_end

    def __repr__(self):
        return f"{self.cases} /n {self.else_case}"
    

class ForNode(object):
    def __init__(self,var_name,start_val,end_val,stride_val,expression,return_null):
        self.var_name = var_name
        self.start_val = start_val
        self.end_val = end_val
        self.stride_val = stride_val
        self.expression = expression
        self.return_null = return_null
        self.pos_start = self.var_name.pos_start
        self.pos_end = self.expression.pos_end

    def __repr__(self):
        return f"{self.var_name},{self.start_val},{self.end_val},{self.stride_val},{self.expression}"
    

class WhileNode(object):
    def __init__(self,condition,expression,return_null):
        self.condition = condition
        self.expression = expression
        self.return_null = return_null
        self.pos_start = self.condition.pos_start
        self.pos_end = self.expression.pos_end

    def __repr__(self):
        return f"{self.condition},{self.expression}"
    

class FuncDefNode(object):
    def __init__(self,var_name,args,expression,auto_return):
        self.var_name = var_name
        self.args = args
        self.expression = expression
        self.auto_return = auto_return

        if self.var_name:
            self.pos_start = self.var_name.pos_start
        elif len(self.args) > 0:
            self.pos_start = self.args[0].pos_start
        else:
            self.pos_start = self.expression.pos_start

        self.pos_end = self.expression.pos_end


class CallFuncNode(object):
    def __init__(self,node_tocall,args_nodes):
        self.node_tocall = node_tocall
        self.args_nodes = args_nodes
        self.pos_start = self.node_tocall.pos_start

        if len(self.args_nodes) > 0:
            self.pos_end = self.args_nodes[len(self.args_nodes)-1].pos_end
        else:
            self.pos_end = self.node_tocall.pos_end


class ReturnNode(object):
    def __init__(self,node_to_return,pos_start,pos_end):
        self.node_to_return = node_to_return
        self.pos_start = pos_start
        self.pos_end = pos_end