# -*- coding: utf-8 -*-
__doc__="链接墙体与梁"
import rpw
from rpw import db
from pyrevit import revit, DB, HOST_APP, UI,_HostApplication
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList,select_file
from Helper import LG_EUN,LG_CHS

from Element.Elements import BAT_Beam,BAT_Floor
import csv
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
hostapp = _HostApplication(__revit__)

if hostapp.app.Language.ToString()=="English_USA":
	ParameterName=LG_EUN()
elif hostapp.app.Language.ToString()=="Chinese_Simplified":
	ParameterName = LG_CHS()
Floor = revit.pick_element()
beam=revit.pick_elements()

for i in beam:
	Beam = BAT_Beam(i).MoveToFloor(Floor)












