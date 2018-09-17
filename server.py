from opcua import Server, ua
import logging

def main():
    
    logging.basicConfig(level=logging.INFO)

    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4040/simumatik")
    server.set_server_name("Simumatik OpcUa Server")
    #server.set_security_policy(ua.SecurityPolicyType.NoSecurity)


    #create node
    node1 = server.nodes.base_object_type.add_object_type(0, "Cube")
    node1.add_variable(0, "height", 3.0).set_modelling_rule(True)
    node1.add_variable(0, "width", 3.0).set_modelling_rule(True)
    node1.add_variable(0, "bredth", 3.0).set_modelling_rule(True)
    node1.add_property(0, "cube_id", "1001")

    #controller = node1.add_object(0, "controller")
    #controller.set_modelling_rule(True)
    #controller.add_property(0, "state", "Visible").set_modelling_rule(True)

    server.start()


if __name__ == "__main__":
    main()
