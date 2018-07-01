# -*- coding: utf-8 -*-
__doc__="创建"
from pyrevit.framework import List
from pyrevit import forms
from pyrevit import revit, DB
from pyrevit import HOST_APP
import rpw
from rpw import db
from rpw.extras.rhino import Rhino as rc
import Helper
from collections import Counter
rg=rc.Geometry


curview = revit.activeview
curdoc=revit.doc

pickpipes=revit.pick_elements()


class BAT_ST_Beam:
    def __init__(self,framing):
        self.framing=framing

    def BaseLevel(self):
        BaseLevel = self.framing.get_Parameter(DB.BuiltInParameter.STRUCTURAL_ELEVATION_AT_BOTTOM).AsValueString()
        return float(BaseLevel)

    def distance(self):
        TopLevel=self.framing.get_Parameter(DB.BuiltInParameter.STRUCTURAL_ELEVATION_AT_TOP).AsValueString()
        BaseLevel = self.framing.get_Parameter(DB.BuiltInParameter.STRUCTURAL_ELEVATION_AT_BOTTOM).AsValueString()
        distance=float(TopLevel)-float(BaseLevel)
        return distance
    def BaseLine_Rhino(self):
        pipePoint1 =self.framing.Location.Curve.GetEndPoint(0)
        pipePoint2 =self.framing.Location.Curve.GetEndPoint(1)
        pipe_pt1 = rc.Geometry.Point3d(pipePoint1.X, pipePoint1.Y, pipePoint1.Z)
        pipe_pt2 = rc.Geometry.Point3d(pipePoint2.X, pipePoint2.Y, pipePoint2.Z)
        line1 = rc.Geometry.Line(pipe_pt1, pipe_pt2)
        return line1

class BAT_MEP_Pipe:
    def __init__(self,Pipe):
        self.Pipe=Pipe

    def TopLevel(self):
        BaseLevel=self.Pipe.get_Parameter(DB.BuiltInParameter.RBS_PIPE_INVERT_ELEVATION).AsValueString()
        Diameter = self.Pipe.get_Parameter(DB.BuiltInParameter.RBS_PIPE_OUTER_DIAMETER).AsDouble()
        #TopLevel=BaseLevel-Diameter
        return float(BaseLevel)+float(Helper.CovertToMM(Diameter))
    def BaseLine_Rhino(self):
        pipePoint1 =self.Pipe.Location.Curve.GetEndPoint(0)
        pipePoint2 =self.Pipe.Location.Curve.GetEndPoint(1)
        pipe_pt1 = rc.Geometry.Point3d(pipePoint1.X, pipePoint1.Y, pipePoint1.Z)
        pipe_pt2 = rc.Geometry.Point3d(pipePoint2.X, pipePoint2.Y, pipePoint2.Z)
        line1 = rc.Geometry.Line(pipe_pt1, pipe_pt2)
        return line1
    def isHorizional(self):
        baseline=self.BaseLine_Rhino()
        point1 = rg.Line.PointAt(baseline, 0)
        point2 = rg.Line.PointAt(baseline, 1)
        if point1.Z>point2.Z:
            toppoint=point1
            basepoint=point2
        else:
            toppoint=point2
            basepoint = point1
        vector = rg.Vector3d(basepoint.X - toppoint.X, basepoint.Y -toppoint.Y, basepoint.Z - toppoint.Z)
        vector.Unitize()
        print(vector)
        if -1 <= vector.Z <= -0.9:

            return False
        else:
            return True



class BAT_MEP_Duct:
    def __init__(self,Duct):
        self.Duct=Duct

    def TopLevel(self):
        TopElevation=self.Duct.get_Parameter(DB.BuiltInParameter.RBS_DUCT_TOP_ELEVATION).AsValueString()
        return float(TopElevation)
    def BaseLine_Rhino(self):
        pipePoint1 =self.Duct.Location.Curve.GetEndPoint(0)
        pipePoint2 =self.Duct.Location.Curve.GetEndPoint(1)
        pipe_pt1 = rc.Geometry.Point3d(pipePoint1.X, pipePoint1.Y, pipePoint1.Z)
        pipe_pt2 = rc.Geometry.Point3d(pipePoint2.X, pipePoint2.Y, pipePoint2.Z)
        line1 = rc.Geometry.Line(pipe_pt1, pipe_pt2)
        return line1

#c=BAT_ST_Beam(pickbeam)
#Only Solve The RelationShape Of Two Line
class Line_Line_Intersection(object):
    def __init__(self,Line1,Line2):
        self.Line1=Line1
        self.Line2=Line2

    @property
    def isIntersect(self):
        list = rc.Geometry.Intersect.Intersection.LineLine(self.Line1, self.Line2)
        if list[0] and 0<=list[1]<=1 and 0<=list[2]<=1:
            return True
        else:
            return False
    def Distance(self):
        list = rc.Geometry.Intersect.Intersection.LineLine(self.Line1, self.Line2)
        point1 = rc.Geometry.Line.PointAt(self.Line1, list[1])
        point2 = rc.Geometry.Line.PointAt(self.Line2, list[2])
        d = rg.Point3d.DistanceTo(point1, point2)

        return Helper.CovertToMM(d)

class Pipe_optimization_With_Framing:
    def __init__(self,pipe,beam,DisToBeam=0):
        self.pipe=BAT_MEP_Pipe(pipe)
        self.beam=BAT_ST_Beam(beam)
        self.DistToBeam = DisToBeam
        self.distance=self.beam.BaseLevel()-self.pipe.TopLevel()-self.DistToBeam
        self.isReferecenLineIntersect=Line_Line_Intersection(self.pipe.BaseLine_Rhino(),self.beam.BaseLine_Rhino()).isIntersect


    @property
    def isIntersect(self):
        _isIntersect=self.isReferecenLineIntersect
        if self.distance<=0 and _isIntersect:
            return True
        else:
            return False
    @property
    def isSuit(self):
        _isIntersect=self.isReferecenLineIntersect
        print(self.distance)
        if self.distance==0 and _isIntersect:
            return True
        else:
            return False

    @rpw.db.Transaction.ensure('Move_Pipe')
    def Pipe_Move(self,Distance):
        Pipe_Offset= self.pipe.Pipe.get_Parameter(DB.BuiltInParameter.RBS_OFFSET_PARAM).AsDouble()
        self.pipe.Pipe.get_Parameter(DB.BuiltInParameter.RBS_OFFSET_PARAM).Set(Pipe_Offset+Helper.MMToFeet(Distance))
        print("Successfuly Moved")


    def Optimization(self):
        if not self.isSuit:
            print(self.distance)
            self.Pipe_Move(self.distance)
            return True
        else:
            print("No Need To Optimization")
            return False

class MEP_optimization_With_Framing:
    def __init__(self,MEP,beam,DisToBeam=0):
        self.MEP=MEP
        if type(self.MEP)==DB.Plumbing.Pipe:
            self.pipe=BAT_MEP_Pipe(self.MEP)
        elif type(self.MEP)==DB.Mechanical.Duct:
            self.pipe=BAT_MEP_Duct(self.MEP)

        self.beam=BAT_ST_Beam(beam)
        self.DistToBeam = DisToBeam
        self.distance=self.beam.BaseLevel()-self.pipe.TopLevel()-self.DistToBeam
        self.isReferecenLineIntersect=Line_Line_Intersection(self.pipe.BaseLine_Rhino(),self.beam.BaseLine_Rhino()).isIntersect


    @property
    def isIntersect(self):
        _isIntersect=self.isReferecenLineIntersect
        if self.distance<=0 and _isIntersect:
            return True
        else:
            return False
    @property
    def isSuit(self):
        _isIntersect=self.isReferecenLineIntersect
        print(self.distance)
        if self.distance==0 and _isIntersect:
            return True
        else:
            return False

    @rpw.db.Transaction.ensure('Move_Object')
    def Pipe_Move(self,Distance):
        Pipe_Offset= self.MEP.get_Parameter(DB.BuiltInParameter.RBS_OFFSET_PARAM).AsDouble()
        self.MEP.get_Parameter(DB.BuiltInParameter.RBS_OFFSET_PARAM).Set(Pipe_Offset+Helper.MMToFeet(Distance))
        print("Successfuly Moved")


    def Optimization(self):
        if not self.isSuit:
            print(self.distance)
            self.Pipe_Move(self.distance)
            return True
        else:
            print("No Need To Optimization")
            return False

# Optimization Pipe With The Same Level Framing
class Pipe_optimization:
    def __init__(self,pipe,DisToBeam=0):
        self.pipe=pipe
        Level=pipe.LevelId
        self.DisToBeam=DisToBeam
        self.beams= db.Collector(of_category='OST_StructuralFraming', level=Level, is_not_type=True)

    def SelectAllIntersectBeam(self):
        allbeam = self.beams.get_elements()

        intersetdbeam = []
        for i in allbeam:
            c = Pipe_optimization_With_Framing(self.pipe, i)
            if c.isReferecenLineIntersect:
                intersetdbeam.append(i)
        return intersetdbeam

    def MostLowsetBeam(self):
        Beams = self.SelectAllIntersectBeam()
        if Beams:
            BaseLevels = [BAT_ST_Beam(i).BaseLevel() for i in Beams]
            most = Counter(BaseLevels).most_common(1)
            index = [i for i, x in enumerate(BaseLevels) if x == most[0][0]][0]
            return Beams[index]
        else:
            print("No Intersect Beam")

    def Optimization(self):
        _Beam = self.MostLowsetBeam()
        try:
            c = Pipe_optimization_With_Framing(self.pipe, _Beam,DisToBeam=self.DisToBeam).Optimization()
        except:
            pass

class MEP_optimization:
    def __init__(self,pipe,DisToBeam=0):
        self.pipe=pipe
        Level=pipe.LevelId
        self.DisToBeam=DisToBeam
        self.beams= db.Collector(of_category='OST_StructuralFraming', level=Level, is_not_type=True)

    def SelectAllIntersectBeam(self):
        allbeam = self.beams.get_elements()

        intersetdbeam = []
        for i in allbeam:
            c = MEP_optimization_With_Framing(self.pipe, i)
            if c.isReferecenLineIntersect:
                intersetdbeam.append(i)
        return intersetdbeam

    def MostLowsetBeam(self):
        Beams = self.SelectAllIntersectBeam()
        if Beams:
            BaseLevels = [BAT_ST_Beam(i).BaseLevel() for i in Beams]
            most = Counter(BaseLevels).most_common(1)
            index = [i for i, x in enumerate(BaseLevels) if x == most[0][0]][0]
            return Beams[index]
        else:
            print("No Intersect Beam")

    def Optimization(self):
        _Beam = self.MostLowsetBeam()
        try:
            MEP_optimization_With_Framing(self.pipe, _Beam,DisToBeam=self.DisToBeam).Optimization()
        except:
            pass
class Pipes_optimization:
    def __init__(self,pipes,DisToBeam=0):
        self.pipes=pipes
        self.DisToBeam=DisToBeam
    def Optimization(self):
        if type(self.pipes)==list:
            for i in self.pipes:
                c=Pipe_optimization(i,self.DisToBeam).Optimization()
                print("{}被成功优化".format(i.Name))
        else:
            c = Pipe_optimization(self.pipes,self.DisToBeam).Optimization()
            print("{}被成功优化".format(self.pipes.Name))

class MEPS_optimization:
    def __init__(self,pipes,DisToBeam=0):
        self.pipes=pipes
        self.DisToBeam=DisToBeam
    def Optimization(self):
        if type(self.pipes)==list:
            for i in self.pipes:
                c=MEP_optimization(i,self.DisToBeam).Optimization()
                print("{}被成功优化".format(i.Name))
        else:
            c = MEP_optimization(self.pipes,self.DisToBeam).Optimization()
            print("{}被成功优化".format(self.pipes.Name))




def GetAllHPipe():
    HP=[]
    for i in pickpipes:
        new=BAT_MEP_Pipe(i)
        if new.isHorizional():
            HP.append(i)
    return HP

print(GetAllHPipe())


LL=MEPS_optimization(GetAllHPipe(),DisToBeam=50).Optimization()

























