# -*- coding: utf-8 -*-
__doc__="DepthMap Analysis"
import  sys
import rpw
import pyrevit
from rpw import db,doc
from pyrevit import revit,DB,UI,forms,HOST_APP
import System
from System.Collections.Generic import List
from pyrevit.framework import Stopwatch
from Element.Elements import Room as _Room

class Room (_Room):
    def GetBoundary(self):
        option=DB.SpatialElementBoundaryOptions()
        Boundary=self.Room.GetBoundarySegments(option)

        print(Boundary)




picked = revit.pick_element()

C=Room(picked)
C.GetBoundary()




