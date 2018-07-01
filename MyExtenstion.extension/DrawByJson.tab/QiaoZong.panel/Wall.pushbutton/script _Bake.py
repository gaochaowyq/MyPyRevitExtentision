# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import time
from threading import Timer  
import time  
import rpw
from rpw import revit, db, ui,DB,UI,doc
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button
import json
from JsonReader import *
from System.Collections.Generic import List
_filename=rpw.ui.forms.select_file('json(*.json)|*.json')
Filename=_filename

#doc = __revit__.ActiveUIDocument.Document
level = db.Collector(of_category='Levels', is_type=False, where=lambda x: x.parameters['Name'] == 'Level 1')[0]


@rpw.db.Transaction.ensure('_WallCreate')
def CreateWallByStartAndEndPoint(start,end,level):

	startpoint=DB.XYZ(start[0],start[2],start[1])
	endpoint=DB.XYZ(end[0],end[2],end[1])
	Wall_curves = List[DB.Curve]()



	Line=DB.Line.CreateBound(startpoint,endpoint)
	Wall_curves.Add(Line)

	DB.Wall.Create(doc,Line,level.Id,False)



mm=Input(Filename)
walls=[]
for i in mm.GetWalls():
	if i.startswith( 'wall' ):
		ccc=Wall(mm.GetWalls()[i],Filename)
		walls.append(ccc)
for i in walls:
	c=i.startpoint()
	b=i.endpoint()
	print(c)
	print(b)

	CreateWallByStartAndEndPoint(c, b, level)


	print("done")


	


		
		






	