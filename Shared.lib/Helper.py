# -*- coding: utf-8 -*-
from pyrevit import revit, DB
def CovertToM3(input):
    value = DB.UnitUtils.ConvertFromInternalUnits(input, DB.DisplayUnitType.DUT_CUBIC_METERS)
    return value
def CovertToM2(input):
    value = DB.UnitUtils.ConvertFromInternalUnits(input, DB.DisplayUnitType.DUT_SQUARE_METERS)
    return value

def CovertToMM(input):
    value = DB.UnitUtils.ConvertFromInternalUnits(input, DB.DisplayUnitType.DUT_MILLIMETERS)
    return value
def CovertToFeet(input):
    value = DB.UnitUtils.ConvertToInternalUnits(input, DB.DisplayUnitType.DUT_MILLIMETERS)
    return value
def CovertToM(input):
    return input*304.800000

def MmToFeet(input):
    return input*3.2808399

def StrToNumber(Input):
    if isinstance(Input,str):
        print(Input)
        c=float(Input[0:-3])
    else:
        c=Input

    return c



def List_Flat(nested_list):
    flatlist=[]
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            for sub_item in List_Flat(item):
                flatlist.append(sub_item)
        else:
            flatlist.append(item)

        return flatlist
             

class LG_EUN():

    #####################################
    #General
    #####################################
    InstanceMark  ="Mark"
    LIGHT_Photometric_Web_File="Photometric Web File"
    Room_Wall_Finish = "Wall Finish"

    #####################################
    #Framing/Beam
    #####################################
    BEAM_Start_Extension  ="Start Extension"
    BEAM_End_Extension = "End Extension"
    BEAM_z_Justification = "z Justification"
    BEAM_Start_Level_Offset = "Start Level Offset"
    BEAM_End_Level_Offset = "End Level Offset"
    BEAM_Width="Width"
    BEAM_Height="Height"


    #####################################
    #WallS
    ####################################

    WALL_BASE_CONSTRAINT="Base Constraint"
    WALL_BASE_OFFSET="Base Offset"
    WALL_HEIGHT_TYPE="Top Constraint"
    WALL_TOP_OFFSET="Top Offset"

    WALL_Length = "Length"
    WALL_Area = "Area"
    WALL_Volume = "Volume"






class LG_CHS():
    #####################################
    #General
    #####################################
    LIGHT_Photometric_Web_File = "光域网文件"
    Room_Wall_Finish = "墙面面层"
    InstanceMark = "标记"
    #####################################
    #Framing/Beam
    #####################################

    BEAM_Start_Extension  ="开始延伸"
    BEAM_End_Extension = "端点延伸"
    BEAM_z_Justification = "Z 轴对正"

    BEAM_Start_Level_Offset = "起点标高偏移"
    BEAM_End_Level_Offset = "终点标高偏移"
    BEAM_Width="宽度"
    BEAM_Height="高度"

    #####################################
    #WallS
    ####################################

    WALL_BASE_CONSTRAINT="底部约束"
    WALL_BASE_OFFSET="底部偏移"
    WALL_HEIGHT_TYPE="顶部约束"
    WALL_TOP_OFFSET="顶部偏移"
    WALL_Length = "长度"
    WALL_Area = "面积"
    WALL_Volume = "体积"


