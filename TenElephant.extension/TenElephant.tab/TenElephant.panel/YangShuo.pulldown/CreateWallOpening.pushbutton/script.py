# -*- coding: utf-8 -*-
__doc__="根据点创建地漏"
from pyrevit import forms ,DB,UI,_HostApplication,revit
from RhinoToRevit import RhinoToRevit as RhToRe
import clr
import rpw
from rpw import db
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList
import csv

from System.Collections.Generic import List
from Element.Elements import BAT_Wall
from  Helper import *
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
hostapp = _HostApplication(__revit__)
print(hostapp.app.Language)
if hostapp.app.Language.ToString()=="English_USA":
    ParameterName=LG_EUN()
elif hostapp.app.Language.ToString()=="Chinese_Simplified":
    ParameterName = LG_CHS()

def FindDuctCurve(duct):

    list =List[DB.XYZ]()

    csi = duct.ConnectorManager.Connectors.ForwardIterator()
    while csi.MoveNext():
        conn = csi.Current
        list.Add(conn.Origin)

    curve = DB.Line.CreateBound(list[0], list[1])
    curve.MakeUnbound()

    return curve


def FindFaceCurve(DuctCurve, WallFace):

    #The intersectionpoint
    intersectionR =clr.Reference[DB.IntersectionResultArray]()
    # Intersection point set
    #SetComparisonResult results
    # Results of Comparison

    results = WallFace.Intersect(DuctCurve, intersectionR)
    intersectionResult =None
    # Intersectioncoordinate
    if DB.SetComparisonResult.Disjoint != results:
        if intersectionR != None:
            if intersectionR.IsEmpty==False:
                intersectionResult = intersectionR.get_Item(0).XYZPoint
            return intersectionResult




walls = db.Collector(of_class='Wall',is_type=False)

pipes = db.Collector(of_category='OST_DuctCurves',is_type=False)


print(pipes[0])


c=FindDuctCurve(pipes[0])
print(c)

FitId=DB.ElementId(203162)
Fit=doc.GetElement(FitId)
LevelId=DB.ElementId(13071)
Level=doc.GetElement(LevelId)
View=doc.ActiveView
StructuralType=DB.Structure.StructuralType.NonStructural
WrapedElement =db.Element.from_id(FitId)
print(Fit)
@rpw.db.Transaction.ensure('Create Drain')
def CreateOpeningForWall(Duct,Wall):

    DuctCurve=FindDuctCurve(Duct)
    WallFace=BAT_Wall(Wall).FindWallFace()

    Inter=FindFaceCurve(DuctCurve,WallFace[0])

    Final = doc.Create.NewFamilyInstance(Inter, Fit.Symbol, StructuralType)
    #picked = revit.pick_element()

    DB.ElementTransformUtils.RotateElement(doc, Final.Id, DB.Line.CreateBound(Inter,Inter.Add(DB.XYZ(0,0,1))), 0)
    #print(Final.HandOrientation)
    #Final.HandOrientation=DB.XYZ(0,0,1)

CreateOpeningForWall(pipes[0],walls[0])







