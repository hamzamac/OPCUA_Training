from opcua import Server, ua, uamethod, Node
from opcua.common.callback import CallbackType
import opcua.common.manage_nodes as node_manager
import logging
import time
import opcua.ua.uatypes

import node_instance as ni
def modify_monitored_item(event, dispatcher):
    print("created item modified")

def delet_subscription(event, dispatcher):
    print("Subscription deleted")

def func(parent):
    obj = server.get_node(parent).get_properties()[0]
    if obj.get_value() :
        obj.set_value(0)     
    else:
        obj.set_value(1)
        
    ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]

@uamethod
def set_variable_value(parent, nodeid:str, value):
    '''set the value of a variable/property'''
    variable = server.get_node(nodeid)
    old_value = variable.get_attribute(ua.AttributeIds.Value).Value
    value_type = old_value.VariantType

    if isinstance(value, (list, tuple)):
        if value_type == ua.VariantType.Int32:
            value = list(map(lambda x: int(x), value))
        elif value_type in (ua.VariantType.Float, ua.VariantType.Double):
            value = list(map(lambda x: float(x), value))
        val = value[0] if len(value)>0 else None
    else:
        val = value

    def set():
        server.get_node(nodeid).set_attribute(ua.AttributeIds.Value, ua.DataValue(value))
        return True

    if isinstance(val, bool) :
        if value_type == ua.VariantType.Boolean:
            value = ua.Variant(value, ua.VariantType.Boolean) 
            return set()   
    elif isinstance(val, int):
        if value_type == ua.VariantType.Int32:
            value = ua.Variant(value, ua.VariantType.Int32)
            return set()
    elif isinstance(val, str): 
        if value_type == ua.VariantType.String:
            value = ua.Variant(value, ua.VariantType.String)
            return set()
    elif isinstance(val, float):
        if value_type in (ua.VariantType.Float, ua.VariantType.Double):
            value = ua.Variant(value, ua.VariantType.Float)
            return set()
    #log
    return False




if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)

    server = Server()
    uri = "opc.tcp://localhost:4847"
    server.set_endpoint(uri)
    server.set_server_name("Day8")
    name_space_index = server.register_namespace(uri)

    #create folders
    component_folder = server.get_root_node().add_folder(name_space_index, "OEP")
    workspace_folder = component_folder.add_folder(name_space_index, "Workspace")
    types_folder = component_folder.add_folder(name_space_index, "Types")

  
    oep_file_type = types_folder.add_object_type(name_space_index,"OepFileType")
    oep_file_type.add_reference(ua.NodeId(identifier= ua.ObjectIds.FileType), ua.ObjectIds.HasSubtype,forward=False)
    method1 = oep_file_type.add_method(name_space_index,"function", set_variable_value, [ua.VariantType.String, ua.VariantType.Null], [ua.VariantType.Boolean])
    prop = oep_file_type.add_property(name_space_index, "state", 0, varianttype=ua.VariantType.Int32)
    prop.set_modelling_rule(True)
    var = oep_file_type.add_variable(name_space_index, "age", 34, varianttype=ua.VariantType.Int32)
    var.set_modelling_rule(True)

    
    my_file = workspace_folder.add_object(name_space_index, "MyFile", objecttype=oep_file_type)
    
    server.start()

    def str_2_array(string, func, uatype):
        if len(string)>2:
            return [func(x, uatype) for x in string.strip('[').strip(']').split(',')] 
        else:
            return []

    def convert(string:str, uatype=0):
        try:
            if uatype == ua.VariantType.String.value:
                value = str(string)
            elif uatype in (ua.VariantType.Double.value, ua.VariantType.Float.value) :
                value = float(string)
            elif uatype in (ua.VariantType.Int32.value, ua.VariantType.Int64.value):
                value = int(string)
            elif uatype == ua.VariantType.Boolean.value:
                if string == 'True':
                    value = True
                elif string == 'False':
                    value = False
                else:
                    value = bool(string)
            else:
                value = None
        except ValueError as e:
            print(e)
            return None 
        return value

    def str_to_py_value(string:str, uatype=0, value_rank=-1):
        if value_rank == -1:
            value = convert(string, uatype)
        else:
            value = []
            if len(string)>2:
                value = [convert(x, uatype) for x in string.strip('[').strip(']').split(',')]      
        return value

    t = str_to_py_value('[0.0,0.0,0.0,0.0,0.2,44.7]',uatype=10, value_rank=0) 
    print(t)  
    print('done')
    # s = func
    # print(s.__name__)
    # print(my_file.nodeid.to_string())


    # variabl = my_file.add_variable(name_space_index, 'newAdded', 4,  varianttype=ua.VariantType.Int32)
    # variabl.set_value(ua.Variant([1,4], ua.VariantType.Int32))
    # try:
    #     my_file.call_method(method1, variabl.nodeid.to_string() , 34)
    # except Exception as e:
    #     print(e)
    
    # for p in my_file.get_variables():
    #     #print(p.set_value([2,4,5,6]))
    #     print(p.get_attribute(ua.AttributeIds.Value))
    #     print(p.get_attribute(ua.AttributeIds.Value).Value.is_array)
   

    #my_file.get_children()
    #node = server.get_node(my_file.get_type_definition())
    #methods = node.get_referenced_nodes(direction=ua.BrowseDirection.Inverse, nodeclassmask=ua.NodeClass.ObjectType).pop()
    # print(my_file.get_referenced_nodes())
    # print(my_file.get_type_definition())
    # print()
    
    # for m in methods.get_methods():
    #     print(m.get_browse_name())