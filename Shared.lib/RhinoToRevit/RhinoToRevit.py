from rpw.extras.rhino import Rhino as rc
from System.Collections.Generic import List
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

def rhMeshToMesh(rhMesh,MaterialId):
	"""

	:param rhMesh: MeshObject From Rhino
	:param MaterialId:
	:return:
	"""
	materialId=MaterialId
	loopVertices =List[_DB.XYZ]()
	builder =_DB.TessellatedShapeBuilder()
	builder.OpenConnectedFaceSet(True)

	Vertices=[]
	FaceIndex=[]
	for i in rhMesh.Vertices:
		Vertices.append(rhPointToPoint(i))


	for i in rhMesh.Faces:
		index=[]
		if i.IsTriangle:
			index.append(i.A)
			index.append(i.B)
			index.append(i.C)
		else:
			index.append(i.A)
			index.append(i.B)
			index.append(i.C)
			index.append(i.D)
		FaceIndex.append(index)
	#print(FaceIndex)
	for i in FaceIndex:
		for index in i:
			loopVertices.Add(Vertices[index])

		builder.AddFace(_DB.TessellatedFace(loopVertices, materialId))
		loopVertices.Clear()
	builder.CloseConnectedFaceSet()
	builder.Target = _DB.TessellatedShapeBuilderTarget.Solid
	builder.Fallback = _DB.TessellatedShapeBuilderFallback.Abort
	try:
		builder.Build()
		result = builder.GetBuildResult()
		GeometricalObjects = result.GetGeometricalObjects()
		return GeometricalObjects
	except Exception as e:
		print(e)
		return  None
