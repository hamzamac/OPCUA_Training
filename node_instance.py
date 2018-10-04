from opcua import Server, ua, uamethod, Node

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
