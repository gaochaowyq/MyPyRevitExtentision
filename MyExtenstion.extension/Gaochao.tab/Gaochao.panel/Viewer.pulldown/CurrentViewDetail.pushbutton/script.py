# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import rpw
from rpw import revit, DB, UI,db,doc,uidoc
from System.Collections.Generic import List
import json
CurrentView=doc.ActiveView
uiviews = uidoc.GetOpenUIViews()
selection = rpw.ui.Selection().get_elements(wrapped=False)
BoundingBox=selection[0].get_BoundingBox(CurrentView)
Points=[BoundingBox.Max,BoundingBox.Min]

for i in uiviews:
	if i.ViewId==CurrentView.Id:
		i.ZoomAndCenterRectangle(Points[0], Points[1])



		