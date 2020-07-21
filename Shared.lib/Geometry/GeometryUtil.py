# -*- coding: utf-8 -*-
__doc__="Revit Geometry Utility"
from pyrevit import DB
#######Get Element Slids
def getSolids(picked):
    name=picked.Name
    _options=DB.Options()
    _options.DetailLevel=DB.ViewDetailLevel.Fine
    geo_elem = picked.get_Geometry(_options)
    solids = []
    for geo in geo_elem:
        print(geo)
        if isinstance(geo, DB.Solid):
            print(geo)
            solids.append(geo)
        if isinstance(geo, DB.GeometryInstance):
            for i in geo.GetSymbolGeometry():
                solids.append(i)
    #########################