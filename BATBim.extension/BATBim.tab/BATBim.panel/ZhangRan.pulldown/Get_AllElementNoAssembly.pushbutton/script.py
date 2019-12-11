# -*- coding: utf-8 -*-
__doc__="反向物体选择"
from pyrevit.framework import List
from pyrevit import forms
from pyrevit import revit, DB
from rpw import  UI,db,doc
import rpw



def lasteCreated():
	curview = revit.activeview


	elements = DB.FilteredElementCollector(revit.doc,curview.Id)\
				 .WhereElementIsNotElementType()\
				 .ToElementIds()
	
	element_to_isolate = []
	Empty=[]
	for elid in elements:
		el = revit.doc.GetElement(elid)
		try:
			WrapedElement=db.Element(el).type
			if WrapedElement.unwrap().get_Parameter(DB.BuiltInParameter.UNIFORMAT_CODE).AsString()=='':
				print(WrapedElement.Id)
		except:
			pass		
		try:
			if WrapedElement.unwrap().get_Parameter(DB.BuiltInParameter.UNIFORMAT_CODE).AsString()=="":
				Empty.append(WrapedElement)
				#print(WrapedElement.unwrap().get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString())
		except:
			pass
        if len(Empty)==0:
			print("所有构件都包含了Assembly Code")
                                
		

	#element_to_id = [i.IntegerValue for i in element_to_isolate]

	#element_to_id.sort()


	#selected=element_to_id[-1]

	#revit.get_selection().set_to(selected)

lasteCreated()

