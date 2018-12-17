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
    oep_folder = server.get_root_node().add_folder(name_space_index, "OEP")
    library_folder = oep_folder.add_folder(name_space_index, "Library")
    workspace_folder = oep_folder.add_folder(name_space_index, "Workspace")
    types_folder = oep_folder.add_folder(name_space_index, "Types")

    
    #create a object types
    oep_file_type = types_folder.add_object_type(name_space_index,"OepFileType")
    oep_file_type.add_reference(ua.NodeId(identifier= ua.ObjectIds.FileType), ua.ObjectIds.HasSubtype,forward=False)
    method1 = oep_file_type.add_method(name_space_index,"function", func, [], [ua.VariantType.Boolean])
    method1.set_modelling_rule(True)
    prop = oep_file_type.add_property(name_space_index, "property", 0, varianttype=ua.VariantType.Int32)
    prop.set_modelling_rule(True)
    var = oep_file_type.add_variable(name_space_index, "variable", 0, varianttype=ua.VariantType.Int32) 
    var.set_modelling_rule(True)

    #instatiate object as component
    my_file = library_folder.add_object(name_space_index, "MyFile", objecttype=oep_file_type)
    # my_file.add_reference(prop, ua.ObjectIds.HasProperty,True, False)


    #my_file.add_reference(var, ua.ObjectIds.HasComponent,True, False)
    instance1 = workspace_folder.add_object(name_space_index, "FileInstance1", objecttype=oep_file_type)
    # system.add_reference(prop, ua.ObjectIds.HasProperty,True, False)
    # system.add_reference(var, ua.ObjectIds.HasComponent,True, False)
    # system.add_reference(method1, ua.ObjectIds.HasComponent,True, False)

    instance2 = workspace_folder.add_object(name_space_index, "FileInstance2", objecttype=oep_file_type)
    ni.add_reference_to_type_properties(instance2, my_file)
    server.start()
