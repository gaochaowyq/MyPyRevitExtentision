# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import  sys
import rpw
import pyrevit
from rpw import db,doc
from pyrevit import revit,DB,UI,forms,HOST_APP
import System
from System.Collections.Generic import List
from pyrevit.framework import Stopwatch

def OffsetLines(Lines,Distance):
    CurveLoop = DB.CurveLoop.Create(Lines)
    NewCurve = DB.CurveLoop.CreateViaOffset(CurveLoop, CovertToFeet(Distance), DB.XYZ(0, 0, 1))
    result=[]
    for i in NewCurve.GetCurveLoopIterator():
        result.append(i)
    return result
def EdgeArrayArrayToList(EdgeArray):
    _List=List[DB.Curve]()
    for i in EdgeArray:
        for c in i:
            _List.Add(c.AsCurve())
    return _List
picked = revit.pick_face()

#for i in picked.get_Geometry(DB.Options ()):
	#for c in i.GetInstanceGeometry():
	#	print(c)
#	c=i

class BAT_Room:
    def __init__(self,Room):
        self.Room=Room
        self.WrapedRoom=db.Element(self.Room)
        self.RoomLevelId=self.Room.Level.Id
        self.RoomLevel = self.Room.Level
    @property
    def RoomName(self):
        p=DB.BuiltInParameter.ROOM_NAME
        Name=self.Room.get_Parameter(p).AsString()
        return Name
    @property
    def RoomHeight(self):
        p = DB.BuiltInParameter.ROOM_HEIGHT
        try:
            Heigth = self.Room.get_Parameter(p).AsDouble()
            print("{RoomName}房间高度为{Height}".format(RoomName=Room.RoomName, Height=Heigth))
            return Heigth
        except Exception as e:
            print("{Room}不能获取房间高度：{Problem}".format(Room=self.RoomName, Problem=e))
    @property
    def RoomBase(self):
        RoomBaseOffset = self.Room.get_Parameter(DB.BuiltInParameter.ROOM_LOWER_OFFSET).AsInteger()
        return RoomBaseOffset
    @property
    def WallFinishType(self):
        try:
            WallFinishName=self.WrapedRoom.parameters['Wall Finish'].value
            param_id = DB.ElementId(DB.BuiltInParameter.SYMBOL_NAME_PARAM)
            parameter_filter = db.ParameterFilter(param_id, equals=WallFinishName)
            WallType = db.Collector(of_category='OST_Walls', parameter_filter=parameter_filter,
                                    is_type=True).get_first()

            return WallType

        except Exception as e:
            print("{roomname} is not set WallFinishType,We use Default Wall Type defaultType".format(roomname=self.RoomName))
        finally:
            defaultWallTypeId =doc.GetDefaultElementTypeId(DB.ElementTypeGroup.WallType)
            WallType=doc.GetElement(defaultWallTypeId)
            return WallType
    @property
    def FloorFinishType(self):
        try:
            WallFinishName=self.Room.get_Parameter(DB.BuiltInParameter.ROOM_FINISH_FLOOR)
            param_id = DB.ElementId(DB.BuiltInParameter.SYMBOL_NAME_PARAM)
            parameter_filter = db.ParameterFilter(param_id, equals=WallFinishName.AsString())
            FloorType = db.Collector(of_category='OST_Floors', parameter_filter=parameter_filter,
                                    is_type=True).get_first(wrapped=False)
            return FloorType

        except Exception as e:
            print("{Room}不能获取建筑楼面类型：{Problem}".format(Room=self.RoomName, Problem=e))

    @property
    def CeilingFinishType(self):
        try:
            WallFinishName=self.Room.get_Parameter(DB.BuiltInParameter.ROOM_FINISH_CEILING)
            param_id = DB.ElementId(DB.BuiltInParameter.SYMBOL_NAME_PARAM)
            parameter_filter = db.ParameterFilter(param_id, equals=WallFinishName.AsString())
            CeilingType = db.Collector(of_category='OST_Ceilings', parameter_filter=parameter_filter,
                                    is_type=True).get_first(wrapped=False)

            return CeilingType
        except Exception as e:
            print("{Room}不能获取吊顶类型：{Problem}".format(Room=self.RoomName,Problem=e))

    @property
    def WallFinishTypeId(self):
        try:
            return  self.WallFinishType.Id
        except Exception as e:
            print("{Room}不能获取墙面类型ID：{Problem}".format(Room=self.RoomName, Problem=e))
    def RoomBoundary(self):
        room_boundary_options = DB.SpatialElementBoundaryOptions()
        room_boundary = self.Room.GetBoundarySegments(room_boundary_options)
        Index=[]

        Length=[]
        for i in room_boundary:
            CurveLoop = DB.CurveLoop.Create([j.GetCurve() for j in i])
            Length.append(CurveLoop.GetExactLength())
        newLength=sorted(Length)
        _room_boundary=[room_boundary[Length.index(i)] for i in newLength]

        return _room_boundary

    def RoomFaceWall(self):
        room_SpatialElementGeometry=DB.SpatialElementGeometryCalculator(doc).CalculateSpatialElementGeometry(self.Room)
        RoomFace=room_SpatialElementGeometry.GetGeometry().Faces
        edgeLoop = []
        edgeNormal = []
        _WallId=[]

        for i in RoomFace:
            SpatialElementGeometryResults = room_SpatialElementGeometry.GetBoundaryFaceInfo(i)

            if len(SpatialElementGeometryResults)>0:
                if SpatialElementGeometryResults[0].SubfaceType==DB.SubfaceType.Side:
                    surface=SpatialElementGeometryResults[0].GetBoundingElementFace()
                    WallId=SpatialElementGeometryResults[0].SpatialBoundaryElement.HostElementId
                    _edgeLoop=EdgeArrayArrayToList(surface.EdgeLoops)

                    _FaceNormal=surface.FaceNormal
                    edgeLoop.append(_edgeLoop)
                    edgeNormal.append(_FaceNormal)
                    _WallId.append(WallId)
        return [edgeLoop,edgeNormal,_WallId]
    def RoomSolid(self):
        room_SpatialElementGeometry=DB.SpatialElementGeometryCalculator(doc).CalculateSpatialElementGeometry(self.Room)
        solid=room_SpatialElementGeometry.GetGeometry()
        return  solid


    def ParaForMakeWall(self):
        Wall_Surface = List[DB.Curve]()
        Aj_WallId = List[DB.ElementId]()
        for boundary_segment, Room_Aj_WallId in zip(self.Offseted_RoomBoundary()[0], self.Offseted_RoomBoundary()[1]):
            try:
                Aj_WallId.Add(Room_Aj_WallId)
                #Wall_curves.Add(boundary_segment)  # 2015, dep 2016
            except AttributeError:
                #Wall_curves.Add(boundary_segment)  # 2017
                pass
        return [Wall_Surface,Aj_WallId]

    def MakeWall(self):
        @rpw.db.Transaction.ensure('Make Wall')
        def make_wall():
            wallfaces=self.RoomFaceWall()
            for l,n,w in zip(wallfaces[0],wallfaces[1],wallfaces[2]):

                transform=DB.Transform.CreateTranslation(self.WallFinishType.Width/2*(n))
                newLines=List[DB.Curve]()
                for i in l:
                    newLines.Add(i.CreateTransformed(transform))


                NewWall=DB.Wall.Create(doc, newLines,self.WallFinishTypeId,self.RoomLevelId, None)
                NewWall.get_Parameter(DB.BuiltInParameter.WALL_ATTR_ROOM_BOUNDING).Set(0)
                OldWall = doc.GetElement(w)
                DB.JoinGeometryUtils.JoinGeometry(doc, NewWall, OldWall)




        make_wall()


    def MakeFloor(self):
        @rpw.db.Transaction.ensure('MakeFloor')
        def make_floor():
            Floor_CurveArray = DB.CurveArray()
            for boundary_segment in self.RoomBoundary()[0]:
                Floor_CurveArray.Append(boundary_segment.GetCurve())
                #Floor_CurveArray.Append(Wall_curves)
            FloorType =self.FloorFinishType
            level =self.RoomLevel

            _doc = pyrevit._HostApplication(__revit__).doc.Create
            try:
                self.NewFloor=_doc.NewFloor(Floor_CurveArray,FloorType,level,None)
                self.NewFloor.get_Parameter(DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM).Set(self.RoomBase)
                print("{RoomName}建筑楼板被创建".format(RoomName=self.RoomName))
            except Exception as e:
                self.NewFloor=None
                print("{RoomName}建筑楼板未能被创建:{Problem}".format(RoomName=Room.RoomName, Problem=e.__traceback__))
        @rpw.db.Transaction.ensure('MakeFloor')
        def make_floor_Open(Floor):
            _doc = HOST_APP.doc.Create
            boundary=[]
            BoundaryArea=[i for i in self.RoomBoundary()]
            for i in range(0,len(self.RoomBoundary())):
                if i!=0:
                    boundary.append(self.RoomBoundary()[i])
            for boundary_segment in boundary:
                Open_CurveArray = DB.CurveArray()
                for i in boundary_segment:
                    Open_CurveArray.Append(i.GetCurve())
                try:
                    _doc.NewOpening(Floor, Open_CurveArray, True)
                    print("OpeningCreated")
                except Exception as e:
                    print(e)
        make_floor()
        if self.NewFloor!=None:
            make_floor_Open(self.NewFloor)


###############################################
    def MakeCeiling(self):
        @rpw.db.Transaction.ensure('MakeFloor')
        def make_ceiling():

            Wall_curves =List[DB.Curve]()
            for boundary_segment in self.Offseted_RoomBoundary():
                try:
                    Wall_curves.Add(boundary_segment)       # 2015, dep 2016
                except AttributeError:
                    Wall_curves.Add(boundary_segment)  # 2017
            CeilingType =self.CeilingFinishType
            level =self.RoomLevel
            Floor_CurveArray=DB.CurveArray()
            for i in Wall_curves:
                Floor_CurveArray.Append(i)
            _doc = pyrevit._HostApplication(__revit__).doc.Create

            _doc.NewFloor(Floor_CurveArray,CeilingType,level,None)
        try:
            make_ceiling()
            print("{RoomName} 吊顶被创建".format(RoomName=Room.RoomName))
        except Exception as e:
            print(e)
            print("{RoomName} 吊顶未被创建".format(RoomName=Room.RoomName))

    def MakeSolid(self):
        solid=self.RoomSolid()
        new= List[DB.GeometryObject]()
        new.Add(solid)
        categoryId = DB.ElementId(DB.BuiltInCategory.OST_GenericModel)
        with revit.Transaction("CreateElement"):
            ds = DB.DirectShape.CreateElement(doc, categoryId)
            ds.SetShape(new)
            ds.Name = "MyShape"

# by TessellatedShapeBuilder
def OffsetWallSurface(Face,Distance):
    mesh=Face.Triangulate()
    #Index=mesh.Triangle
    Vertices=mesh.Vertices
    materialId=Face.MaterialElementId


    Normal=Face.ComputeNormal(DB.UV(0, 0)).Normalize()

    trans=DB.Transform.CreateTranslation(Normal*Distance)
    Vertices=[trans.OfPoint(i) for i in Vertices]
    builder = DB.TessellatedShapeBuilder()
    loopVertices = List[DB.XYZ]()
    builder.OpenConnectedFaceSet(True)
    for i in range(mesh.NumTriangles):
        triangle=mesh.Triangle[i]
        loopVertices.Add(Vertices[triangle.Index[0]])
        loopVertices.Add(Vertices[triangle.Index[1]])
        loopVertices.Add(Vertices[triangle.Index[2]])

        builder.AddFace(DB.TessellatedFace(loopVertices, materialId))
        loopVertices.Clear()

    builder.CloseConnectedFaceSet()
    builder.Target = DB.TessellatedShapeBuilderTarget.AnyGeometry
    builder.Fallback = DB.TessellatedShapeBuilderFallback.Mesh
    builder.Build()

    result = builder.GetBuildResult()

    return  result

# by BRepBuilder
def OffsetWallSurface_BRep(Face,Distance):
    mesh=Face.Triangulate()
    #Index=mesh.Triangle
    Vertices=mesh.Vertices
    materialId=Face.MaterialElementId


    Normal=Face.ComputeNormal(DB.UV(0, 0)).Normalize()

    trans=DB.Transform.CreateTranslation(Normal*Distance)
    Vertices=[trans.OfPoint(i) for i in Vertices]
    #Naming convention for faces and edges: we assume that x is to the left and pointing down, y is horizontal and pointing to the right, z is up
    brepBuilder = DB.BRepBuilder(DB.BRepType.Solid)

    #The surfaces of the four faces.
    basis = DB.Frame(DB.XYZ(50, -100, 0), DB.XYZ(0, 1, 0), DB.XYZ(-1, 0, 0), DB.XYZ(0, 0, 1))
    cylSurf = DB.CylindricalSurface.Create(basis, 50)
    top = DB.Plane.CreateByNormalAndOrigin(DB.XYZ(0, 0, 1), DB.XYZ(0, 0, 100))
    bottom = DB.Plane.CreateByNormalAndOrigin(DB.XYZ(0, 0, 1), DB.XYZ(0, 0, 0))

    #Add the four faces
    frontCylFaceId = brepBuilder.AddFace(DB.BRepBuilderSurfaceGeometry.Create(cylSurf, None), False)
    backCylFaceId = brepBuilder.AddFace(DB.BRepBuilderSurfaceGeometry.Create(cylSurf, None), False)
    topFaceId = brepBuilder.AddFace(DB.BRepBuilderSurfaceGeometry.Create(top, None), False)
    bottomFaceId = brepBuilder.AddFace(DB.BRepBuilderSurfaceGeometry.Create(bottom, None), True)

    # Geometry for the four semi-circular edges and two vertical linear edges
    frontEdgeBottom = DB.BRepBuilderEdgeGeometry.Create(DB.Arc.Create(DB.XYZ(0, -100, 0), DB.XYZ(100, -100, 0), DB.XYZ(50, -50, 0))) 
    backEdgeBottom = DB.BRepBuilderEdgeGeometry.Create(DB.Arc.Create(DB.XYZ(100, -100, 0), DB.XYZ(0, -100, 0), DB.XYZ(50, -150, 0))) 

    frontEdgeTop = DB.BRepBuilderEdgeGeometry.Create(DB.Arc.Create(DB.XYZ(0, -100, 100), DB.XYZ(100, -100, 100), DB.XYZ(50, -50, 100))) 
    backEdgeTop = DB.BRepBuilderEdgeGeometry.Create(DB.Arc.Create(DB.XYZ(0, -100, 100), DB.XYZ(100, -100, 100), DB.XYZ(50, -150, 100))) 

    linearEdgeFront = DB.BRepBuilderEdgeGeometry.Create(DB.XYZ(100, -100, 0), DB.XYZ(100, -100, 100)) 
    linearEdgeBack = DB.BRepBuilderEdgeGeometry.Create(DB.XYZ(0, -100, 0), DB.XYZ(0, -100, 100)) 

    # Add the six edges
    frontEdgeBottomId = brepBuilder.AddEdge(frontEdgeBottom)
    frontEdgeTopId = brepBuilder.AddEdge(frontEdgeTop)
    linearEdgeFrontId = brepBuilder.AddEdge(linearEdgeFront)
    linearEdgeBackId = brepBuilder.AddEdge(linearEdgeBack)
    backEdgeBottomId = brepBuilder.AddEdge(backEdgeBottom)
    backEdgeTopId = brepBuilder.AddEdge(backEdgeTop)

    # Loops of the four faces
    loopId_Top = brepBuilder.AddLoop(topFaceId)
    loopId_Bottom = brepBuilder.AddLoop(bottomFaceId)
    loopId_Front = brepBuilder.AddLoop(frontCylFaceId)
    loopId_Back = brepBuilder.AddLoop(backCylFaceId)

    # Add coedges for the loop of the front face
    brepBuilder.AddCoEdge(loopId_Front, linearEdgeBackId, False) 
    brepBuilder.AddCoEdge(loopId_Front, frontEdgeTopId, False) 
    brepBuilder.AddCoEdge(loopId_Front, linearEdgeFrontId, True) 
    brepBuilder.AddCoEdge(loopId_Front, frontEdgeBottomId, True) 
    brepBuilder.FinishLoop(loopId_Front) 
    brepBuilder.FinishFace(frontCylFaceId) 

    # Add coedges for the loop of the back face
    brepBuilder.AddCoEdge(loopId_Back, linearEdgeBackId, True) 
    brepBuilder.AddCoEdge(loopId_Back, backEdgeBottomId, True) 
    brepBuilder.AddCoEdge(loopId_Back, linearEdgeFrontId, False) 
    brepBuilder.AddCoEdge(loopId_Back, backEdgeTopId, True) 
    brepBuilder.FinishLoop(loopId_Back) 
    brepBuilder.FinishFace(backCylFaceId) 

    # Add coedges for the loop of the top face
    brepBuilder.AddCoEdge(loopId_Top, backEdgeTopId, False) 
    brepBuilder.AddCoEdge(loopId_Top, frontEdgeTopId, True) 
    brepBuilder.FinishLoop(loopId_Top) 
    brepBuilder.FinishFace(topFaceId) 

    # Add coedges for the loop of the bottom face
    brepBuilder.AddCoEdge(loopId_Bottom, frontEdgeBottomId, False) 
    brepBuilder.AddCoEdge(loopId_Bottom, backEdgeBottomId, False) 
    brepBuilder.FinishLoop(loopId_Bottom) 
    brepBuilder.FinishFace(bottomFaceId) 

    brepBuilder.Finish() 


    return  brepBuilder.GetResult()
solid=OffsetWallSurface_BRep(picked,1)
new=List[DB.GeometryObject]()
#for i in picked:
#    result=  OffsetWallSurface(i,0.1)
#    for c in result.GetGeometricalObjects():
#        new.Add(c)
new.Add(solid)
categoryId =DB.ElementId(DB.BuiltInCategory.OST_GenericModel)
with revit.Transaction("CreateElement"):
    ds = DB.DirectShape.CreateElement(doc, categoryId)
    ds.SetShape(new)
    ds.Name = "MyShape"
