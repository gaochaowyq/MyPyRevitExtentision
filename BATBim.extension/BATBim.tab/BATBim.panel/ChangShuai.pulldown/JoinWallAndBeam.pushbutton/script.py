# -*- coding: utf-8 -*-
__doc__="链接墙体与梁"
from pyrevit.framework import List
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList
import rpw
from rpw import db
from pyrevit import revit, DB,UI
from CSharp import FunctionHelper
from  Helper import *


curview = revit.active_view
curdoc=revit.doc
#picked=revit.pick_element()
options=DB.Options()
categoryId =DB.ElementId(DB.BuiltInCategory.OST_GenericModel)
openSymbol = rpw.db.Collector(of_category='OST_GenericModel', is_type=True).get_elements(wrapped=False)



openTypeOptions = {t.FamilyName + ";" + t.Parameter[DB.BuiltInParameter.SYMBOL_NAME_PARAM].AsString(): t for t in
                        openSymbol}


#Level_type = db.Collector(of_category='Levels', is_type=False).get_elements(wrapped=False)
#Level_type_options = {t.Name: t for t in Level_type}

components = [
    Label('构件名称'),
    ComboBox('FamilyName', openTypeOptions),
    Button('确定')
]
form = FlexForm('开洞', components)
form.show()
Value = form.values


openSymbol=Value["FamilyName"]


def GetElementSolid(Element):
    Solids=[]
    geo=Element.get_Geometry(options)
    for i in geo:
        if type(i) != DB.GeometryInstance:
            if i.Volume!=0:
                Solids.append(i)
    return Solids
def GetFamilyInstanceSolid(Element):
    Solids=[]
    geo=Element.get_Geometry(options)
    for i in geo:
        if type(i)== DB.GeometryInstance:
            c=i.GetInstanceGeometry()
            for d in c:
                if d.Volume != 0:
                    Solids.append(d)
        elif type(i)== DB.Solid:
            if i.Volume!=0:
                Solids.append(i)
    return Solids




walls = db.Collector(of_class='Wall',is_not_type=True).get_elements(wrapped=False)

"""
with db.Transaction('ChageWall'):
    for w in walls:
        for b in beams:
            try:
                wSolid=GetElementSolid(w)[0]
                wBox=wSolid.GetBoundingBox()
                bSolid = GetElementSolid(b)[0]

                result=DB.BooleanOperationsUtils.ExecuteBooleanOperation (wSolid,bSolid,DB.BooleanOperationsType.Intersect)
                if result.Volume>0.0001:
                    DB.JoinGeometryUtils.JoinGeometry(curdoc,w,b)

            except:
                print("Id{}或Id{}有问题请查看".format(w.Id,b.Id))



@rpw.db.Transaction.ensure('JoinWallAndConcreteFraming')
def _JoinWallAndConcreteFraming(walls):
    for w in walls:
        try:
            #wSolid=GetElementSolid(w)[0]
            wBox=w.BoundingBox[curview]
            #ds = DB.DirectShape.CreateElement(curdoc, categoryId)
            #ListGeometry=List[DB.GeometryObject]()
            #ListGeometry.Add(wBox)
            #ds.AppendShape(ListGeometry)
            #print("Createed")
            outLine=DB.Outline(wBox.Min,wBox.Max)

            boundingBoxIntersectsFilter=DB.BoundingBoxIntersectsFilter(outLine)

            collector=DB.FilteredElementCollector(curdoc)

            elements = collector.WherePasses(boundingBoxIntersectsFilter).OfCategory(DB.BuiltInCategory.OST_StructuralFraming).ToElements()
            for i in elements:
                bSolid=GetFamilyInstanceSolid(i)
                wSolid=GetElementSolid(w)
                if len(bSolid)!=0:
                    result=DB.BooleanOperationsUtils.ExecuteBooleanOperation (wSolid[0],bSolid[0],DB.BooleanOperationsType.Intersect)
                    if result.Volume>0.0001:
                        DB.JoinGeometryUtils.JoinGeometry(curdoc,w,i)
                        print("ID{}与ID{}连接成功".format(w.Id,i.Id))
                else:
                    print("ID{}没有实体".format(i.Id))

        except Exception as e:
            print("ID:{}墙体有问题".format(w.Id))
"""

#TODO:
def ElementIntersectWith(Elements,BuiltInCategory):
    """
    :param Elements，Any Elments for test which is Interset with:
           BuiltInCategory，Which Category Elements be Interseted
    :return [[Intersections],[Intersections],[Intersections]]:
    """
    Final=[]
    for w in Elements:
        wBox = w.BoundingBox[curview]
        outLine = DB.Outline(wBox.Min, wBox.Max)
        boundingBoxIntersectsFilter = DB.BoundingBoxIntersectsFilter(outLine)
        collector = DB.FilteredElementCollector(curdoc)
        elements = collector.WherePasses(boundingBoxIntersectsFilter).OfCategory(
            BuiltInCategory).ToElements()
        wSolid = GetElementSolid(w)
        bFinal=[]
        for i in elements:
            bSolid = GetFamilyInstanceSolid(i)
            if len(bSolid) != 0:
                result = DB.BooleanOperationsUtils.ExecuteBooleanOperation(wSolid[0], bSolid[0],
                                                                           DB.BooleanOperationsType.Intersect)
                if result.Volume > 0.0001:
                    #DB.JoinGeometryUtils.JoinGeometry(curdoc, w, i)
                    bFinal.append(i)
                    print("ID{}与ID{}相交".format(w.Id, i.Id))
            else:
                print("ID{}没有实体".format(i.Id))
        Final.append(bFinal)
    return  Final


#TODO
def CovertCurveToVector(Curve):
    startPoint=Curve.GetEndPoint(0)
    endPoint=Curve.GetEndPoint(1)
    vector=endPoint-startPoint
    return vector.Normalize()

#TODO
def CurveVectorAtPoint(Curve,Point):
    parameter=Curve.Project(Point).Parameter

    vector=Curve.ComputeDerivatives(parameter,False).BasisX
    return vector


def CreateOpenByPointAndDirection(FamilySymbol,Point,Direction,Width,Height,Depth):
    """
    :param FamilySymbol: OpenFimily
    :param Point: IntersectPoint
    :param Direction: Direction Of Opening
    :return: Bool: Created or not
    """
    rotateAngle=DB.XYZ(0,1,0).AngleTo(Direction)
    print(rotateAngle)
    Creation=curdoc.Application.Create
    familyInstanceCreationData=Creation.NewFamilyInstanceCreationData(Point,FamilySymbol,DB.Structure.StructuralType.NonStructural)

    _familyInstanceCreationData=List[familyInstanceCreationData.GetType()]()
    rotateAxis=DB.Line.CreateBound(Point,DB.XYZ(Point.X,Point.Y,Point.Z+10000))
    familyInstanceCreationData.Axis=rotateAxis
    if Direction.X>=0:
        familyInstanceCreationData.RotateAngle=-rotateAngle
    else:
        familyInstanceCreationData.RotateAngle = rotateAngle
    _familyInstanceCreationData.Add(familyInstanceCreationData)
    newElements=curdoc.Create.NewFamilyInstances2(_familyInstanceCreationData)
    for i in newElements:
        wrapedElement=db.Element.from_id(i)
        wrapedElement.parameters["洞口宽度"].value=Width
        wrapedElement.parameters["洞口深度"].value = Depth
        wrapedElement.parameters["洞口高度"].value = Height

    return newElements

@rpw.db.Transaction.ensure('JoinWallAndConcreteFraming')
def JoinWallAndFraming(wall,framings):
    for framing in framings:
        framingType=framing.Symbol.Family.get_Parameter(DB.BuiltInParameter.FAMILY_STRUCT_MATERIAL_TYPE).AsInteger()

        if framingType==1:
            framingLocation=framing.Location
            wallLocation=wall.Location
            if isinstance(framingLocation,DB.LocationCurve):
                # get the curve for wall and framing
                fWCurve=wallLocation.Curve
                fLCurve=framingLocation.Curve
                # get curve Intersection Result
                results = FunctionHelper.BAT_ComputeClosestPoints(fWCurve, fLCurve)[0]

                fWVector=CurveVectorAtPoint(fWCurve,results.XYZPointOnFirstCurve)
                fLVector = CurveVectorAtPoint(fLCurve,results.XYZPointOnSecondCurve)
                dot=fWVector.DotProduct(fLVector)
                Width=framing.Symbol.get_Parameter(DB.BuiltInParameter.STRUCTURAL_SECTION_COMMON_WIDTH).AsDouble()
                Height=framing.Symbol.get_Parameter(DB.BuiltInParameter.STRUCTURAL_SECTION_COMMON_HEIGHT).AsDouble()
                Depth=wall.WallType.get_Parameter(DB.BuiltInParameter.WALL_ATTR_WIDTH_PARAM).AsDouble()
                if -0.99<dot<0.99:
                    createdElements=CreateOpenByPointAndDirection(openSymbol,results.XYZPointOnSecondCurve,fLVector,Width,Height,Depth+1)
                    for i in createdElements:
                        DB.InstanceVoidCutUtils.AddInstanceVoidCut (curdoc,wall,curdoc.GetElement(i) )



                else:
                    #make a open in the all
                    pass



            else:
                print("ID{}Is Point Based FamilyInstance")


        elif framingType==2:
            DB.JoinGeometryUtils.JoinGeometry(curdoc, wall, framing)
        elif framingType==3:
            pass
        elif framingType==4:
            pass



Intersects=ElementIntersectWith(walls,DB.BuiltInCategory.OST_StructuralFraming)

for w,b in zip(walls,Intersects):
    JoinWallAndFraming(w,b)


#print(picked.Symbol.Family.get_Parameter(DB.BuiltInParameter.FAMILY_STRUCT_MATERIAL_TYPE).AsInteger())

#JoinWallAndConcreteFraming(walls)
print("完成所有剪切")








