from opcua import Server, ua, uamethod
from opcua.common.xmlexporter import XmlExporter

def main():
    server = Server()
    uri = "opc.tcp://localhost:4849/day3"
    server.set_endpoint(uri)
    address_space = server.register_namespace("uri")
    

    motor_object_type = server.nodes.base_object_type.add_object_type(0,"motor")
    motor_object_type.add_variable(0, "speed", 0, varianttype=ua.VariantType.Int32).set_modelling_rule(True)
    motor_object_type.add_property(0, "name", "IndustialMotor", varianttype=ua.VariantType.String).set_modelling_rule(True)
   
    #motor_object = instantiate(server.nodes.objects, motor_object_type,bname="0:namee")
    motor_object = server.nodes.objects.add_object(address_space, "RefinaryMotor", objecttype=motor_object_type)        

    #Lering Node object functions
    #print(motor_object.get_browse_name()) #QualifiedName(2:RefinaryMotor)
    #print(motor_object.get_node_class())
    #print(server)

    #expoting Method

    server.start()

    #XML
    xml_exporter = XmlExporter(server)
    xml_exporter.build_etree([motor_object_type])
    xml_exporter.write_xml("motor_object_type.xml")

if __name__ == "__main__" :
    main()