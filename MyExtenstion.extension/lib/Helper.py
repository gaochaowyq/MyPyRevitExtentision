def CovertToM3(input):
	return input/35.3147248
def CovertToM2(input):
	return input/10.7639104
	
def CovertToMM(input):
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
             

