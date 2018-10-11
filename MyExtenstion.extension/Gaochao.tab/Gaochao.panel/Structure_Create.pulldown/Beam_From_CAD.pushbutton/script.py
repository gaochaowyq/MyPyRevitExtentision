# -*- coding: utf-8 -*-
__doc__ = "返回选择物体的类型"
import rpw
from rpw import db, doc
from pyrevit import revit, DB, HOST_APP, UI
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList


picked = revit.pick_element()
DOC = doc
Structure = []
Framing_types = rpw.db.Collector(of_category='OST_StructuralFraming', is_type=True).get_elements(wrapped=False)

Framing_type_options = {t.FamilyName + DB.Element.Name.GetValue(t): t for t in Framing_types}

Level_type = db.Collector(of_category='Levels', is_type=False).get_elements(wrapped=False)
Level_type_options = {DB.Element.Name.GetValue(t): t for t in Level_type}

components = [
    Label('输入图层名称'),
    TextBox('图层名称', Text="0"),
    Label('构件名称'),
    ComboBox('FamilyName', Framing_type_options),
    Label('标高'),
    ComboBox('Level', Level_type_options),
    Label('偏移标高'),

]
form = FlexForm('结构', components)
form.show()
Value = form.values
LayerName = Value['图层名称']
FamilyName = Value['FamilyName']
Level = Value['Level']
StructuralType=DB.Structure.StructuralType.Beam
for abc in picked.get_Geometry(DB.Options()):
    for crv in abc.GetInstanceGeometry():
        if str(crv.GetType()) == "Autodesk.Revit.DB.NurbSpline":
            Structure.append(crv)



@rpw.db.Transaction.ensure('CreateBeam')
def CreateBeam(Curves, FamilySymbol, Level, StructureType):
    for i in Curves:
        c = doc.Create.NewFamilyInstance(i, FamilySymbol, Level, StructureType)
        WrpedElement = db.Element(c)
        print(WrpedElement)
CreateBeam(Structure, FamilyName, Level, StructuralType)


	


		
		






	