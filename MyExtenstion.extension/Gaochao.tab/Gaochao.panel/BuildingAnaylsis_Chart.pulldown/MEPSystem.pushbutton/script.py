# -*- encoding: utf-8 -*-
__doc__="设置构件价格"
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
	

picked = revit.pick_element()




