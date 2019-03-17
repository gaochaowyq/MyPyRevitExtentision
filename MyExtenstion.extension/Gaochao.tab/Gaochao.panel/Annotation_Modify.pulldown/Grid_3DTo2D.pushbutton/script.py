# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import rpw
from rpw import revit, DB, UI,db,doc
#from System.Collections.Generic import List
#import json
#from scriptutils import this_script
#from scriptutils.userinput import CommandSwitchWindow
#import subprocess as sp
#Change Selected Grid From 3D to 2D

#selection = rpw.ui.Selection().elements

#Grid=selection[0]
#Grid= rpw.db.Element(Grid).parameters.all

#print(Grid)

#Change Grid buble visibility
selection = rpw.ui.Selection()

Grid=selection
endpoint=DB.DatumEnds.End0
startpoint=DB.DatumEnds.End1
CurrentView=doc.ActiveView
DatumExtentType2D=DB.DatumExtentType.ViewSpecific 
@rpw.db.Transaction.ensure('Hide_Grid_Bubble')
def DatumExtentType3DTo2D(_Grid,points,CurrentView):
	for i in points:		
		_Grid.SetDatumExtentType(i,CurrentView,DatumExtentType2D)




for i in Grid:
	DatumExtentType3DTo2D(i,[endpoint,startpoint],CurrentView)
	print("Good")



