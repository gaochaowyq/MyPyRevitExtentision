# -*- encoding: utf-8 -*-
import rpw
from rpw import db
from pyrevit import revit, DB, HOST_APP, UI,_HostApplication
from CodeInterperator.AssembyCode_Inter import *
class GetElementsByAssemblyCode(object):
    def __init__(self,AssemblyCode):
        self.param_id = DB.ElementId(DB.BuiltInParameter.UNIFORMAT_CODE)
        self.AssembleCode = AssemblyCode
        #KEYNOTE_PARAM
        self.param_id_Keynote = DB.ElementId(DB.BuiltInParameter.KEYNOTE_PARAM)
    #Return Wrapped Element
    def Elements(self):
        if hasattr(self, 'NotContainAssembleCode'):
            parameter_filter = rpw.db.ParameterFilter(self.param_id, begins=self.AssembleCode,
                                                      not_contains=self.NotContainAssembleCode)
            collector = rpw.db.Collector(parameter_filter=parameter_filter, is_type=False).get_elements(wrapped=True)
        else:
            if isinstance(self.AssembleCode,str):
                lexer=Lexer(self.AssembleCode)
                prase=Parser(lexer)
                interpreter=CustomInterpreter(prase)
                collector=interpreter.interpret()
            else:
                collector=[]
                for i in self.AssembleCode:
                    parameter_filter = rpw.db.ParameterFilter(self.param_id, begins=i)
                    _collector = rpw.db.Collector(parameter_filter=parameter_filter, is_type=False).get_elements(wrapped=True)
                    for i in _collector:
                        collector.append(i)
        return collector