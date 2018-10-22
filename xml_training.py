from xml.etree import ElementTree as ET
import time
if __name__ == '__main__':
    # tree = et(element=Element('opcua_emulation_platform', {'version':'1.0'}))
    # root = tree.getroot()
    # system = SubElement(root, 'system', {'guid':'1111'})
    # system2 = SubElement(root, 'system', {'guid':'1111'})
    # tree.write('tree.xml')

    # found = tree.find("//*[@guid='1111']")
    # assembly = Element('assembly', {'guid':'2222'})
    # assembly.text = ' '
    # found.append(assembly)
    # tree.write('tree.xml')

    node_tree = ET.parse('component.xml')
    root = node_tree.getroot()

    def get_child_elements_generator(element):
        '''Returns the child element that have tag name as a types from OpenEmulationPlatformTypes'''
        for child in element.findall('*'):
            yield child
    
    def children_element_iterrator(gen_list):
        if len(gen_list) > 0:
            child_gen_list = []
            
            for generator in gen_list:
                for child_element in generator[0]:
                    print(child_element.tag, child_element.get('guid'), generator[1])
                    child_gen_list.append((get_child_elements_generator(child_element), child_element.tag))
            else:
                children_element_iterrator(child_gen_list)

    gen = get_child_elements_generator(root)
    children_element_iterrator([(gen,'parent')])

