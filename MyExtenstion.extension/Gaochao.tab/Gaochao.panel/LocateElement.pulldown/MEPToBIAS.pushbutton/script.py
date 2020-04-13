# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import pyrevit
import clr
import rpw
from rpw import db,doc
from pyrevit import revit,DB,UI,forms,HOST_APP
import System
from System.Collections.Generic import List
from pyrevit.framework import Stopwatch
##############################################################################

OST_MEPSYSTEM=DB.Category.GetCategory(doc,DB.BuiltInCategory.OST_DuctSystem)
##############################################################################
title="MEPToBIAS"
description="将MEP输出为Curve Based Json"

MEPSystemInst = rpw.db.Collector(of_category='OST_DuctSystem', is_type=False).get_elements(wrapped=False)

MEPSystemInstElements=MEPSystemInst[0].DuctNetwork

print(MEPSystemInstElements)

def GetConnectors(e):

	connectors =[]
	if isinstance(e,DB.FamilyInstance):
		m = e.MEPModel
		if (None!=m and  None != m.ConnectorManager):
			connectors = m.ConnectorManager.Connectors

	elif isinstance(e,DB.Electrical.Wire):
		connectors = e.ConnectorManager.Connectors
	else:
		print(
			#e.GetType().IsSubclassOf(DB.MEPCurve)),
			"expected all candidate connector provider "
			+ "elements to be either family instances or "
			+ "derived from MEPCurve")

	if isinstance(e,DB.MEPCurve):
		connectors =e.ConnectorManager.Connectors
	return connectors



for i in MEPSystemInstElements:
	print(GetConnectors(i) )











