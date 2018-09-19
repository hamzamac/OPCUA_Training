from opcua import Server, ua, instantiate

def main():
    server = Server()
    uri = "opc.tcp://localhost:4849/day3"
    server.set_endpoint(uri)
    address_space = server.register_namespace("uri")
    

    motor_object_type = server.nodes.base_object_type.add_object_type(0,"motor")
    motor_object_type.add_variable(0, "speed", 0, varianttype=ua.VariantType.Int32).set_modelling_rule(True)
    motor_object_type.add_property(0, "name", "IndustialMotor", varianttype=ua.VariantType.String).set_modelling_rule(True)
   
    motor_object = instantiate(server.nodes.objects, motor_object_type,bname="0:namee")
    #motor_object = server.nodes.objects.add_object(address_space, "RefenaryMotor", objecttype=motor_object_type)        

    server.start()

if __name__ == "__main__" :
    main()