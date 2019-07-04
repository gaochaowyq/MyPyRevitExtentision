import rpw
from interperator import *
from pyrevit import DB

class CustomInterpreter(Interpreter):
    def __init__(self,NodeVisitor):
        super(CustomInterpreter,self).__init__(NodeVisitor)
        self.param_id = DB.ElementId(DB.BuiltInParameter.UNIFORMAT_CODE)

    def visit_BinOp(self, node):
        if node.op.type == PLUS:

            leftset=set(self.visit(node.left))
            rightset=set(self.visit(node.right))
            result=leftset.union(rightset)
            return list(result)
        elif node.op.type == DIV:
            return self.visit(node.left) +'well'+ self.visit(node.right)

    def visit_Assemblycode(self, node):
        parameter_filter = rpw.db.ParameterFilter(self.param_id, begins=node.value)
        collector = rpw.db.Collector(parameter_filter=parameter_filter, is_type=False).get_elements(
            wrapped=True)
        return collector

