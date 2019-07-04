from rpw.extras.rhino import Rhino as rc
from pyrevit import DB as _DB
from  Helper import *

def rhPointToPoint(rhPoint):
	rhPointX = rhPoint.X
	rhPointY = rhPoint.Y
	rhPointZ = rhPoint.Z
	return _DB.XYZ(CovertToFeet(rhPointX),CovertToFeet(rhPointY),CovertToFeet(rhPointZ))

def rhLineToLine(rhCurve):
	try:
		dsStartPoint = rhPointToPoint(rhCurve.From)
		dsEndPoint = rhPointToPoint(rhCurve.To)
	except:
		dsStartPoint = rhPointToPoint(rhCurve.PointAtStart)
		dsEndPoint = rhPointToPoint(rhCurve.PointAtEnd)
		pass
	return _DB.Line.CreateBound(dsStartPoint,dsEndPoint)