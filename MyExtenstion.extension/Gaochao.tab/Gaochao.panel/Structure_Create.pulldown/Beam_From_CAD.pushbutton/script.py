# -*- coding: utf-8 -*-
__doc__="根据导入的CAD绘制结构梁"
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
# Import RevitNodes
clr.AddReference("RevitAPI")
import Autodesk
#from Autodesk.Revit.DB.Events import *
#from Autodesk.Revit.DB import *
from math import *
clr.AddReference("RevitNodes")
import Revit
#clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

# Import Revit elements
# Import DocumentManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
# Import ToProtoType, ToRevitType geometry conversion extension methods

import rpw
from rpw import DB,db,UI
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList

from  Helper import *
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
Picked= uidoc.Selection.PickObject(UI.Selection.ObjectType.Element)
PickedElementId=Picked.ElementId


Picked_Selection=db.Element.from_id(PickedElementId)
#信息输入部分
Framing_types = rpw.db.Collector(of_category='OST_StructuralFraming', is_type=True).get_elements(wrapped=False)

Framing_type_options = {t.FamilyName+DB.Element.Name.GetValue(t): t for t in Framing_types}

Level_type=db.Collector(of_category='Levels', is_type=False).get_elements(wrapped=False)
Level_type_options = {DB.Element.Name.GetValue(t): t for t in Level_type}
	


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
Offset=MmToFeet(float(Value['Offset']))

#

def Draw_LinesfromPoints(Points):
	pass
	
def _ConvertRevitCurves(xcrv):
	if str(xcrv.GetType()) != "Autodesk.Revit.DB.PolyLine":	
		rtn=xcrv.ToProtoType()
	else:
		pt=[]
		lines=[]
		points=xcrv.GetCoordinates()
		for abc in points:
			pt.append(abc.ToPoint())
		rtn=Polygon.ByPoints(pt)
		rtn=[Line.ByStartPointEndPoint(i.StartPoint,i.EndPoint) for i in PolyCurve.Explode(rtn)]
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
		CovertedLine=_ConvertRevitCurves(crv)
		if isinstance(CovertedLine,list):
			for i in CovertedLine:
				CRX.append((i))
		else:
			CRX.append(_ConvertRevitCurves(crv))
		CRV.append(crv)		
		LAY.append(lay)
		CLR.append(ccc.Green)
	
#OUT = [CRV, CRX, LAY, CLR]
OUT=CRX


LayedSelection=[]
for c,l in zip(CRX,LAY):
	if l==LayerName:
		LayedSelection.append(c)

class LineToBeam:
	def __init__(self,Line1,Line2):
		self.Line1=Line1
		self.Line2=Line2

	def Par(self):
		vec1=Vector.Normalized(self.Line1.Direction)
		vec2=Vector.Normalized(self.Line2.Direction)
		self.num=vec1.X*vec2.Y-vec2.X*vec1.Y
		self.distance=Line.DistanceTo(self.Line1,self.Line2)
		dot=Vector.Dot(vec1,vec2)
		#print(self.num,self.distance,dot)
		if self.num==0  and 50<=self.distance<=400 and dot>=0 :
			return [self.Line1,self.Line2]
		elif self.num==0 and 50 <= self.distance <= 400 and dot<=0 :
			return [Line.Reverse(self.Line1), self.Line2]
		else:
			return False
	def MidLine(self):
		parLine=self.Par()
		if parLine !=False:
			startPoint1s=[i.StartPoint for i in parLine]
			endPoint1s = [i.EndPoint for i in parLine]

			startMidP=Line.PointAtParameter(Line.ByStartPointEndPoint(startPoint1s[0],startPoint1s[1]),0.5)
			endtMidP = Line.PointAtParameter(Line.ByStartPointEndPoint(endPoint1s[0], endPoint1s[1]), 0.5)

			newline=Line.ByStartPointEndPoint(startMidP,endtMidP)
			return newline.ToRevitType(False)
		else:
			pass






testLine=LayedSelection

@rpw.db.Transaction.ensure('CreateBeam')
def CreateBeam(Curves,FamilySymbol,Level,StructureType):
	for i in Curves:
		c=doc.Create.NewFamilyInstance(i,FamilySymbol,Level,StructureType)
		WrpedElement=db.Element(c)
		WrpedElement.parameters['Start Level Offset']=Offset
		WrpedElement.parameters['End Level Offset']=Offset
		print(WrpedElement)
Curve=List_Flat(testLine)

StructuralType=DB.Structure.StructuralType.Beam


Linelist1=[i for i in OUT]
Linelist2=[i for i in OUT]
result=[]
for i in Linelist1:
	Linelist1.remove(i)
	for j in Linelist2:
		par=LineToBeam(i,j)
		out=par.MidLine()
		if out==False or out==None:
			pass
		else:
			print(out)
			result.append(out)
			Linelist2.remove(j)
			break
c=CreateBeam(result,FamilyName,Level,StructuralType)
print(result)

	


		
		






	