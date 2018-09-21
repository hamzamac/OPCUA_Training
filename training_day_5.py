from opcua import Server, ua
from opcua.common.callback import CallbackType
import logging
import time
def modify_monitored_item(event, dispatcher):
    print("created tem modified")

def delet_subscription(event, dispatcher):
    print("Subscription deleted")

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)

    server = Server()
    uri = "opc.tcp://localhost:4847"
    server.set_endpoint(uri)
    server.set_server_name("Day5")
    name_space_index = server.register_namespace(uri)

    #create folder
    component_folder = server.get_objects_node().add_folder(name_space_index, "Components")
    
    #create a writable object
    switch_object_type = server.nodes.object_types.add_object_type(name_space_index,"SwitchType")
    switch_propoerty = switch_object_type.add_property(name_space_index, "state", 0, varianttype=ua.VariantType.Int32)
    switch_propoerty .set_modelling_rule(True)
    switch_propoerty.set_writable()
    
    
    switch = component_folder.add_object(name_space_index, "Switch", objecttype=switch_object_type)
    
    #Create Callback for item events
    server.subscribe_server_callback(CallbackType.ItemSubscriptionCreated, modify_monitored_item)
    server.subscribe_server_callback(CallbackType.ItemSubscriptionDeleted, delet_subscription)
    
    server.start()

    while True:
        try:
            # print(switch.get_properties())
            # print(switch.get_properties().pop().get_browse_name().to_string())
            time.sleep(5)
        finally:
            pass
