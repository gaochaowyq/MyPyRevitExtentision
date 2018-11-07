# -*- encoding: utf-8 -*-
__doc__="evry"
import os
import traceback
import  sys
import rpw
import pyrevit
from rpw import db,doc
from pyrevit import revit,DB,UI,forms,HOST_APP
import System
from System.Collections.Generic import List
from pyrevit.framework import Stopwatch
	

MEPSystem= revit.get_selection().first


ConnectorManager=MEPSystem.ConnectorManager.Connectors
for i in ConnectorManager:
    print(i)




