# -*- coding: utf-8 -*-
__doc__="将Rhino的实体导入Revit"

from pyrevit import script
from rpw import db
from pyrevit import revit, DB, HOST_APP, UI,_HostApplication,forms
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList,select_file
from Helper import LG_EUN,LG_CHS,CovertToFeet
from System.Collections.Generic import List
import csv
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
hostapp = _HostApplication()
app=__revit__.Application
output = script.get_output()

if hostapp.app.Language.ToString()=="English_USA":
    ParameterName=LG_EUN()
elif hostapp.app.Language.ToString()=="Chinese_Simplified":
    ParameterName = LG_CHS()

#Read Rhino File
allElementsInView=db.Collector(view=doc.ActiveView,is_type=False).get_elements(wrapped=False)

for i in allElementsInView:
    materials=i.GetMaterialIds(False)
    name=i.Name
    materialNames=[]
    """
    if isinstance(i,DB.FamilyInstance):
        type=i.Symbol
        assemblyCode=type.get_Parameter(DB.BuiltInParameter.UNIFORMAT_CODE).AsString()
    else:
        assemblyCode=None
    """
    wrappedElement=db.Element(i)
    try:
        assemblyCode=wrappedElement.type.parameters[ParameterName.UNIFORMAT_CODE].value
    except:
        assemblyCode=None


    for c in materials:
        m=doc.GetElement(c)
        materialNames.append(m.Name)
    if name==None or name=='' or assemblyCode==None or assemblyCode=='':
        if  name=='' or name==None:
            pass
        else:
            output.print_html('<div style="background:red">name:{},assemblyCode:{},materials:{},Id:{}</div>'.format(name,assemblyCode,name,i.Id))

    else:
        print("name:{},assemblyCode{},materials:{}".format(name,assemblyCode,name))






