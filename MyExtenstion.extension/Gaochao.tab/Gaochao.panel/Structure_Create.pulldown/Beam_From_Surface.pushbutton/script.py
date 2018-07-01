# -*- coding: utf-8 -*-
__doc__="更具曲面与垂直线创建结构"
import sys
import clr
import os
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
#The inputs to this node will be stored as a list in the IN variables.
clr.AddReference("RevitNodes")
import Revit


clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

import rpw
from rpw import revit, db, ui,DB,UI
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button, Alert
import json

from MyLib import Helper
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
# 参数输入
components = [
Label('曲面偏移距离'),
TextBox('OffsetDistance', Text="500"),
Label('构件名称'),
TextBox('FamilyName', Text="HB200*100"),
Button('确定')
]
form = FlexForm('根据曲面与垂直线创建结构', components)
form.show()
Value=form.values
OffsetDistance=Value["OffsetDistance"]
FamilyName=Value['FamilyName']
Alert('请选择基础面', title=__doc__)

#pick Surface
Picked= uidoc.Selection.PickObject(UI.Selection.ObjectType.Face,"选择面")
PickedElementId=Picked.ElementId
Picked_Selection=doc.GetElement(PickedElementId)
PickedFaces=Picked_Selection.GetGeometryObjectFromReference(Picked)
# CovertTo Dynamo type
print(PickedFaces)
DS_Face=PickedFaces.ToProtoType()
print(DS_Face)

#Offset Surface

DS_Face_Offset=DS_Face[0].Offset(float(OffsetDistance))

Alert('选择垂直线',title=__doc__)

#Def Filter
class ModleLineFilter(UI.Selection.ISelectionFilter):

	def AllowElement(self,element):
		if (element.Category.Name == "Lines"):
		

			return True
		return False

		
	
fileter=ModleLineFilter()



#pick Lines
Picked= uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element,fileter,"选择多条线")

Lines=[]
for i in Picked:
	PickedElementId=i.ElementId
	Picked_Selection=doc.GetElement(PickedElementId)
	PickedLines=Picked_Selection.GetGeometryObjectFromReference(i).GetEnumerator()
	for c in PickedLines:
		Lines.append(c.ToProtoType())
		
#Extrude All Lines

Extrude_Lines=[]

for i in Lines:
	c=Curve.ExtendEnd(i,-1000)
	c=Curve.ExtendStart(c,-1000)
	_vector=Vector.ZAxis()
	vector=Vector.Scale(_vector,-20000)
	c=Curve.Extrude(c,vector)
	Extrude_Lines.append(c)
	
# Intersect Surface
Intersect_Lines=[]

for i in Extrude_Lines:
	#如果没有交线 退出程序
	c=Surface.Intersect(i,DS_Face_Offset)
	if len(c)==0:
		print("项目没有交线")
	
	startpoint=NurbsCurve.PointAtParameter(c[0],0)
	endpoint=NurbsCurve.PointAtParameter(c[0],1)
	

	c=NurbsCurve.PointsAtEqualSegmentLength(c[0],10)
	newPoints=[]
	for i in c:
		newPoints.append(i)
	
	newPoints.insert(0,startpoint)
	newPoints.append(endpoint)
	

	c=NurbsCurve.ByPoints(newPoints)
	Intersect_Lines.append(c.ToRevitType())

#Picked_Selection=db.Element.from_id(PickedElementId).unwrap()
#信息输入部分


	
	

@rpw.db.Transaction.ensure('CreateBeam')
def CreateBeam(Curves,FamilySymbol,Level,StructureType):
	for i in Curves:
		doc.Create.NewFamilyInstance(i,FamilySymbol,Level,StructureType)
	
	
Level_Roof=db.Collector(of_category='Levels', is_type=False,where=lambda x: x.parameters['Name']=='Roof')[0]
FramingSymbol=db.Collector(of_category='OST_StructuralFraming',is_not_type=False).wrapped_elements
for i in FramingSymbol:
	if i.name==FamilyName:
		FramingSymbol=i.unwrap()
StructuralType=DB.Structure.StructuralType.Beam


c=CreateBeam(Intersect_Lines,FramingSymbol,Level_Roof,StructuralType)
print(Intersect_Lines)
print("绘制完成")

	


		
		






	