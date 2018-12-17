from opcua import Server, ua, uamethod, Node
from opcua.common.callback import CallbackType
import opcua.common.manage_nodes as node_manager
import logging
import time
from xml.etree.ElementTree import Element, ElementTree, SubElement

import node_instance as ni
def modify_monitored_item(event, dispatcher):
    print("created item modified")

def delet_subscription(event, dispatcher):
    print("Subscription deleted")

def func(parent):
    obj = server.get_node(parent).get_properties()[0]
    if obj.get_value() :
        obj.set_value(0)     
    else:
        obj.set_value(1)
        
    ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)

    server = Server()
    uri = "opc.tcp://localhost:4847"
    server.set_endpoint(uri)
    server.set_server_name("Day5")
    name_space_index = server.register_namespace(uri)

    #create folders
    component_folder = server.get_root_node().add_folder(name_space_index, "OEP")
    library_folder = component_folder.add_folder(name_space_index, "Library")
    workspace_folder = component_folder.add_folder(name_space_index, "Workspace")
    types_folder = component_folder.add_folder(name_space_index, "Types")

    i = ni.NodeInstance(server)
    workspace_folder.add_method(name_space_index, 'RemoveNode', i.remove_node_instance, [ua.VariantType.NodeId], [ua.VariantType.Boolean])
    workspace_folder.add_method(name_space_index, 'AddNode', i.create_node_instance, [ua.VariantType.String, ua.VariantType.NodeId], [ua.VariantType.Boolean])
    workspace_folder.add_method(name_space_index, 'SaveNode', i.save_node_instance, [ua.VariantType.NodeId], [ua.VariantType.Boolean])
    workspace_folder.add_method(name_space_index, 'GetTypeName', i.get_type_name, [ua.VariantType.NodeId], [ua.VariantType.String])
    
    
    #create a writable object
    switch_object_type = types_folder.add_object_type(name_space_index,"SwitchObjectType")
    switch_propoerty = switch_object_type.add_property(name_space_index, "state", 0, varianttype=ua.VariantType.Int32)
    switch_propoerty .set_modelling_rule(True)
    switch_propoerty.set_writable()
 
    oep_file_type = types_folder.add_object_type(name_space_index,"OepFileType")
    oep_file_type.add_reference(ua.NodeId(identifier= ua.ObjectIds.FileType), ua.ObjectIds.HasSubtype,forward=False)
    method1 = oep_file_type.add_method(name_space_index,"function", func, [], [ua.VariantType.Boolean])
    method1.set_modelling_rule(True)
    prop = oep_file_type.add_property(name_space_index, "state", 0, varianttype=ua.VariantType.Int32)
    prop.set_modelling_rule(True)
    var = oep_file_type.add_variable(name_space_index, "name", 0, varianttype=ua.VariantType.Int32)
    var.set_modelling_rule(True)

    oep_some_type = types_folder.add_object_type(name_space_index,"OepSomeType")
    oep_some_type.add_reference(oep_file_type, ua.ObjectIds.HasSubtype,forward=False)
    oep_some_type.add_method(name_space_index,"some_function", func, [], [ua.VariantType.Boolean])
    oep_some_type.add_property(name_space_index, "some_state", 0, varianttype=ua.VariantType.Int32).set_modelling_rule(True)

    #instatiate objects
    switch = workspace_folder.add_object(name_space_index, "Switch", objecttype=switch_object_type)
    my_file = workspace_folder.add_object(name_space_index, "MyFile", objecttype=oep_file_type)

    my_file_child1 = my_file.add_object(name_space_index, "MyFileChild1", objecttype=oep_file_type)
    my_file_child1_child = my_file_child1.add_object(name_space_index, "MyFileChild1Child", objecttype=oep_file_type)
    my_file_child2 = my_file.add_object(name_space_index, "MyFileChild2", objecttype=oep_file_type)
    my_file_child2_child = my_file_child2.add_object(name_space_index, "MyFileChild2Child", objecttype=oep_file_type)
    my_file_child1_child_child = my_file_child1_child.add_object(name_space_index, "MyFileChild1ChildChild", objecttype=oep_file_type)
    
    server.start()
    
    node = server.get_node(my_file.get_type_definition())
    methods = node.get_referenced_nodes(direction=ua.BrowseDirection.Inverse, nodeclassmask=ua.NodeClass.ObjectType).pop()
    
    #print(node.get_attribute(ua.AttributeIds.BrowseName))
    members = ni.get_node_members(my_file, server)
    # for key in members.keys():
    #     print('{0} : {1}'.format(key, members[key]))


    #create xml element yield
    # for m in ni.properties_generator(my_file, server):
    #     name = m.get_attribute(ua.AttributeIds.BrowseName).Value.Value.Name
    #     value = m.get_attribute(ua.AttributeIds.Value).Value.Value
    #     print(name)
    #     print(value)

    #pro = Element('property', {'name':'name'}).text = 'value'
    #print(pro)
    #open_emulation_platform version="1.0"

    def get_xml_from_node(node:Node, node_type:str, tree:ElementTree=None):
        if tree is None:
            tree = ElementTree(element=Element('opcua_emulation_platform', {'version':'1.0'}))
        root = tree.getroot()
        node_element = SubElement(root, node_type)
        node_element.set('guid', node.nodeid.to_string())
        node_metadata = SubElement(node_element, 'metadata')
        for property in ni.properties_generator(node, server):
            node_propoerty = SubElement(node_metadata, 'property')
            node_propoerty.set('name', property.get_attribute(ua.AttributeIds.BrowseName).Value.Value.Name)
            node_propoerty.text =  str(property.get_attribute(ua.AttributeIds.Value).Value.Value)
        return tree

    # t1 = get_xml_from_node(workspace_folder, 'system')
    # t1.write('node1.xml')
    # t2 = get_xml_from_node(my_file, 'component', t1)
    # t1.write('node2.xml')
    # print('done')   
    gen = ni.get_child_nodes_generator(my_file, server) 

    # for v in gen:
    #     print('Result', v.get_path(as_string=True))
    # else:
    #     print('end')
    
    def add_node_to_tree(child_node):
        parent_nodeid = child_node.get_parent().nodeid.to_string()
        paent_element = tree.find(".//*[@guid='{0}']".format(parent_nodeid))
        
        node_type = child_node.get_references(refs=ua.ObjectIds.HasTypeDefinition, direction=ua.BrowseDirection.Forward)[0]
        node_type_name = node_type.BrowseName.Name
        #child_node.server.get_node(node_type).get_attribute(ua.AttributeIds.BrowseName).Value.Value.Name
       
        print(node_type_name)
        #TODO: auto detect node type
        node_element = SubElement(paent_element, node_type_name)
        node_element.set('guid', child_node.nodeid.to_string())
        node_metadata = SubElement(node_element, 'metadata')
        for property in ni.properties_generator(child_node, server):
            node_propoerty = SubElement(node_metadata, 'property')
            node_propoerty.set('name', property.get_attribute(ua.AttributeIds.BrowseName).Value.Value.Name)
            node_propoerty.text =  str(property.get_attribute(ua.AttributeIds.Value).Value.Value)        

    def somefunc(gen_list, tree, add_node_to_tree):
        if len(gen_list) > 0:
            child_gen_list = []
            for generator in gen_list:
                for child_node in generator:
                    print(child_node.get_path(as_string=True))
                    # Begin Experiment
                    add_node_to_tree(child_node)
                    # End Experiment 
                    child_gen_list.append(ni.get_child_nodes_generator(child_node, server))
            else: 
                tree.write('tree.xml') 
                somefunc(child_gen_list, tree, add_node_to_tree)
        return tree

    print('*********')
    #tree = ElementTree(element=Element('opcua_emulation_platform', {'version':'1.0'}))
    tree = get_xml_from_node(my_file, 'component') 
    #tree.write('my_file.xml')            
    tree = somefunc([gen], tree, add_node_to_tree)
    # path = ".[@guid='{0}']".format(my_file_child1.get_parent().nodeid.to_string())
    # parent = tree.getroot().find(path)
    # parent.append(Element('Child1'))

    tree.write('me.xml')




    # print('*********')
    for n in node_manager._add_childs([my_file]):
        print('Child', n.get_path(as_string=True))
        
        
    
