# -*- coding: utf-8 -*-
__doc__="反向物体选择"
from pyrevit.framework import List
from pyrevit import forms
from pyrevit import revit, DB
import rpw






selection = rpw.ui.Selection()
selectedid=[i.Id for i in selection ]
curview = revit.activeview


elements = DB.FilteredElementCollector(revit.doc, curview.Id)\
			 .WhereElementIsNotElementType()\
			 .ToElementIds()

element_to_isolate = []
for elid in elements:
	el = revit.doc.GetElement(elid)
	if not el.ViewSpecific:  # and not isinstance(el, DB.Dimension):
		element_to_isolate.append(elid)



for i in selectedid:
	for j in element_to_isolate:
		if i==j:
			element_to_isolate.remove(j)
element_to_isolate = List[DB.ElementId](element_to_isolate)
newelement=[revit.doc.GetElement(i) for i in element_to_isolate]

revit.get_selection().set_to(newelement)




