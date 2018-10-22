from opcua import Server, ua, uamethod, Node
from opcua.common.callback import CallbackType
import opcua.common.manage_nodes as node_manager
import logging
import time
import opcua.ua.uatypes

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

def set_variable_value(parent, nodeid, new_value): 
    old_value = server.get_node(nodeid.Value).get_attribute(ua.AttributeIds.Value).Value
    if old_value.VariantType.value == new_value.VariantType.value:
        if old_value.is_array == new_value.is_array:
            try:
                server.get_node(nodeid.Value).set_attribute(ua.AttributeIds.Value, ua.DataValue(ua.Variant(new_value.Value,old_value.VariantType)))
                
                print(server.get_node(nodeid.Value).get_attribute(ua.AttributeIds.ValueRank))
                print(server.get_node(nodeid.Value).get_attribute(ua.AttributeIds.Value).Value.is_array)
                return [True]
            except Exception as e:
                print(e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)

    server = Server()
    uri = "opc.tcp://localhost:4847"
    server.set_endpoint(uri)
    server.set_server_name("Day8")
    name_space_index = server.register_namespace(uri)

    #create folders
    component_folder = server.get_root_node().add_folder(name_space_index, "OEP")
    workspace_folder = component_folder.add_folder(name_space_index, "Workspace")
    types_folder = component_folder.add_folder(name_space_index, "Types")

  
    oep_file_type = types_folder.add_object_type(name_space_index,"OepFileType")
    oep_file_type.add_reference(ua.NodeId(identifier= ua.ObjectIds.FileType), ua.ObjectIds.HasSubtype,forward=False)
    method1 = oep_file_type.add_method(name_space_index,"function", set_variable_value, [ua.VariantType.NodeId, ua.VariantType.Variant], [ua.VariantType.Boolean])
    prop = oep_file_type.add_property(name_space_index, "state", 0, varianttype=ua.VariantType.Int32)
    prop.set_modelling_rule(True)
    var = oep_file_type.add_variable(name_space_index, "age", 34, varianttype=ua.VariantType.Int32)
    var.set_modelling_rule(True)

    
    my_file = workspace_folder.add_object(name_space_index, "MyFile", objecttype=oep_file_type)
    
    server.start()




    variabl = my_file.add_variable(name_space_index, 'newAdded', [3,4,45])

    try:
        my_file.call_method(method1, variabl.nodeid ,230)
    except Exception as e:
        print(e)
    
    # for p in my_file.get_variables():
    #     #print(p.set_value([2,4,5,6]))
    #     print(p.get_attribute(ua.AttributeIds.Value))
    #     print(p.get_attribute(ua.AttributeIds.Value).Value.is_array)
    print('done')

    #my_file.get_children()
    #node = server.get_node(my_file.get_type_definition())
    #methods = node.get_referenced_nodes(direction=ua.BrowseDirection.Inverse, nodeclassmask=ua.NodeClass.ObjectType).pop()
    # print(my_file.get_referenced_nodes())
    # print(my_file.get_type_definition())
    # print()
    
    # for m in methods.get_methods():
    #     print(m.get_browse_name())