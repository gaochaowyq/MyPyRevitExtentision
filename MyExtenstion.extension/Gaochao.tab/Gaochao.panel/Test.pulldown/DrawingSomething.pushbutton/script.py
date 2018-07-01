# -*- coding: utf-8 -*-
__doc__ = 'Join All Floor and Framing'
import rpw
from rpw import revit, DB, UI,db,doc
from System.Collections.Generic import List

from scriptutils.userinput import CommandSwitchWindow


#Framing= rpw.Collector(of_category='Wall').wrapped_elements
#View=rpw.View3D.collect(where=lambda x: x.Name='Whatever')
Floor= db.Collector(of_category='OST_Floors',is_not_type=True).wrapped_elements
Framing=db.Collector(of_category='OST_StructuralFraming',is_not_type=True).wrapped_elements
def UnwrapElementInList(List):
	NewList=[]
	for i in List:
		NewList.append(i.unwrap())
	return NewList
		
UnWrappednFraming=UnwrapElementInList(Framing)
		
	
Options=DB.Options()
Options.ComputeReferences =True
solids=[]
for i in UnWrappednFraming:
	#print(i.get_BoundingBox(doc.ActiveView).Min)
	GeometryElement=i.get_Geometry(Options)
	enum1=GeometryElement.GetEnumerator()
	enum1.MoveNext()
	geo2=enum1.Current.GetInstanceGeometry()	
	for f in geo2:
		if f!=None:
			solids.append(f)
print(solids)
print(len(solids))

c=solids[2].Faces.GetEnumerator()
while c.MoveNext():
	print(c.Current.Area)


#for i in Floor:
#	print(i.get_BoundingBox(doc.ActiveView))

#	print(i.get_BoundingBox(doc.ActiveView))
