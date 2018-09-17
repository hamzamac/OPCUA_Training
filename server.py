from opcua import Server, ua
import logging

def main():
    
    logging.basicConfig(level=logging.INFO)

    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4040/simumatik")
    server.set_server_name("Simumatik OpcUa Server")
    server.set_security_policy(ua.SecurityPolicyType.NoSecurity)

    logging.info("Server started")



if __name__ == "__main__":
    main()
