from opcua import Server, ua, uamethod, Node
from opcua.common.callback import CallbackType
import opcua.common.manage_nodes as node_manager
import logging
import time

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
    

    server.start()
    
    node = server.get_node(my_file.get_type_definition())
    methods = node.get_referenced_nodes(direction=ua.BrowseDirection.Inverse, nodeclassmask=ua.NodeClass.ObjectType).pop()
    
    print(node.get_attribute(ua.AttributeIds.BrowseName))
    members = ni.get_node_members(my_file, server)
    for key in members.keys():
        print('{0} : {1}'.format(key, members[key]))


    
                



