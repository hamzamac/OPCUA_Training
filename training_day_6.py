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
    workspace_folder.add_method(name_space_index, 'RemoveWorksoace', i.remove_node_instance, [ua.VariantType.NodeId], [ua.VariantType.Boolean])
    workspace_folder.add_method(name_space_index, 'AddSystem', i.create_node_instance, [ua.VariantType.String, ua.VariantType.NodeId], [ua.VariantType.Boolean])
    workspace_folder.add_method(name_space_index, 'SaveWorkspace', i.save_node_instance, [ua.VariantType.NodeId], [ua.VariantType.Boolean])
    #workspace_folder.add_method(name_space_index, 'GetTypeName', i.get_type_name, [ua.VariantType.NodeId], [ua.VariantType.String])
    
    
    #Create Object Types
    system = types_folder.add_object_type(name_space_index,"System")
    system.add_method(name_space_index, 'AddAssembly', i.create_node_instance, [ua.VariantType.String, ua.VariantType.NodeId], [ua.VariantType.Boolean])
    system.add_method(name_space_index, 'RemoveAssembly', i.remove_node_instance, [ua.VariantType.String, ua.VariantType.NodeId], [ua.VariantType.Boolean])
    system_propoerty = system.add_property(name_space_index, "name", 0, varianttype=ua.VariantType.String)
    system_propoerty .set_modelling_rule(True)
    system_propoerty.set_writable()

    assembly = types_folder.add_object_type(name_space_index,"Assembly")
    assembly.add_method(name_space_index, 'AddComponent', i.create_node_instance, [ua.VariantType.String, ua.VariantType.NodeId], [ua.VariantType.Boolean])
    assembly.add_method(name_space_index, 'RemoveComponent', i.remove_node_instance, [ua.VariantType.String, ua.VariantType.NodeId], [ua.VariantType.Boolean])
    assembly_propoerty = assembly.add_property(name_space_index, "neme", 0, varianttype=ua.VariantType.String)
    assembly_propoerty .set_modelling_rule(True)
    assembly_propoerty.set_writable()

    component = types_folder.add_object_type(name_space_index,"Component")
    component_propoerty = component.add_property(name_space_index, "name", 0, varianttype=ua.VariantType.String)
    component_propoerty .set_modelling_rule(True)
    component_propoerty.set_writable()

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
    Component1 = library_folder.add_object(name_space_index, "Component1", objecttype=component)
    Component1.set_modelling_rule(True)
    Component2 = library_folder.add_object(name_space_index, "Component2", objecttype=component)
    

    server.start()


    def get_child_node_by_name(parent, child_name:str):
        childrens = parent.get_referenced_nodes(ua.ObjectIds.References, ua.BrowseDirection.Forward, nodeclassmask=ua.NodeClass.Object)
        result = {node.get_attribute(ua.AttributeIds.DisplayName).Value.Value.Text: node for node in childrens}

        if child_name in result:
            return result[child_name]
        else:
            return None
    
    print(get_child_node_by_name(component_folder, 'Workspace'))