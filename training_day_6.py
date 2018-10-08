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
    server.set_server_name("Day6")
    server.set_application_uri('Day6')
    name_space_index = server.register_namespace(uri)

    #create folders
    component_folder = server.get_root_node().add_folder(name_space_index, "OEP")
    types_folder = component_folder.add_folder(name_space_index, "Types")
    library_folder = component_folder.add_folder(name_space_index, "Library")
    workspace_folder = component_folder.add_folder(name_space_index, "Workspace")
    

    i = ni.NodeInstance(server)
    workspace_folder.add_method(name_space_index, 'RemoveNode', i.remove_node_instance, [ua.VariantType.NodeId], [ua.VariantType.Boolean])
    workspace_folder.add_method(name_space_index, 'AddNode', i.create_node_instance, [ua.VariantType.String, ua.VariantType.NodeId], [ua.VariantType.Boolean])
    workspace_folder.add_method(name_space_index, 'SaveNode', i.save_node_instance, [ua.VariantType.NodeId], [ua.VariantType.Boolean])
    workspace_folder.add_method(name_space_index, 'GetTypeName', i.get_type_name, [ua.VariantType.NodeId], [ua.VariantType.String])
    
    
    #Create Object Types
    system = types_folder.add_object_type(name_space_index,"System")
    system_propoerty = system.add_property(name_space_index, "name", 0, varianttype=ua.VariantType.string)
    system_propoerty .set_modelling_rule(True)
    system_propoerty.set_writable()

    assembly = types_folder.add_object_type(name_space_index,"Assembly")
    assembly_propoerty = assembly.add_property(name_space_index, "neme", 0, varianttype=ua.VariantType.String)
    assembly_propoerty .set_modelling_rule(True)
    assembly_propoerty.set_writable()

    component = types_folder.add_object_type(name_space_index,"Assembly")
    component_propoerty = component.add_property(name_space_index, "name", 0, varianttype=ua.VariantType.String)
    component_propoerty .set_modelling_rule(True)
    component_propoerty.set_writable()

    system = types_folder.add_object_type(name_space_index,"System")
    system_propoerty = system.add_property(name_space_index, "state", 0, varianttype=ua.VariantType.Int32)
    system_propoerty .set_modelling_rule(True)
    system_propoerty.set_writable()



    # oep_file_type = types_folder.add_object_type(name_space_index,"OepFileType")
    # oep_file_type.add_reference(ua.NodeId(identifier= ua.ObjectIds.FileType), ua.ObjectIds.HasSubtype,forward=False)
    # method1 = oep_file_type.add_method(name_space_index,"function", func, [], [ua.VariantType.Boolean])
    # prop = oep_file_type.add_property(name_space_index, "state", 0, varianttype=ua.VariantType.Int32)
    # prop.set_modelling_rule(True)

    # oep_some_type = types_folder.add_object_type(name_space_index,"OepSomeType")
    # oep_some_type.add_reference(oep_file_type, ua.ObjectIds.HasSubtype,forward=False)
    # oep_some_type.add_method(name_space_index,"some_function", func, [], [ua.VariantType.Boolean])
    # oep_some_type.add_property(name_space_index, "some_state", 0, varianttype=ua.VariantType.Int32).set_modelling_rule(True)
    
    #instatiate objects
    Component1 = workspace_folder.add_object(name_space_index, "Component1", objecttype=component)
    Component2 = workspace_folder.add_object(name_space_index, "Component2", objecttype=component)
    
    #my_file.set_modelling_rule(True)
    


    #Create Callback for item events
    #server.subscribe_server_callback(CallbackType.ItemSubscriptionCreated, modify_monitored_item)
    #server.subscribe_server_callback(CallbackType.ItemSubscriptionDeleted, delet_subscription)
    
    
    server.start()
    #my_file.get_children()
    node = server.get_node(my_file.get_type_definition())
    methods = node.get_referenced_nodes(direction=ua.BrowseDirection.Inverse, nodeclassmask=ua.NodeClass.ObjectType).pop()
    # print(my_file.get_referenced_nodes())
    # print(my_file.get_type_definition())
    # print()
    
    # for m in methods.get_methods():
    #     print(m.get_browse_name())