from opcua import Server, ua, uamethod, Node
from opcua.common.callback import CallbackType
import opcua.common.manage_nodes as node_manager
import logging
import time
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

# ----------------------------------NODE_INSTANCE CLASS MEMBERS-------------------------------------
# TODO : make server variable passed through argument
@uamethod
def remove_node_instance(parent, nodeid) -> bool:
    print('Received node id {0}'.format(nodeid))
    nodes = []
    nodes.append(server.get_node(nodeid))

    try:
        server.delete_nodes(nodes) 
        print('Node with name {0} deleted form server {1}'.format(node.get_browse_name(),server.name))
        # TODO : use physical_node function to delete node file on disk
        return True
    except Exception as e:
        print('Failed to delete node with name {0} form server {1}: {2}'.format(node.get_browse_name(),server.name, e))
        return False
    
@uamethod
def save_node_instance():
    pass

@uamethod
def upload_node_instance():
    pass


@uamethod
def create_node_instance(parent,name,typeid):
    parent_node = server.get_node(parent)
    type_node = server.get_node(typeid)
    method = type_node.get_methods()[0]

    try:
        instantiated_object =parent_node.add_object(name_space_index, name, objecttype=typeid)
        instantiated_object.add_reference(method, ua.ObjectIds.HasComponent,True, False)
        print('Instantiated object with id: {}'.format(instantiated_object))
        return True
    except Exception as e:
        print('Failed to instantiate node on server {0} : {1}'.format(server.name, e))
        return False

@uamethod
def copy_methods(parent,typeid,target_node_id):
    '''Copies all methods from one node to another'''
    pass

# END NODE_INSTANCE CLASS MEMBERS-------------------------------------
#self.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

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

    workspace_folder.add_method(name_space_index, 'RemoveNode', remove_node_instance, [ua.VariantType.NodeId], [ua.VariantType.Boolean])
    workspace_folder.add_method(name_space_index, 'AddNode', create_node_instance, [ua.VariantType.String, ua.VariantType.NodeId], [ua.VariantType.Boolean])
    
    
    #create a writable object
    switch_object_type = types_folder.add_object_type(name_space_index,"SwitchObjectType")
    switch_propoerty = switch_object_type.add_property(name_space_index, "state", 0, varianttype=ua.VariantType.Int32)
    switch_propoerty .set_modelling_rule(True)
    switch_propoerty.set_writable()
    # Hej! Kan du se den här?
    #ja
    # Nice! Proba att exekvera...
    # det finns live share audio
    # Det är riktigt bra! 
    # Vi kan prova audio imorgon ;) Vi ses imorgon!
    #vi ses

    oep_file_type = types_folder.add_object_type(name_space_index,"OepFileType")
    oep_file_type.add_reference(ua.NodeId(identifier= ua.ObjectIds.FileType), ua.ObjectIds.HasSubtype,forward=False)
    method1 = oep_file_type.add_method(name_space_index,"function", func, [], [ua.VariantType.Boolean])
    prop = oep_file_type.add_property(name_space_index, "state", 0, varianttype=ua.VariantType.Int32)
    prop.set_modelling_rule(True)

    oep_some_type = types_folder.add_object_type(name_space_index,"OepSomeType")
    oep_some_type.add_reference(oep_file_type, ua.ObjectIds.HasSubtype,forward=False)
    oep_some_type.add_method(name_space_index,"some_function", func, [], [ua.VariantType.Boolean])
    oep_some_type.add_property(name_space_index, "some_state", 0, varianttype=ua.VariantType.Int32).set_modelling_rule(True)
    

    
    


    #instatiate objects
    switch = workspace_folder.add_object(name_space_index, "Switch", objecttype=switch_object_type)

    my_file = workspace_folder.add_object(name_space_index, "MyFile", objecttype=oep_file_type)
    my_file.set_modelling_rule(True)
    
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