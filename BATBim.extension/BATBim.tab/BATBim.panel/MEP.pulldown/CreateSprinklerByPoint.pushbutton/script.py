# -*- coding: utf-8 -*-
__doc__="根据点创建地漏"
from pyrevit import forms ,DB,UI,_HostApplication,revit
from RhinoToRevit import RhinoToRevit as RhToRe

import rpw
from rpw import db
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList
import csv

from  Helper import *
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
hostapp = _HostApplication()
print(hostapp.app.Language)
if hostapp.app.Language.ToString()=="English_USA":
    ParameterName=LG_EUN()
elif hostapp.app.Language.ToString()=="Chinese_Simplified":
    ParameterName = LG_CHS()


finlename=forms.pick_file(file_ext='csv', files_filter='', init_dir='', restore_dir=True, multi_file=False, unc_paths=False)

points=[]

with open(finlename) as f:
    reader = csv.reader(f)
    for i in reader:
        try:
            point=DB.XYZ(CovertToFeet(float(i[0])),CovertToFeet(float(i[1])),CovertToFeet(float(i[2])))
            points.append(point)
        except Exception as e:
            print(e)

PipeAccessoriesFamilyType = rpw.db.Collector(of_category='OST_PipeAccessory', is_type=True).get_elements(wrapped=False)



PipeAccessoriesFamilyType_options = {t.FamilyName+";"+t.Parameter[DB.BuiltInParameter.SYMBOL_NAME_PARAM].AsString(): t for t in PipeAccessoriesFamilyType}
components = [
Label('族类型'),
ComboBox('FamilySymbol', PipeAccessoriesFamilyType_options),

Button('确定')

]

form = FlexForm('结构', components)
form.show()
Value=form.values
PipeAccessoriesType=Value["FamilySymbol"]

@rpw.db.Transaction.ensure('Create Drain')
def CreatePipeAccessoriesByPoint(XYZ,FamilySymbol):
    print(XYZ)
    doc.Create.NewFamilyInstance(XYZ,FamilySymbol,DB.Structure.StructuralType.NonStructural)
    print("Created")


for i in points:
    CreatePipeAccessoriesByPoint(i,PipeAccessoriesType)







