# -*- coding: utf-8 -*-
__doc__="将Rhino中的Mesh 导入 Revit 中"
from rpw.extras.rhino import Rhino as rc
from pyrevit import forms ,DB,UI,_HostApplication,revit
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


#RhToRe.rhMeshToMesh(1)

#Read Rhino File
finlename=forms.pick_file(file_ext='3dm', files_filter='', init_dir='', restore_dir=True, multi_file=False, unc_paths=False)
Materials = rpw.db.Collector(of_category='OST_Materials', is_type=False).get_elements(wrapped=False)
Materials_options = {t.Name: t for t in Materials}
#信息输入部分
components = [
Label('材质'),
ComboBox('Material', Materials_options),
Label('Rhino图层'),
TextBox('Layer', Text="Default"),
Button('确定')

]
form = FlexForm('结构', components)
form.show()
Value=form.values

Mat=Value['Material'].Id


RhinoFile=rc.FileIO.File3dm.Read(finlename)
def GetOBjectByLayer(RehinoFile,LayerName):
	Objects=RehinoFile.Objects.FindByLayer(LayerName)
	return Objects
RhinoOBject=GetOBjectByLayer(RhinoFile,Value['Layer'])
Mesh=None
for i in RhinoOBject:
	Mesh=i.Geometry


#NewLine=[RhToRe.rhLineToLine(i.Geometry) for i in RhinoOBject]

@rpw.db.Transaction.ensure('CreateBeam')
def CreateBeam(GeometricalObjects):
	ds = DB.DirectShape.CreateElement(doc, DB.ElementId(DB.BuiltInCategory.OST_GenericModel))
	ds.ApplicationId = "Application id"
	ds.ApplicationDataId = "Geometry object id"

	ds.SetShape(GeometricalObjects)
	print("CoverSionWell")
CreateBeam(RhToRe.rhMeshToMesh(Mesh,Mat))

	


		
		






	