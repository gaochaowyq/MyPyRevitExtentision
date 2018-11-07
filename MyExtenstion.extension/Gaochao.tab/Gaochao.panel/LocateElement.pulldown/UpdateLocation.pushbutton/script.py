# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import pyrevit
import clr
import rpw
from rpw import db,doc
from pyrevit import revit,DB,UI,forms,HOST_APP
import System
from System.Collections.Generic import List
from pyrevit.framework import Stopwatch
##############################################################################
OST_WALL=DB.Category.GetCategory(doc,DB.BuiltInCategory.OST_Walls)
OST_StructuralColumns=DB.Category.GetCategory(doc,DB.BuiltInCategory.OST_StructuralColumns)
##############################################################################
title="根据Accessmbly筛选构件价格"
description="根据Accessmbly筛选构件价格"
value=rpw.ui.forms.TextInput(title, default=None, description=description, sort=True, exit_on_close=True)
Accessmbly_Code=value




def GetIntersection(line1,line2 ):
	# do As Out
	results =clr.Reference[DB.IntersectionResultArray]()

	result= line1.Intersect(line2, results )

	if result != DB.SetComparisonResult.Overlap:
		print("Input lines did not intersect." )

	if results == None or results.Size != 1 :
		print("Could not extract line intersection point." )

	iResult= results.get_Item(0)

	return iResult.XYZPoint

class GridPoint:
	def __init__(self,Grid1,Grid2):
		self.Grid1=Grid1
		self.Grid2=Grid2
		self.Grid1Name=Grid1.Name
		self.Grid2Name = Grid2.Name
	def InterPoint(self):
		Grid1Line1=self.Grid1.Curve
		Grid1Line2 = self.Grid2.Curve
		Point=GetIntersection(Grid1Line1,Grid1Line2)
		return Point
	def __str__(self):
		return "{grid1}And{grid2}".format(grid1=self.Grid1Name,grid2=self.Grid2Name)
	def __repr__(self):
		return self.__str__()
class Rec:
	# G1 G2 G3 G4 get From GridPoint
	def __init__(self,G1,G2,G3,G4):
		self.G1=G1
		self.G2=G2
		self.G3=G3
		self.G4=G4
		self.p1=G1.InterPoint()
		self.p2=G2.InterPoint()
		self.p3 =G3.InterPoint()
		self.p4 =G4.InterPoint()
	#point DB.XYZ
	def InRec(self,point):
		if point ==None:
			print("No Point Found")
			return False
		X=point.X
		Y=point.Y
		if self.p1.X <=X<=self.p3.X and self.p1.Y<=Y<=self.p2.Y:

			return True
		else:
			return False
	def ReturnString(self):
		return "{V1}~{V2}And{H1}~{H2}".format(V1=self.G1.Grid1Name,V2=self.G3.Grid1Name,H1=self.G1.Grid2Name,H2=self.G2.Grid2Name)

class GetGrid:
	def __init__(self,grids):
		self.grids=grids
		self.SortedGrid=self._SortGrids()
	def _SortGrids(self):
		_GridsName=[i.Name for i in self.grids]
		GridsName = [i.Name for i in self.grids]
		GridsName.sort()
		index=GridsName.index("A")
		Vertical=GridsName[index:]
		Horizonal=GridsName[:index]
		VGrid=[]
		HGrid=[]
		for c in Vertical:
			VGrid.append(self.grids[_GridsName.index(c)])
		for c in Horizonal:
			HGrid.append(self.grids[_GridsName.index(c)])
		return [VGrid,HGrid]
	def CreateRecs(self):
		VGrid=self.SortedGrid[0]
		HGrid = self.SortedGrid[1]
		AllRecs=[]

		for i in range(0,len(VGrid)-1):
			for c in range(0,len(HGrid)-1):
				V1=VGrid[i]
				V2 = VGrid[i+1]
				H1=HGrid[c]
				H2=HGrid[c+1]
				Gp1=GridPoint(H1,V1)
				Gp2 = GridPoint(H1, V2)
				Gp3 = GridPoint(H2, V1)
				Gp4 = GridPoint(H2, V2)
				New=Rec(Gp1,Gp2,Gp3,Gp4)
				AllRecs.append(New)
		return AllRecs




Grids= revit.get_selection().elements

#c=GridPoints(Grids[0],Grids[1])
c=GetGrid(Grids)

rec=c.CreateRecs()


param_id = DB.ElementId(DB.BuiltInParameter.UNIFORMAT_CODE)

parameter_filter = rpw.db.ParameterFilter(param_id, begins=Accessmbly_Code)
collector = rpw.db.Collector(parameter_filter=parameter_filter, is_type=False).get_elements(wrapped=True)

class Element:
	def __init__(self,Element):
		self.Element=Element
		UnwrapElement=Element.unwrap()
		self.Type=UnwrapElement.GetType()
		self.Category=UnwrapElement.Category
		LevelId=UnwrapElement.LevelId

		self.BaseLevel=doc.GetElement(LevelId)
	def LocationPoint(self):
		if self.Element.Location.GetType()==DB.LocationCurve:
			point=self.Element.Location.Curve.Evaluate(0.5,True)
			return point
		elif self.Element.Location.GetType()==DB.LocationPoint:

			return self.Element.Location.Point
	def AbstractLocation(self):

		if self.Category.Name==OST_WALL.Name:

			for c in rec:
				b = c.InRec(self.LocationPoint())
				if b:
					_Grid = c.ReturnString()
					return "{Plan}|{Level}".format(Plan=_Grid, Level=self.BaseLevel.Name)
		elif self.Category.Name==OST_StructuralColumns.Name:
			_Grid=self.Element.unwrap().get_Parameter(DB.BuiltInParameter.COLUMN_LOCATION_MARK).AsString()
			return "{Plan}|{Level}".format(Plan=_Grid, Level=self.BaseLevel.Name)
		else:
			return "The Element is Not Support To Locate"

	def UpdateLocation(self):
		with revit.Transaction("Convert ACIS to FreeFrom"):
			self.Element.parameters['模糊定位']=self.AbstractLocation()






for i in collector:
	El=Element(i)
	El.UpdateLocation()

	print(El.AbstractLocation())











