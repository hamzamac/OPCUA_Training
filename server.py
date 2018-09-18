from opcua import Server, ua
import logging
import time

def main():
    
    logging.basicConfig(level=logging.INFO)

    server = Server()
    server.set_endpoint("opc.tcp://localhost:4841/makame")
    
    server.set_server_name("Simumatik OpcUa Server")
    
    uri = "https://github.com/hamzamac"
    address_space = server.register_namespace(uri)

    #create node type
    cube_teype = server.nodes.base_object_type.add_object_type(0, "Cube")
    cube_teype.add_variable(0, "height", 3.0).set_modelling_rule(True)
    cube_teype.add_variable(0, "width", 3.0).set_modelling_rule(True)
    cube_teype.add_variable(0, "bredth", 3.0).set_modelling_rule(True)
    cube_teype.add_property(0, "cube_id", "1001").set_modelling_rule(True)

    objects = server.get_objects_node()
    cube1 = objects.add_object(address_space, "Cube1", objecttype=cube_teype)
    
    

  
    # starting!
    server.start()

    while(True):
        time.sleep(2)
        

    """

    # populating our address space
    myobj = objects.add_object(address_space, "MyObject")
    myvar = myobj.add_variable(address_space, "MyVariable", 6.7)
    myvar.set_writable()    # Set MyVariable to be writable by clients

    #create node type
    cube_teype = server.nodes.base_object_type.add_object_type(0, "Cube")
    cube_teype.add_variable(0, "height", 3.0).set_modelling_rule(True)
    cube_teype.add_variable(0, "width", 3.0).set_modelling_rule(True)
    cube_teype.add_variable(0, "bredth", 3.0).set_modelling_rule(True)
    cube_teype.add_property(0, "cube_id", "1001")


    objects = server.get_objects_node()
    cube1 = objects.add_object(address_space, "Cube1", objecttype=cube_teype)

    #create forder for the cubes objects instances
    cub_folder = server.nodes.objects.add_folder(ns,"cubeFolder")

    cube1 = server.nodes.objects.add_object(ns, "Cube1", objecttype=cube_teype)
    """

    #server.start()


if __name__ == "__main__":
    main()
