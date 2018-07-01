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

#Wall Selection
selection = rpw.ui.Selection()

SelectedWall=selection[0]

location=SelectedWall.Location

print(location)


#Wall Divide To Separtpart