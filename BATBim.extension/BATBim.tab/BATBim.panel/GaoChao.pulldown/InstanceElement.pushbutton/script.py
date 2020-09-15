# -*- coding: utf-8 -*-
__doc__="DepthMap Analysis"
import clr
import time
import  sys
import rpw
import pyrevit
from rpw import db,doc,uidoc,ui
from pyrevit import revit,DB,UI,forms,HOST_APP
import System
from System.Collections.Generic import List
from pyrevit.framework import Stopwatch
uiapp = __revit__
######################################
options=DB.Options()
#allWallsInView = DB.FilteredElementCollector(doc, doc.ActiveView.Id).ToElements()

#for i in allElementsInView:
#    print(i)

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
#elementInstance= revit.pick_element()




allColumn = rpw.db.Collector(of_category='OST_StructuralColumns', is_type=False).get_elements(wrapped=False)

allFraming = rpw.db.Collector(of_category='OST_StructuralFraming', is_type=False).get_elements(wrapped=False)

picked=revit.pick_element()
@rpw.db.Transaction.ensure('ResetColumnToInstance')
def ResetColumnToInstance(Element):
    for element in Element:
        try:
            level = doc.GetElement(element.LevelId)

            baseLevel=element.Parameter[DB.BuiltInParameter.FAMILY_BASE_LEVEL_PARAM]
            topLevel=element.Parameter[DB.BuiltInParameter.FAMILY_TOP_LEVEL_PARAM]
            baseOffset=element.Parameter[DB.BuiltInParameter.FAMILY_BASE_LEVEL_OFFSET_PARAM]
            topOffset=element.Parameter[DB.BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM]

            elementLocation = element.Location.Point
            elementSymbol = element.Symbol

            #elementFamily = elementSymbol.Family

            newElementInstance=doc.Create.NewFamilyInstance(elementLocation,elementSymbol,level,DB.Structure.StructuralType.Column)

            newElementInstance.Parameter[DB.BuiltInParameter.FAMILY_BASE_LEVEL_PARAM].Set(baseLevel.AsElementId())
            newElementInstance.Parameter[DB.BuiltInParameter.FAMILY_TOP_LEVEL_PARAM].Set(topLevel.AsElementId())
            newElementInstance.Parameter[DB.BuiltInParameter.FAMILY_BASE_LEVEL_OFFSET_PARAM].Set(baseOffset.AsDouble())
            newElementInstance.Parameter[DB.BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM].Set(topOffset.AsDouble())
            #topOffset.Set(newElementInstance.Id)
            print("ID{}Done".format(element.Id))
            doc.Delete(element.Id)


        except Exception as e:
            print("ID{}Wrong".format(element.Id))
@rpw.db.Transaction.ensure('ResetBeamToInstance')
def ResetBeamToInstance(Element):
    for element in Element:
        try:
            level = doc.GetElement(element.LevelId)

            referenceLevel=element.Parameter[DB.BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM]
            startLevelOffset=element.Parameter[DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION]
            endLevelOffset=element.Parameter[DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION]

            elementLocation = element.Location.Curve
            elementSymbol = element.Symbol

            #elementFamily = elementSymbol.Family

            newElementInstance=doc.Create.NewFamilyInstance(elementLocation,elementSymbol,level,DB.Structure.StructuralType.Beam)

            newElementInstance.Parameter[DB.BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM].Set(referenceLevel.AsElementId())
            newElementInstance.Parameter[DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION].Set(startLevelOffset.AsDouble())
            newElementInstance.Parameter[DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION].Set(endLevelOffset.AsDouble())
            #topOffset.Set(newElementInstance.Id)
            print("ID{}Done".format(element.Id))
            doc.Delete(element.Id)


        except Exception as e:
            print(e)
            print("ID{}Wrong".format(element.Id))

ResetColumnToInstance(allColumn)
#ResetBeamToInstance(allFraming)

#ResetBeamToInstance([picked])
