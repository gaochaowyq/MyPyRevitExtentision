# -*- coding: utf-8 -*-
def CovertToM3(input):
    return input/35.3147248
def CovertToM2(input):
    return input/10.7639104

def CovertToMM(input):
    return input*304.8
def CovertToFeet(input):
    return input/304.8
def CovertToM(input):
    return input*304.8

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
    BEAM_Start_Extension  ="Start Extension"
    BEAM_End_Extension = "End Extension"
    BEAM_z_Justification = "z Justification"
    InstanceMark  ="Mark"
    BEAM_Start_Level_Offset = "Start Level Offset"
    BEAM_End_Level_Offset = "End Level Offset"


class LG_CHS():
    BEAM_Start_Extension  ="开始延伸"
    BEAM_End_Extension = "端点延伸"
    BEAM_z_Justification = "Z 轴对正"
    InstanceMark = "标记"
    BEAM_Start_Level_Offset = "起点标高偏移"
    BEAM_End_Level_Offset = "终点标高偏移"