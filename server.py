from opcua import Server, ua, uamethod
import logging
import time

def main():
    
    logging.basicConfig(level=logging.WARNING)

    server = Server()
    server.set_endpoint("opc.tcp://localhost:4841/makame")
    
    server.set_server_name("Simumatik OpcUa Server")
    
    uri = "https://github.com/hamzamac"
    address_space = server.register_namespace(uri)

    #define a function
    
    def func(parent):
        led_state = server.get_node(parent).get_properties()[0]
        if led_state.get_value() :
            led_state.set_value(0)
        else:
            led_state.set_value(1)

        ret = True
        return [ua.Variant(ret, ua.VariantType.Boolean)]  

    #create node type
    cube_teype = server.nodes.base_object_type.add_object_type(0, "Cube")
    cube_teype.add_variable(0, "height", 3.0).set_modelling_rule(True)
    cube_teype.add_variable(0, "width", 3.0).set_modelling_rule(True)
    cube_teype.add_variable(0, "bredth", 3.0).set_modelling_rule(True)
    cube_teype.add_property(0, "cube_id", "1001").set_modelling_rule(True)

    #create an LED type with a toggl methode method
    led_type = server.nodes.base_object_type.add_object_type(1, "LED")
    led_type.add_property(1,"state", 0).set_modelling_rule(True)

    #events
    led_event_type = server.nodes.base_event_type.add_object_type(2,"ledEvent")


    # create cube object that references an LED object
    objects = server.get_objects_node()

    cube1 = objects.add_object(address_space, "Cube1", objecttype=cube_teype)

    led1 = objects.add_object(address_space, "led1", objecttype=led_type)
    led1.add_method(address_space,"function", func, [], [ua.VariantType.Boolean])
    
    led_event_generator = server.get_event_generator(led_event_type,led1)
    led_event_generator.event.Message = ua.LocalizedText("this is a LED event")

    # starting!
    server.start()
    try:
        while(True):
            if  len(led1.get_properties()) :
                led_state = led1.get_properties()[0]
                state_value = led_state.get_value()
                if state_value:
                    led_event_generator.trigger()
            time.sleep(3)
    finally:
        server.stop()


if __name__ == "__main__":
    main()
