from opcua import Server, ua
from opcua.common.callback import CallbackType
import logging
import time
def modify_monitored_item(event, dispatcher):
    print("created item modified")

def delet_subscription(event, dispatcher):
    print("Subscription deleted")

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
    prop = oep_file_type.add_property(name_space_index, "state", 0, varianttype=ua.VariantType.Int32)
    prop.set_modelling_rule(None)
    #you made it
    #instatiate objects
    switch = workspace_folder.add_object(name_space_index, "Switch", objecttype=switch_object_type)

    my_file = workspace_folder.add_object(name_space_index, "MyFile", objecttype=oep_file_type)
    
    
    #Create Callback for item events
    #server.subscribe_server_callback(CallbackType.ItemSubscriptionCreated, modify_monitored_item)
    #server.subscribe_server_callback(CallbackType.ItemSubscriptionDeleted, delet_subscription)
    
    
    server.start()
    #my_file.get_children()
    node = server.get_node(my_file.get_type_definition())
    methods = node.get_referenced_nodes(direction=ua.BrowseDirection.Inverse, nodeclassmask=ua.NodeClass.ObjectType).pop()
    print(my_file.get_referenced_nodes())
    print(my_file.get_type_definition())
    print()
    for m in methods.get_methods():
        print(m.get_browse_name())