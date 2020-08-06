#!/usr/bin/python


import xml.etree.ElementTree as ET



def main(file_name):
    """
    this commond is used to change the safe file.
    """
    tree = ET.ElementTree(file=file_name)
    root = tree.getroot()
    temp1=file_name[14:22]
    #for component in root.findall('productInfo/missionInfo/orbitDirection'):
    	#print component.text
    for component2 in root.findall('generalAnnotation/productInformation/pass'):
	temp2=component2.text    
    for component3 in root.findall('adsHeader/absoluteOrbitNumber'):
    	temp3=component3.text
    print ("%s %s %s"%(temp1,temp2,temp3))
    return 

if __name__=='__main__':
    import sys
    main(sys.argv[1])

# for elem in tree.iter():
#         name=elem.get('name')
#         #if (name)
#         com=elem.text
#         print ('{0:25}  >>>  {1:10}'.format(name, com))



