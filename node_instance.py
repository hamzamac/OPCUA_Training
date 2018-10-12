from opcua import Server, ua, uamethod, Node
from opcua.common.xmlexporter import XmlExporter
from uuid import UUID
# ----------------------------------NODE_INSTANCE CLASS MEMBERS-------------------------------------
# TODO : make server variable passed through argument
class NodeInstance(object):
    def __init__(self, server):      
        self._server = server
            
    @uamethod
    def remove_node_instance(self,parent, nodeid) -> bool:
        node = self._server.get_node(nodeid)
        node_list = []
        node_list.append(node)
        bname = node.get_browse_name()
        
        try:
            self._server.delete_nodes(node_list) 
            print('Node with name {0} deleted form server {1}'.format(bname, self._server.name))
            # TODO : use physical_node function to delete node file on disk
            return True
        except Exception as e:
            print('Failed to delete node with name {0} form server {1}: {2}'.format(bname, self._server.name, e))
            return False
        
    @uamethod
    def ssave_node_instance(self, parent, nodeid)->bool:
        exporter = XmlExporter(self._server)
        node = self._server.get_node(nodeid)
        
        exporter.node_to_etree(node)
        try:
            exporter.write_xml('node.xml')
            return True
        except Exception as e:
            print(e)
            return False
        
    @uamethod
    def get_type_name(self, parent, nodeid)->str:
        node = self._server.get_node(nodeid)
        type_definition = node.get_type_definition()
        type_name = self._server.get_node(type_definition).get_browse_name().Name
        return type_name       

    @uamethod
    def upload_node_instance(self, parent):
        pass

  
    @uamethod
    def create_node_instance(self,parent,name,typeid):
        parent_node = self._server.get_node(parent)
        type_node = self._server.get_node(typeid)

        try:
            instantiated_node = parent_node.add_object(parent.NamespaceIndex, name, objecttype=typeid)
            self.add_reference_to_type_methods(instantiated_node,type_node)
            print('Instantiated object with id: {0}'.format(instantiated_node))
            return True
        except Exception as e:
            print('Failed to instantiate node on server {0} : {1}'.format(self._server.name, e))
            return False
        instantiated_node = self.add_reference_to_type_methods(instantiated_node,type_node)

    @uamethod
    def save_node_instance(self, parent)->bool:
        parent_node = self._server.get_node(parent)
        for property in parent_node.get_properties():
            print(property.get_value)
            print(property.get_browse_name().Name)
        return True
    
   
    def add_reference_to_type_methods(self,instantiated_node,type_node):
        '''Adds reference to all methods of type object to node from one node to another'''
        method = type_node.get_methods()

        for method in type_node.get_methods():
            instantiated_node.add_reference(method, ua.ObjectIds.HasComponent,True, False)
        return instantiated_node
        
# END NODE_INSTANCE CLASS MEMBERS-------------------------------------
#self.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
#ua.NodeId(guid,parent.NamespaceIndex,ua.NodeIdType.String)
