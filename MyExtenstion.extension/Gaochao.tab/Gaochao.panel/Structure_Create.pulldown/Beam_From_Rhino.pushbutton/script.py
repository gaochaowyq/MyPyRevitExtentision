# -*- coding: utf-8 -*-
__doc__="根据导入的CAD绘制结构梁"
from rpw.extras.rhino import Rhino as rc
from pyrevit import forms ,DB,UI,_HostApplication
from RhinoToRevit import RhinoToRevit as RhToRe
import rpw
from rpw import db
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList

from  Helper import *
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
hostapp = _HostApplication(__revit__)
print(hostapp.app.Language)
if hostapp.app.Language.ToString()=="English_USA":
	ParameterName=LG_EUN()
elif hostapp.app.Language.ToString()=="Chinese_Simplified":
	ParameterName = LG_CHS()



#Read Rhino File
finlename=forms.pick_file(file_ext='3dm', files_filter='', init_dir='', restore_dir=True, multi_file=False, unc_paths=False)





#信息输入部分
Framing_types = rpw.db.Collector(of_category='OST_StructuralFraming', is_type=True).get_elements(wrapped=False)



Framing_type_options = {t.FamilyName+";"+t.Parameter[DB.BuiltInParameter.SYMBOL_NAME_PARAM].AsString(): t for t in Framing_types}

print(Framing_type_options)

Level_type=db.Collector(of_category='Levels', is_type=False).get_elements(wrapped=False)
Level_type_options = {t.Name: t for t in Level_type}
	


components = [
Label('构件名称'),
ComboBox('FamilyName', Framing_type_options),
Label('标高'),
ComboBox('Level', Level_type_options),
Label('偏移标高'),
TextBox('Offset', Text="0"),
Label('Rhino图层'),
TextBox('Layer', Text="First"),
Button('确定')

]
form = FlexForm('结构', components)
form.show()
Value=form.values



RhinoFile=rc.FileIO.File3dm.Read(finlename)
def GetOBjectByLayer(RehinoFile,LayerName):
	Objects=RehinoFile.Objects.FindByLayer(LayerName)
	return Objects
RhinoOBject=GetOBjectByLayer(RhinoFile,Value['Layer'])
NewLine=[RhToRe.rhLineToLine(i.Geometry) for i in RhinoOBject]

FamilyName=Value['FamilyName']
Level=Value['Level']
Offset=float(Value['Offset'])

@rpw.db.Transaction.ensure('CreateBeam')
def CreateBeam(Curves,FamilySymbol,Level,StructureType):
	for i in Curves:
		c=doc.Create.NewFamilyInstance(i,FamilySymbol,Level,StructureType)
		DB.Structure.StructuralFramingUtils.DisallowJoinAtEnd(c,0)
		DB.Structure.StructuralFramingUtils.DisallowJoinAtEnd(c, 1)
		WrpedElement=db.Element(c)
		WrpedElement.parameters[ParameterName.BEAM_Start_Extension]=CovertToFeet(-12.5)
		WrpedElement.parameters[ParameterName.BEAM_End_Extension]=CovertToFeet(-12.5)

		WrpedElement.parameters[ParameterName.BEAM_z_Justification] = CovertToFeet(Offset)
		print(WrpedElement)

StructuralType=DB.Structure.StructuralType.Beam


c=CreateBeam(NewLine,FamilyName,Level,StructuralType)

	


		
		






	