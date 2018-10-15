from xml.etree.ElementTree import Element, ElementTree as et, SubElement




if __name__ == '__main__':
    tree = et(element=Element('opcua_emulation_platform', {'version':'1.0'}))
    root = tree.getroot()
    system = SubElement(root, 'system', {'guid':'1111'})
    system2 = SubElement(root, 'system', {'guid':'1111'})
    tree.write('tree.xml')

    found = tree.find("//*[@guid='1111']")
    assembly = Element('assembly', {'guid':'2222'})
    assembly.text = ' '
    found.append(assembly)
    tree.write('tree.xml')

