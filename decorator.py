from functools import wraps
   

def good_decorator(function):
    @wraps(function)
    def inner(self):
        return function(self) + ' good'
    return inner





def require_validation():
    def decorator(function):
        def inner(t):
            glob = t
            if glob:
                return function(t)
            else:
                return False
        return inner
    return decorator

@require_validation()
def hello(t):
    return "Text"



def children_nodes_iterrator(gen_list:list, server,G,  function_of_node,get_child_nodes_generator, returns=None, **function_params):
    '''Iterrates recusively through childrens of a node and apply a function_of_node to each child
    Arguments:
    gen_list -- liat of generator objects
    function_of_node -- function to be applied to each node
    returns -- string key of the returned parameter, must be in function_params
    '''
    def inner():
        if len(gen_list) > 0:
            child_gen_list = []
            for generator in gen_list:
                for child_node in generator:
                    #apply function on child object
                    try:
                        function_of_node(child_node, server=server, **function_params)#server, tree=tree
                        #create generatoer list for the child object
                        child_gen_list.append(get_child_nodes_generator(child_node, server))
                    except Exception as e:
                        G.LOGGER.error("[children_nodes_iterrator] Error while running function {0}: {1}".format(function_of_node,e))

            else: 
                children_nodes_iterrator(child_gen_list, server, function_of_node, returns, **function_params)
        if returns is not None:
            return function_params[returns]
    return inner


def function_locals(x):
    print(locals())
    x = 4
    return locals()





if __name__ == '__main__':
    r = function_locals(x=3)
    function_locals(r)