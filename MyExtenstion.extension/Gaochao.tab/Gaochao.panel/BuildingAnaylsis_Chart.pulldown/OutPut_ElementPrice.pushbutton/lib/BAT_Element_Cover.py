# -*- encoding: utf-8 -*-
from Base import GetAllBase
from Minix import *
from pyrevit import DB

#################################################################################
class Get_Stu_Base(GetAllBase):
    def __init__(self):
        super(Get_Stu_Base, self).__init__()
        self.AssembleCode = "14-20.10"
        self.ClassName = "地基基础"
        self.unit = 'm3'


class Get_Stu_CO_Floors(GetAllBase):
    def __init__(self):
        super(Get_Stu_CO_Floors, self).__init__()
        self.AssembleCode = "14-20.20.03"
        self.ClassName = "结构楼地板"
        self.unit = 'm2'

class Get_Stu_ST_Columns(GetAllBase):
    def __init__(self):
        super(Get_Stu_ST_Columns, self).__init__()
        self.AssembleCode = "14-20.30.03"
        self.ClassName = "钢结构柱"
        self.unit = 't'
class Get_Stu_ST_Framings(GetAllBase):
    def __init__(self):
        super(Get_Stu_ST_Framings, self).__init__()
        self.AssembleCode = "14-20.30.06"
        self.ClassName = "钢结构梁"
        self.unit = 't'


class Get_Stu_CO_Columns(GetAllBase):
    def __init__(self):
        super(Get_Stu_CO_Columns, self).__init__()
        self.AssembleCode = "14-20.20.09"
        self.ClassName = "混凝土结构柱"
        self.unit = 'm3'


class Get_Stu_CO_Walls(GetAllBase):
    def __init__(self):
        super(Get_Stu_CO_Walls, self).__init__()
        self.AssembleCode = "14-20.20.15"
        self.ClassName = "混凝土结构墙"
        self.unit = 'm2'


##################################################################

class Get_Arc_Element_Walls(GetAllBase):
    def __init__(self):
        super(Get_Arc_Element_Walls, self).__init__()
        self.AssembleCode = "14-10.20.03"
        self.ClassName = "建筑墙"
        self.unit = 'm2'


class Get_Arc_Element_Columns(GetAllBase):
    def __init__(self):
        super(Get_Arc_Element_Columns, self).__init__()
        self.AssembleCode = "14-10.20.06"
        self.ClassName = "建筑柱"
        self.unit = 'Count'
#"Get_Arc_Element_Planting_Place":"14-10.10.18.12"

class Get_Arc_Element_Planting_Place(GetAllBase):
    def __init__(self):
        super(Get_Arc_Element_Planting_Place, self).__init__()
        self.AssembleCode = "14-10.10.18.12"
        self.ClassName = "种植花槽"
        self.unit = 'Count'


class Get_Arc_Element_Door(GetAllBase):
    def __init__(self):
        super(Get_Arc_Element_Door, self).__init__()
        self.AssembleCode = "14-10.20.09"
        self.ClassName = "门"
        self.unit = 'Count'


class Get_Arc_Element_Window(GetAllBase):
    def __init__(self):
        super(Get_Arc_Element_Window, self).__init__()
        self.AssembleCode = "14-10.20.12"
        self.ClassName = "窗户"
        self.unit = 'Count'


class Get_Arc_Element_Roofs(GetAllBase):
    def __init__(self):
        super(Get_Arc_Element_Roofs, self).__init__()
        self.AssembleCode = "14-10.20.15"
        self.ClassName = "建筑屋面"
        self.unit = 'm2'


class Get_Arc_Element_Floors(GetAllBase):
    def __init__(self):
        super(Get_Arc_Element_Floors, self).__init__()
        self.AssembleCode = "14-10.20.18"
        self.NotContainAssembleCode = "14-10.20.18.15"
        self.ClassName = "建筑楼地板"
        self.unit = 'm2'


class Get_Arc_Element_Ceiling(GetAllBase):
    def __init__(self):
        super(Get_Arc_Element_Ceiling, self).__init__()
        self.AssembleCode = "14-10.20.24"
        self.ClassName = "建筑吊顶"
        self.unit = 'm2'
#"Get_Arc_Element_CurtainWall_Element":"14-10.20.21.03",
class Get_Arc_Element_CurtainWall_Element(GetAllBase):
    def __init__(self):
        super(Get_Arc_Element_CurtainWall_Element, self).__init__()
        self.AssembleCode = "14-10.20.21.03"
        self.ClassName = "立面幕墙其它构件"
        self.unit = 'Count'
#"Get_Arc_Element_Canopy":"14-10.20.48.12",
class Get_Arc_Element_Canopy(GetAllBase):
    def __init__(self):
        super(Get_Arc_Element_Canopy, self).__init__()
        self.AssembleCode = "14-10.20.48.12"
        self.ClassName = "雨棚"
        self.unit = 'Count'



class Get_MEP_Ducts(GetAllBase):
    def __init__(self):
        super(Get_MEP_Ducts, self).__init__()
        self.AssembleCode = "14-30.40.03"
        self.ClassName = "MEP_风管"
        self.unit = 'm'


class Get_MEP_Pipe(MixPipe, GetAllBase):
    def __init__(self):
        super(Get_MEP_Pipe, self).__init__()
        self.AssembleCode = "14-30.20.03"
        self.ClassName = "MEP_水管"
        self.unit = 'm'
#14 40 10 03
#14 40 20 03
#14 40 30
class Get_MEP_SupplyPipe(MixPipe, GetAllBase):
    def __init__(self):
        super(Get_MEP_SupplyPipe, self).__init__()
        self.AssembleCode = "14-40.10.03"
        self.ClassName = "供水管道"
        self.unit = 'm'
class Get_MEP_DrainPipe(MixPipe, GetAllBase):
    def __init__(self):
        super(Get_MEP_DrainPipe, self).__init__()
        self.AssembleCode = "14-40.20.03"
        self.ClassName = "排水管道"
        self.unit = 'm'

class Get_MEP_FirePipe(MixPipe, GetAllBase):
    def __init__(self):
        super(Get_MEP_FirePipe, self).__init__()
        self.AssembleCode ="14-40.30.09+14-40.30.12+14-40.30.15"
        self.ClassName = "消防用水管道"
        self.unit = 'm'

class Get_MEP_Conduit(MixConduit, GetAllBase):
    def __init__(self):
        super(Get_MEP_Conduit, self).__init__()
        self.AssembleCode = "14-50.40"
        self.ClassName = "MEP_线缆"
        self.unit = 'm'
###########################################################
#Custom Part
#"Get_Custom_HAVC_Place":"14-60.10"
class Get_Custom_HAVC_Place(GetAllBase):
    def __init__(self):
        super(Get_Custom_HAVC_Place, self).__init__()
        self.AssembleCode = "14-60.10"
        self.ClassName = "空调架"
        self.unit = 'Count'

class Get_WallFloors(GetAllBase):
    def __init__(self):
        super(Get_WallFloors, self).__init__()
        self.AssembleCode = "14-20.20.03+14-10.20.03"
        self.ClassName = "空调架"
        self.unit = 'm2'