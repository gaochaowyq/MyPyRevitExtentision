# -*- coding: utf-8 -*-
__doc__="根据导入的CAD绘制结构梁"
from pyrevit import rhino as rc
from pyrevit import forms ,DB
from RhinoToRevit import RhinoToRevit as RhToRe
import rpw
from rpw import db
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList

from  Helper import *
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document



#Read Rhino File
finlename=forms.pick_file(file_ext='3dm', files_filter='', init_dir='', restore_dir=True, multi_file=False, unc_paths=False)
RhinoFile=rc.FileIO.File3dm.Read(finlename)
def GetOBjectByLayer(RehinoFile,LayerName):
	Objects=RehinoFile.Objects.FindByLayer(LayerName)
	return Objects
RhinoOBject=GetOBjectByLayer(RhinoFile,"Default")


NewLine=[RhToRe.rhLineToLine(i.Geometry) for i in RhinoOBject]



#信息输入部分
Framing_types = rpw.db.Collector(of_category='OST_StructuralFraming', is_type=True).get_elements(wrapped=False)

Framing_type_options = {t.FamilyName: t for t in Framing_types}

Level_type=db.Collector(of_category='Levels', is_type=False).get_elements(wrapped=False)
Level_type_options = {t.Name: t for t in Level_type}
	


components = [
Label('输入图层名称'),
TextBox('图层名称', Text="SM-PLAN-B4B3B2$0$S-BEAM-DASH"),
Label('构件名称'),
ComboBox('FamilyName', Framing_type_options),
Label('标高'),
ComboBox('Level', Level_type_options),
Label('偏移标高'),
TextBox('Offset', Text="-300"),
Button('确定')

]
form = FlexForm('结构', components)
form.show()
Value=form.values

LayerName=Value['图层名称']
FamilyName=Value['FamilyName']
Level=Value['Level']
Offset=CovertToFeet(float(Value['Offset']))

@rpw.db.Transaction.ensure('CreateBeam')
def CreateBeam(Curves,FamilySymbol,Level,StructureType):
	for i in Curves:
		c=doc.Create.NewFamilyInstance(i,FamilySymbol,Level,StructureType)
		WrpedElement=db.Element(c)
		WrpedElement.parameters['Start Level Offset']=Offset
		WrpedElement.parameters['End Level Offset']=Offset
		print(WrpedElement)

StructuralType=DB.Structure.StructuralType.Beam


c=CreateBeam(NewLine,FamilyName,Level,StructuralType)

	


		
		






	