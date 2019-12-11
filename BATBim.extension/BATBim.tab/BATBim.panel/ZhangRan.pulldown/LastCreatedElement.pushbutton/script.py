# -*- coding: utf-8 -*-
__doc__="反向物体选择"
from pyrevit.framework import List
from pyrevit import forms
from pyrevit import revit, DB
from rpw import  UI,db,doc
import rpw



def lasteCreated():
	curview = revit.activeview


	elements = DB.FilteredElementCollector(revit.doc, curview.Id)\
				 .WhereElementIsNotElementType()\
				 .ToElementIds()

	element_to_isolate = []
	for elid in elements:
		el = revit.doc.GetElement(elid)
		if not el.ViewSpecific:  # and not isinstance(el, DB.Dimension):
			element_to_isolate.append(elid)

	element_to_id = [i.IntegerValue for i in element_to_isolate]

	element_to_id.sort()


	selected=element_to_id[-1]

	revit.get_selection().set_to(selected)

lasteCreated()

