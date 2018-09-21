from opcua import Server

if __name__ == "__main__":
    server = Server()
    uri = "opc.tcp://localhost:4847"
    server.set_endpoint(uri)
    server.set_server_name("Day5")
    name_space_index = server.register_namespace(uri)

    server.start()

