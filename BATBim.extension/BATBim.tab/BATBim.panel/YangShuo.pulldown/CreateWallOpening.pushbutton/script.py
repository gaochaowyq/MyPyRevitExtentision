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
from CSharp import FunctionHelper
from  Helper import *

hostapp = _HostApplication(__revit__)
print(hostapp.app.Language)
if hostapp.app.Language.ToString()=="English_USA":
    ParameterName=LG_EUN()
elif hostapp.app.Language.ToString()=="Chinese_Simplified":
    ParameterName = LG_CHS()

###########################################################################
# StartCode
curview = revit.active_view
curdoc=revit.doc
def GetElmentLocationCurve(element):
    locaiton=element.Locaiton
    if isinstance(DB.LocationCurve,locaiton):
        return locaiton
    else:
        print("This Element is PointBased")
        return None
walls = db.Collector(of_class='Wall',is_type=False)
# Get Symbol for Opening
openSymbol = rpw.db.Collector(of_category='OST_GenericModel', is_type=True).get_elements(wrapped=False)
openTypeOptions = {t.FamilyName + ";" + t.Parameter[DB.BuiltInParameter.SYMBOL_NAME_PARAM].AsString(): t for t in
                        openSymbol}
components = [
    Label('构件名称'),
    ComboBox('FamilyName', openTypeOptions),
    Button('确定')
]
form = FlexForm('开洞', components)
form.show()
Value = form.values
openSymbol=Value["FamilyName"]
##########################################################

###########################################################

@rpw.db.Transaction.ensure('Create Opening')
def CreateOpeningForWall(wall,ducts):
    """
    :param wall:
    :param ducts:
    :return:
    """
    for duct in ducts:
        framingType=duct.Symbol.Family.get_Parameter(DB.BuiltInParameter.FAMILY_STRUCT_MATERIAL_TYPE).AsInteger()
        if framingType==1:
            framingLocation=duct.Location
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

CreateOpeningForWall(pipes[0],walls[0])







