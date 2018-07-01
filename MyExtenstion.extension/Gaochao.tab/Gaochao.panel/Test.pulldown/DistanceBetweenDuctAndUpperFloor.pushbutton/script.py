# -*- coding: utf-8 -*-
__doc__="检查当前楼层风管与当前楼层梁的间距"
import rpw
from rpw import revit, DB, UI,db,doc
from System.Collections.Generic import List

from scriptutils.userinput import CommandSwitchWindow




Duct= db.Collector(of_category='OST_DuctCurves',is_not_type=True).wrapped_elements
Framing=db.Collector(of_category='OST_StructuralFraming',is_not_type=True).wrapped_elements

#DuctParameter=Duct[0].parameters.all
def DistanceBetweenFramingAndDuct (Duct,Framing):
	#风管顶部高度
	Duct_Height=Duct.parameters['Top Elevation'].value
	#结构梁底部高度
	Framing_Height=Framing.parameters['Elevation at Bottom'].value
	
	Distance=(Framing_Height-Duct_Height)*304.8
	return Distance
	
def SanJieHangLieShi(List):
	_result=List[0][0]*List[1][1]*List[2][2]+List[0][1]*List[1][2]*List[2][0]+List[0][2]*List[1][0]*List[2][1]-List[0][2]*List[1][1]*List[0][0]-List[0][1]*List[1][0]*List[2][2]-List[0][0]*List[1][2]*List[0][1]
	result=round(_result,1)
	return result
class DuctAndFraming:
	#Family= Wrapped Element
	def __init__(self,Duct,Framing):		
		self.DuctPoint1=Duct.Location.Curve.GetEndPoint(0)
		self.DuctPoint2=Duct.Location.Curve.GetEndPoint(1)
		self.FramingPoint1=Framing.Location.Curve.GetEndPoint(0)
		self.FramingPoint2=Framing.Location.Curve.GetEndPoint(1)
	def TextCorss(self):
		Vector1=self.DuctPoint2-self.DuctPoint1
		Vector2=self.FramingPoint1-self.FramingPoint2
		Vector3=self.FramingPoint1-self.DuctPoint1
		Result=SanJieHangLieShi([Vector1,Vector2,Vector3])
		
		
		
		return Result
		
		
Result=[]
for i in Duct:
	for c in Framing:
		DuctLocationLine=DuctAndFraming(i,c)
		Result.append(DuctLocationLine.TextCorss())

print(Result)
		
	
		

#@rpw.db.Transaction.ensure('Do Something')
#def set_some_parameter(Framing, value):
#    Framing.parameters['Start Level Offset'].value=value
#set_some_parameter(Framing[0],2000)
	 


