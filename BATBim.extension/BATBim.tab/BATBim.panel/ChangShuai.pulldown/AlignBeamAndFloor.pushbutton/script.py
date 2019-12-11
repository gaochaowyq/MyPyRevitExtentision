# -*- coding: utf-8 -*-
__doc__="链接墙体与梁"
import rpw
from rpw import db
from pyrevit import revit, DB, HOST_APP, UI,_HostApplication
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList,select_file
from Helper import LG_EUN,LG_CHS,CovertToFeet

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

GenericCategory = rpw.db.Collector(of_category='OST_GenericModel', is_type=True).get_elements(wrapped=False)


Framing_type_options = {t.FamilyName : t for t in GenericCategory}

components = [

	Label('构件名称'),
	ComboBox('FamilyName', Framing_type_options),

	Button('确定')

]
form = FlexForm('结构', components)
form.show()

Value = form.values

AnnonationType = Value['FamilyName']

for i in beam:
	startP= BAT_Beam(i).MoveToFloor(Floor)

	with db.Transaction('Move Beam To Floor'):
		instance = DB.AdaptiveComponentInstanceUtils.CreateAdaptiveComponentInstance(doc, AnnonationType)
		placePointIds = DB.AdaptiveComponentInstanceUtils.GetInstancePlacementPointElementRefIds(instance)
		instanceWraped = db.Element(instance)

		point = doc.GetElement(placePointIds[0])
		point.Position = startP[1]














