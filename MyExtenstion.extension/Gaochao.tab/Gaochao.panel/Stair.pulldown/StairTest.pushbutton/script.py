# -*- coding: utf-8 -*-
__doc__="分析设计中内墙与外墙的量"
import rpw
from rpw import revit, DB, UI,db,doc
from System.Collections.Generic import List
import json
from scriptutils import this_script
from scriptutils.userinput import CommandSwitchWindow
import subprocess as sp
from pyrevit.coreutils.console import charts
# Global Setting
Options=DB.Options()
Options.ComputeReferences =True
#Get Inside Wall And Outside Wall then show in on the Pin Table


selection = rpw.ui.Selection()

SelectedStair=selection[0]



StairGeometry=SelectedStair.get_Geometry(Options)
enum1=StairGeometry.GetEnumerator()

for i in enum1:
	print(i)
	newenum1=i.GetInstanceGeometry()
	print(newenum1)
	for i in newenum1:
		print(i)

enum1.MoveNext()
#geo2=enum1.Current.GetInstanceGeometry()
print(enum1)

for i in enum1:
	

	print(i)