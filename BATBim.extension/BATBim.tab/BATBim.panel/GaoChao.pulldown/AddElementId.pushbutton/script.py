# -*- coding: utf-8 -*-
__doc__="DepthMap Analysis"
import clr
import time
import  sys
import rpw
import pyrevit
from rpw import db,doc,uidoc
from pyrevit import revit,DB,UI,forms,HOST_APP
import System
from System.Collections.Generic import List
from pyrevit.framework import Stopwatch

######################################

#allElementsInView = DB.FilteredElementCollector(doc, doc.ActiveView.Id).ToElements()

#for i in allElementsInView:
#    print(i)

allElementsInView=db.Collector(view=doc.ActiveView,is_type=False).get_elements(wrapped=True)

with db.Transaction('AddElementId'):

    for i in allElementsInView:
        #print(i.unwrap().Id)
        try:
            i.parameters['ElementId'].value=i.unwrap().Id
        except:
            pass






