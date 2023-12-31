# CLASS THAT'LL HELP IN VISITING THE NODES
import nodes,parse,lexer,os,math
from nodes import *
from parse import *


class RTResult(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.func_return_val = None

    def register(self,res):
        self.error = res.error
        self.func_return_val = res.func_return_val
        return res.value
    
    def success(self,value):
        self.reset()
        self.value = value
        return self
    
    def success_return(self,value):
        self.reset()
        self.func_return_val = value
        return self
    
    def failure(self,error):
        self.reset()
        self.error = error
        return self
    
    def should_return(self):
        return (self.error or self.func_return_val)
    

# VALUES(Parent class-> data types like number,string,list inherit from it)
    
class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self,pos_start=None,pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def set_context(self,context=None):
        self.context = context
        return self
    
    def add_to(self,other):
        return None,self.illegal_operation(other)
    
    def sub_by(self,other):
        return None,self.illegal_operation(other)
    
    def mul_by(self,other):
        return None,self.illegal_operation(other)
    
    def div_by(self,other):
        return None,self.illegal_operation(other)
    
    def colon_by(self,other):
        return None,self.illegal_operation(other)
    
    def pow_by(self,other):
        return None,self.illegal_operation(other)
    
    def compare_equal(self,other):
        return None,self.illegal_operation(other)
    
    def compare_notequal(self,other):
        return None,self.illegal_operation(other)
    
    def compare_lessthan(self,other):
        return None,self.illegal_operation(other)
    
    def compare_greaterthan(self,other):
        return None,self.illegal_operation(other)
    
    def compare_lte(self,other):
        return None,self.illegal_operation(other)
    
    def compare_gte(self,other):
        return None,self.illegal_operation(other)
    
    def modulo_by(self,other):
        return None,self.illegal_operation(other)
    
    def and_by(self,other):
        return None,self.illegal_operation(other)
    
    def or_by(self,other):
        return None,self.illegal_operation(other)
    
    def not_by(self):
        return None,self.illegal_operation(other)
    
    def execute(self,args):
        return None,RTResult().failure(self.illegal_operation())
    
    def copy(self):
        raise Exception('No copy method defined')
    
    def is_true(self):
        return False
    
    def illegal_operation(self,other=None):
        if not other: other = self
        return RuntimeError(self.pos_start,other.pos_end,'Illegal operation',self.context)
    

    
class Number(Value):
    def __init__(self,value):
        super().__init__()
        self.value = value

    def add_to(self,other):
        if isinstance(other,Number):
            return Number(self.value+other.value).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def sub_by(self,other):
        if isinstance(other,Number):
            return Number(self.value-other.value).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def mul_by(self,other):
        if isinstance(other,Number):
            return Number(self.value*other.value).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def div_by(self,other):
        if isinstance(other,Number):
            if other.value == 0:
                return None,RuntimeError(other.pos_start,other.pos_end,"Division by zero",self.context)
            return Number(self.value/other.value).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def compare_equal(self,other):
        if isinstance(other,Number):
            return Number(int(self.value == other.value)).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def compare_notequal(self,other):
        if isinstance(other,Number):
            return Number(int(self.value != other.value)).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def compare_lessthan(self,other):
        if isinstance(other,Number):
            return Number(int(self.value < other.value)).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def compare_greaterthan(self,other):
        if isinstance(other,Number):
            return Number(int(self.value > other.value)).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def compare_lte(self,other):
        if isinstance(other,Number):
            return Number(int(self.value <= other.value)).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def compare_gte(self,other):
        if isinstance(other,Number):
            return Number(int(self.value >= other.value)).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def pow_by(self,other):
        if isinstance(other,Number):
            return Number(self.value**other.value).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def modulo_by(self,other):
        if isinstance(other,Number):
            return Number(self.value%other.value).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def and_by(self,other):
        if isinstance(other,Number):
            return Number(int(self.value and other.value)).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def or_by(self,other):
        if isinstance(other,Number):
            return Number(int(self.value or other.value)).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def not_by(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context),None
    
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start,self.pos_end)
        copy.set_context(self.context)
        return copy
        
    def is_true(self):
        return self.value != 0
        
    def __repr__(self):
        return str(self.value)



class String(Value):
    def __init__(self,value):
        super().__init__()
        self.value = value

    def add_to(self,other):
        if isinstance(other,String):
            return String(self.value+other.value).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def mul_by(self,other):
        if isinstance(other,Number):
            return String(self.value*other.value).set_context(self.context),None
        else:
            return None,Value.illegal_operation(self,other)
        
    def is_true(self):
        return len(self.value) > 0
    
    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start,self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return str(self.value)
    


class List(Value):
    def __init__(self,elements):
        super().__init__()
        self.elements = elements

    def add_to(self,other):
        if isinstance(other,List): return None,Value.illegal_operation(self,other)
        list = List([])
        for element in self.elements:
            list.elements.append(element)
        list.elements.append(other.value)
        return list,None
    
    def mul_by(self, other):
        if isinstance(other,List):
            list = List([])
            for element in self.elements:
                list.elements.append(element)
            list.elements.extend(other.elements)
            return list,None
        else:
            return None,Value.illegal_operation(self,other)

    def sub_by(self,other):
	if isinstance(other,Number):
            list = List([])
            for element in self.elements:
                list.elements.append(element)
            try:
                list.elements.pop(other.value)
                return list,None
            except:
                return None,RuntimeError(other.pos_start,other.pos_end,"Index out of bound",self.context)
        else:
            return None,Value.illegal_operation(self,other)
        
        
    def colon_by(self,other):
        if isinstance(other,Number):
            try:
                return self.elements[other.value],None
            except:
                return None,RuntimeError(other.pos_start,other.pos_end,"Index out of bound",self.context)
        else:
            return None,Value.illegal_operation(self,other)
        
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start,self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return f'[{", ".join([str(element) for element in self.elements])}]'
    
    def __repr__(self):
        return f'[{", ".join([str(element) for element in self.elements])}]'
    


class BaseFunction(Value):
    def __init__(self,name):
        super().__init__()
        self.name = name

    def make_context(self):
        new_context = Context(self.name,self.context,self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context
    
    def check_args(self,arg_names,args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RuntimeError(self.pos_start,self.pos_end,"Lessen the args",self.context))
        
        if len(args) < len(arg_names):
            return res.failure(RuntimeError(self.pos_start,self.pos_end,"Pass more args",self.context))
        
        return res.success(None)
    
    def populate_args(self,arg_names,args,execute_context):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_val = args[i]
            arg_val.set_context(execute_context)
            execute_context.symbol_table.set(arg_name,arg_val)

    def check_and_populate_args(self,arg_names,args,execute_context):
        res = RTResult()

        res.register(self.check_args(arg_names,args))
        if res.should_return(): return res
        self.populate_args(arg_names,args,execute_context)

        return res.success(None)



class Function(BaseFunction):
    def __init__(self,name,expression,args,auto_return):
        super().__init__(name)
        self.expression = expression
        self.args = args
        self.auto_return = auto_return

    def execute(self,args):
        res = RTResult()
        interpreter = Interpreter()
        new_context = self.make_context()

        res.register(self.check_and_populate_args(self.args,args,new_context))
        if res.should_return(): return res

        val = res.register(interpreter.visit(self.expression,new_context))
        if res.should_return() and res.func_return_val == None: return res

        return_val = (val if self.auto_return else None) or res.func_return_val or Number.null
        return res.success(return_val)
    
    def copy(self):
        copy = Function(self.name,self.expression,self.args,self.auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start,self.pos_end)
        return copy
    
    def __repr__(self):
        return f"<function {self.name}>"
    


class BuiltInFunction(BaseFunction):
    def __init__(self,name):
        super().__init__(name)

    def no_visit_method(self):
        raise Exception(f"No exec_{self.name} method defined")

    def execute(self,args):
        res = RTResult()
        new_context = self.make_context()
        method_name = f"exec_{self.name}"

        method = getattr(self,method_name,self.no_visit_method)
        res.register(self.check_and_populate_args(method.arg_names,args,new_context))
        if res.should_return(): return res

        return_val = res.register(method(new_context))
        if res.should_return(): return res

        return res.success(return_val) 
    
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start,self.pos_end)
        return copy
    
    def __repr__(self):
        return f"<built-in-function {self.name}>"
    
# DEFINING BUILT IN FUNCTIONS
    def exec_print(self,execute_context):
        print(str(execute_context.symbol_table.get("value")))
        return RTResult().success(Number.null)
    exec_print.arg_names = ["value"]

    def exec_input(self,execute_context):
        text = input()
        return RTResult().success(String(text))
    exec_input.arg_names = []

    def exec_int_input(self,execute_context):
        while True:
            text = input()
            try: 
                num = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer")

        return RTResult().success(Number(num))
    exec_int_input.arg_names = []

    def exec_clear(self,execute_context):
        os.system('cls' if os.name == 'nt' else 'clear')
        return RTResult().success(Number.null)
    exec_clear.arg_names = []

    def exec_is_num(self,execute_context):
        is_num = isinstance(execute_context.symbol_table.get("value"),Number)
        return RTResult().success(Number.true if is_num else Number.false)
    exec_is_num.arg_names = ["value"]

    def exec_is_str(self,execute_context):
        is_str = isinstance(execute_context.symbol_table.get("value"),String)
        return RTResult().success(Number.true if is_str else Number.false)
    exec_is_str.arg_names = ["value"]

    def exec_is_list(self,execute_context):
        is_list = isinstance(execute_context.symbol_table.get("value"),List)
        return RTResult().success(Number.true if is_list else Number.false)
    exec_is_list.arg_names = ["value"]

    def exec_is_func(self,execute_context):
        is_func = isinstance(execute_context.symbol_table.get("value"),BaseFunction)
        return RTResult().success(Number.true if is_func else Number.false)
    exec_is_func.arg_names = ["value"]

    def exec_num(self,execute_context):
        num = execute_context.symbol_table.get("value")

        if isinstance(num,List): return RTResult().failure(RuntimeError(self.pos_start,self.pos_end,"Argument should be a string with numbers or int|float",execute_context))
        if isinstance(num,String):
            for i in range(len(num.value)):
                if num.value[i] not in '1234567890':
                    return RTResult().failure(RuntimeError(self.pos_start,self.pos_end,"Argument should be a string with numbers or int|float",execute_context))
            return RTResult().success(Number(int(num.value)))
        if isinstance(num,Number): return RTResult().success(num)
    exec_num.arg_names = ["value"]

    def exec_str(self,execute_context):
        string = execute_context.symbol_table.get("value")

        if isinstance(string,List): return RTResult().failure(RuntimeError(self.pos_start,self.pos_end,"Argument should be an int or float",execute_context))
        if isinstance(string,String): return RTResult().success(str)

        if isinstance(string,Number): 
            stringx = str(string.value)
            return RTResult().success(String(stringx))
    exec_str.arg_names = ["value"]

    def exec_gint(self,execute_context):
        num = execute_context.symbol_table.get("value")

        if not isinstance(num,Number): return RTResult().failure(RuntimeError(self.pos_start,self.pos_end,"Argument should be an int or float",execute_context))
        return RTResult().success(Number(math.floor(num.value)))
    exec_gint.arg_names = ["value"]

    def exec_round(self,execute_context):
        num = execute_context.symbol_table.get("value")

        if not isinstance(num,Number): return RTResult().failure(RuntimeError(self.pos_start,self.pos_end,"Argument should be an int or float",execute_context))
        return RTResult().success(Number(math.ceil(num.value)))
    exec_round.arg_names = ["value"]

    def exec_len_str(self,execute_context):
        string = execute_context.symbol_table.get("string")

        if not isinstance(string,String): return RTResult().failure(RuntimeError(self.pos_start,self.pos_end,"Argument should be a string",execute_context))
        return RTResult().success(Number(len(string.value)))
    exec_len_str.arg_names = ["string"]

    def exec_len(self,execute_context):
        list = execute_context.symbol_table.get("list")

        if isinstance(list,Number): return RTResult().failure(RuntimeError(self.pos_start,self.pos_end,"Argument should be a list or string",execute_context))
        if isinstance(list,List): return RTResult().success(Number(len(list.elements)))
        if isinstance(list,String): return RTResult().success(Number(len(list.value)))
    exec_len.arg_names = ["list"]


    def exec_run(self,execute_context):
        fname = execute_context.symbol_table.get("fname")

        if not isinstance(fname,String): return RTResult().failure(RuntimeError(self.pos_start,self.pos_end,"Argument should be a string",execute_context))

        fname = fname.value
        # ftype = fname[-5:]
        if len(fname) <= 5 or fname[-5:] != ".norm": return RTResult().failure(RuntimeError(self.pos_start,self.pos_end,"Create a '.norm' file for script execution",execute_context))

        try: 
            with open(fname,"r") as f:
                script = f.read()
        except Exception as e: return RTResult().failure(RuntimeError(self.pos_start,self.pos_end,f"Failed to load script {fname} \n"+str(e),execute_context))

        _,error = run(fname,script)

        if error: return RTResult().failure(RuntimeError(self.pos_start,self.pos_end,f"Failed to finish script execution {fname} \n"+error.err_as_str(),execute_context))

        return RTResult().success(Number.null)
    exec_run.arg_names = ["fname"]


Number.null = Number(0)
Number.true = Number(1)
Number.false = Number(0)

BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.int_input = BuiltInFunction("int_input")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.is_num = BuiltInFunction("is_num")
BuiltInFunction.is_str = BuiltInFunction("is_str")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_func = BuiltInFunction("is_func")
BuiltInFunction.num = BuiltInFunction("num")
BuiltInFunction.str = BuiltInFunction("str")
BuiltInFunction.len = BuiltInFunction("len")
BuiltInFunction.gint = BuiltInFunction("gint")
BuiltInFunction.round = BuiltInFunction("round")
BuiltInFunction.len_str = BuiltInFunction("len_str")
BuiltInFunction.run = BuiltInFunction("run")

    
# CONTEXT(for generating tracebacks)

class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos
		self.symbol_table = None


# SYMBOL TABLE(for storing variables along with their values)

class SymbolTable:
	def __init__(self, parent=None):
		self.symbols = {}
		self.parent = parent

	def get(self, name):
		value = self.symbols.get(name, None)
		if value == None and self.parent:
			return self.parent.get(name)
		return value

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		del self.symbols[name]
                
    
# INTERPRETER(going through the AST and calculating the result)

class Interpreter(object):
    def visit(self,node,context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self,method_name,self.no_visit)
        return method(node,context)
    
    def no_visit(self,node,context):
        raise Exception(f"visit_{type(node).__name__} is not defined")
    
    def visit_NumNode(self,node,context):
        return RTResult().success(Number(node.token.value).set_context(context).set_pos(node.pos_start,node.pos_end))
    

    def visit_StringNode(self,node,context):
        return RTResult().success(String(node.token.value).set_context(context).set_pos(node.pos_start,node.pos_end))
    

    def visit_BinOpNode(self,node,context):
        res = RTResult()
        left = res.register(self.visit(node.left,context))
        if res.should_return(): return res
        right = res.register(self.visit(node.right,context))
        if res.should_return(): return res

        error = None
        
        if node.op.type == PLUS:
            result,error = left.add_to(right)
        elif node.op.type == MINUS:
            result,error = left.sub_by(right)
        elif node.op.type == MUL:
            result,error = left.mul_by(right)
        elif node.op.type == DIV:
            result,error = left.div_by(right)
        elif node.op.type == DEQUAL:
            result,error = left.compare_equal(right)
        elif node.op.type == NOTEQUAL:
            result,error = left.compare_notequal(right)
        elif node.op.type == LT:
            result,error = left.compare_lessthan(right)
        elif node.op.type == GT:
            result,error = left.compare_greaterthan(right)
        elif node.op.type == LTE:
            result,error = left.compare_lte(right)
        elif node.op.type == GTE:
            result,error = left.compare_gte(right)
        elif node.op.type == POW:
            result,error = left.pow_by(right)
        elif node.op.type == COLON:
            result,error = left.colon_by(right)
        elif node.op.type == MODULO:
            result,error = left.modulo_by(right)
        elif node.op.matches(KEYWORD,'AND'):
            result,error = left.and_by(right)
        elif node.op.matches(KEYWORD,'OR'):
            result,error = left.or_by(right)

        if error: 
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start,node.pos_end))


    def visit_UnaryNode(self,node,context):
        res = RTResult()
        val = res.register(self.visit(node.node,context))
        if res.should_return(): return res
        
        error = None

        if node.op.type == MINUS:
            val,error = val.mul_by(Number(-1))
        elif node.op.matches(KEYWORD,'NOT'):
            val,error = val.not_by()

        if error:
            return res.failure(error)
        else:
            return res.success(val.set_pos(node.pos_start,node.pos_end))
        
    
    def visit_VarAccessNode(self,node,context):
        res = RTResult()
        var_name = node.var_token.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RuntimeError(node.pos_start,node.pos_end,f"Var name -> {var_name} is not defined",context))
        
        value = value.copy().set_pos(node.pos_start,node.pos_end).set_context(context)
        return res.success(value)
    
    def visit_VarAssignNode(self,node,context):
        res = RTResult()
        var_name = node.var_token.value
        value = res.register(self.visit(node.val_node,context))
        if res.should_return(): return res

        context.symbol_table.set(var_name,value)
        return res.success(value)
    
    
    def visit_IfNode(self,node,context):
        res = RTResult()

        for condition,expression,return_null in node.cases:
            condition_val = res.register(self.visit(condition,context))
            if res.should_return(): return res

            if condition_val.is_true():
                expression_val = res.register(self.visit(expression,context))
                if res.should_return(): return res

                return res.success(Number.null if return_null else expression_val) 

        if node.else_case:
            expression,return_null = node.else_case
            expression_val = res.register(self.visit(expression,context))
            if res.should_return(): return res

            return res.success(Number.null if return_null else expression_val)
        
        return res.success(Number.null)
    
    def visit_ForNode(self,node,context):
        res = RTResult()
        elements = []

        start_val = res.register(self.visit(node.start_val,context))
        if res.should_return(): return res

        end_val = res.register(self.visit(node.end_val,context))
        if res.should_return(): return res

        if node.stride_val:
            stride_val = res.register(self.visit(node.stride_val,context))
            if res.should_return(): return res
        else:
            stride_val = Number(1)

        i = start_val.value

        if stride_val.value >= 0:
            condition = lambda: i < end_val.value
        else:
            condition = lambda: i > end_val.value

        while condition():
            context.symbol_table.set(node.var_name.value,Number(i))
            i += stride_val.value

            elements.append(res.register(self.visit(node.expression,context)))
            if res.should_return(): return res

        return res.success(Number.null if node.return_null else List(elements).set_pos(node.pos_start,node.pos_end))


    def visit_WhileNode(self,node,context):
        res = RTResult()
        elements = []

        while True:
            condition_val = res.register(self.visit(node.condition,context))
            if res.should_return(): return res

            if not condition_val.is_true(): break

            val = res.register(self.visit(node.expression,context))
            if res.should_return(): return res
            elements.append(val)

        return res.success(Number.null if node.return_null else List(elements).set_pos(node.pos_start,node.pos_end).set_context(context))
    

    def visit_ListNode(self,node,context):
        res = RTResult()
        elements = []

        for element in node.elements:
            elements.append(res.register(self.visit(element,context)))
            if res.should_return(): return res

        return res.success(List(elements).set_context(context).set_pos(node.pos_start,node.pos_end))
    

    def visit_FuncDefNode(self,node,context):
        res = RTResult()

        func_name = node.var_name.value if node.var_name else None
        expression = node.expression
        args = [arg.value for arg in node.args]
        func_val = Function(func_name,expression,args,node.auto_return).set_context(context).set_pos(node.pos_start,node.pos_end)

        if node.var_name:
            context.symbol_table.set(func_name,func_val)

        return res.success(func_val)
    

    def visit_CallFuncNode(self,node,context):
        res = RTResult()
        args = []

        val_tocall = res.register(self.visit(node.node_tocall,context))
        if res.should_return(): return res
        val_tocall = val_tocall.copy().set_pos(node.pos_start,node.pos_end)

        for arg_node in node.args_nodes:
            args.append(res.register(self.visit(arg_node,context)))
            if res.should_return(): return res

        return_val = res.register(val_tocall.execute(args))
        if res.should_return(): return res
        return_val = return_val.copy().set_pos(node.pos_start,node.pos_end).set_context(context)

        return res.success(return_val)
    

    def visit_ReturnNode(self,node,context):
        res = RTResult()

        if node.node_to_return:
            val = res.register(self.visit(node.node_to_return,context))
            if res.should_return(): return res
        else:
            val = Number.null

        return res.success_return(val)


# SETTING SOME VALES IN A GLOBAL SYMBOL TABLE

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)    
global_symbol_table.set("PRINT",BuiltInFunction.print)
global_symbol_table.set("INPUT",BuiltInFunction.input)
global_symbol_table.set("INTINPUT",BuiltInFunction.int_input)
global_symbol_table.set("CLEAR",BuiltInFunction.clear)
global_symbol_table.set("ISNUM",BuiltInFunction.is_num)
global_symbol_table.set("ISSTR",BuiltInFunction.is_str)
global_symbol_table.set("ISLIST",BuiltInFunction.is_list)
global_symbol_table.set("ISFUNC",BuiltInFunction.is_func)
global_symbol_table.set("NUM",BuiltInFunction.num)
global_symbol_table.set("STR",BuiltInFunction.str)
global_symbol_table.set("LEN",BuiltInFunction.len)
global_symbol_table.set("GINT",BuiltInFunction.gint)
global_symbol_table.set("ROUND",BuiltInFunction.round)
global_symbol_table.set("LENSTR",BuiltInFunction.len_str)
global_symbol_table.set("RUN",BuiltInFunction.run)



def run(fname,text):
    lexer = Lexer(fname,text)
    tokens,error = lexer.next_token()
        
    if error: return None,error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None,ast.error

    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node,context)

    return result.value,result.error

