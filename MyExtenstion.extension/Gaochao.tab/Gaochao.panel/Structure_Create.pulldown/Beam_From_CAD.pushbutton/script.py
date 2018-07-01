# -*- coding: utf-8 -*-
__doc__="根据导入的CAD绘制结构梁"
import sys
import os
from collections import namedtuple
from Autodesk.Revit.DB.Architecture import Room

import rpw
from rpw import doc, uidoc, DB, UI, db, ui
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList
import json

from MyLib import Helper
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document



Picked= uidoc.Selection.PickObject(UI.Selection.ObjectType.Element)
PickedElementId=Picked.ElementId


Picked_Selection=db.Element.from_id(PickedElementId)
#信息输入部分
Framing_types = rpw.db.Collector(of_category='OST_StructuralFraming', is_type=True).elements

Framing_type_options = {t.FamilyName+DB.Element.Name.GetValue(t): t for t in Framing_types}

Level_type=db.Collector(of_category='Levels', is_type=False).elements
Level_type_options = {DB.Element.Name.GetValue(t): t for t in Level_type}
	


components = [
Label('输入图层名称'),
TextBox('图层名称', Text="S-STEL-BEAM"),
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
Offset=Helper.MmToFeet(float(Value['Offset']))

#

def Draw_LinesfromPoints(Points):
	pass
	


def Old_ConvertRevitCurves(xcrv):
	if  str(xcrv.GetType()) != "Autodesk.Revit.DB.PolyLine":
		rtn=xcrv
	else:
		pt = []
		for abc in xcrv.GetCoordinates():
			#print(abc)
			pt.append(abc)
		#for i in range(0,len(pt)-1):
		#	lines.append(DB.Line.CreateBound(pt[i],pt[1+1]));
		#rtn=lines
	return rtn
	
def _ConvertRevitCurves(xcrv):
	if str(xcrv.GetType()) != "Autodesk.Revit.DB.PolyLine":	
		rtn=xcrv
	elif str(xcrv.GetType())=="Autodesk.Revit.DB.PolyLine":
		lines=[]
		points=xcrv.GetCoordinates()
		for i in range(0,len(points)-1):
			try:
				newline=DB.Line.CreateBound(points[i],points[i+1])
			except:
				pass
	
			lines.append(newline)
		rtn=lines		
	else:
		rtn=xcrv
		
	return rtn
		
		
DOC =doc
DWG =Picked_Selection.unwrap()
CRV = []
CRX = []
LAY = []
CLR = []

for abc in DWG.get_Geometry(DB.Options()):
	for crv in abc.GetInstanceGeometry():
		#print(crv.GetType())
		lay = DOC.GetElement(crv.GraphicsStyleId).GraphicsStyleCategory.Name
		ccc = DOC.GetElement(crv.GraphicsStyleId).GraphicsStyleCategory.LineColor
		CRX.append(_ConvertRevitCurves(crv))
		CRV.append(crv)		
		LAY.append(lay)
		CLR.append(ccc.Green)
	
OUT = [CRV, CRX, LAY, CLR]


LayedSelection=[]
for c,l in zip(CRX,LAY):
	if l==LayerName:
		LayedSelection.append(c)


testLine=LayedSelection

@rpw.db.Transaction.ensure('CreateBeam')
def CreateBeam(Curves,FamilySymbol,Level,StructureType):
	for i in Curves:
		c=doc.Create.NewFamilyInstance(i,FamilySymbol,Level,StructureType)
		WrpedElement=db.Element(c)
		WrpedElement.parameters['Start Level Offset']=Offset
		WrpedElement.parameters['End Level Offset']=Offset
		print(WrpedElement)
Curve=Helper.List_Flat(testLine)

StructuralType=DB.Structure.StructuralType.Beam


c=CreateBeam(Curve,FamilyName,Level,StructuralType)
print(c)
print("绘制完成")

	


		
		






	