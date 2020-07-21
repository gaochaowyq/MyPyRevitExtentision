# -*- coding: utf-8 -*-
__doc__ = "将梁附着在楼板底部"
import rpw
import clr
from pyrevit import forms
from rpw import db, doc
from pyrevit import revit, DB, HOST_APP, UI
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button,SelectFromList


floor = revit.pick_element()

beams=revit.pick_elements()

#out_sUV = clr.Reference[DB.UV]()
#out_eUV = clr.Reference[DB.UV]()
#out_sDistance = clr.Reference[float]()
#out_eDistance = clr.Reference[float]()


currentView=revit.uidoc.ActiveView

res = forms.alert("请选择板顶或板底",
                  options=["板顶",
                           "板底"])
if res == "板顶":
    surfaceRef=0
else:
    surfaceRef=1

@rpw.db.Transaction.ensure('CreateBeam')
def CreateBeam(Curve, FamilySymbol, Level, StructureType):
    doc.Create.NewFamilyInstance(Curve, FamilySymbol, Level, StructureType)
@rpw.db.Transaction.ensure('DeleteFamilyInstance')
def DeleteFamilyInstance(FamilyInstanceId):
    doc.Delete(FamilyInstanceId)


def getProjectedPoints(point,floor,surfaceRef=0):
    referenceIntersector = DB.ReferenceIntersector(floor.Id, DB.FindReferenceTarget.Face, currentView)
    ReferenceWithContext = referenceIntersector.Find(point, DB.XYZ(0, 0, 1))
    newPoint = ReferenceWithContext[surfaceRef].GetReference().GlobalPoint
    return newPoint




for beam in beams:

    if isinstance(beam.Location.Curve,DB.Arc):
        print("不支持弧线梁")
    elif isinstance(beam.Location.Curve,DB.Line):
    
        try:
            startPoint = beam.Location.Curve.GetEndPoint(0)
            endPoint = beam.Location.Curve.GetEndPoint(1)

            referenceIntersector = DB.ReferenceIntersector( floor.Id, DB.FindReferenceTarget.Face,currentView)

            sReferenceWithContext = referenceIntersector.Find(startPoint,DB.XYZ(0,0,1))
            eReferenceWithContext = referenceIntersector.Find(endPoint, DB.XYZ(0, 0, 1))


            _startPoint=sReferenceWithContext[surfaceRef].GetReference().GlobalPoint
            _endPoint = eReferenceWithContext[surfaceRef].GetReference().GlobalPoint

            _locationLine = DB.Line.CreateBound(_startPoint, _endPoint)
            Level = doc.GetElement(beam.LevelId)
            FramingSymbol = beam.Symbol
            StructuralType = beam.StructuralType
            c = CreateBeam(_locationLine, FramingSymbol, Level, StructuralType)
            DeleteFamilyInstance(beam.Id)
        except Exception as e:
            print(e)
    else:
        print("The Location.Curve Type is not correct")













