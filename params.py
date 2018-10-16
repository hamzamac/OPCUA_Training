#With list or tuples
def doer_function(x, *args):
    
    print(x*args[0])


def itrerator(maxx, func, *args):
    for x in range(maxx):
        func(x, args)


#with dictionaries
def doer_func(x, numerator=1, denominator=1):
    
    print(x*numerator/denominator)


def itre(maxx, func, **param):
    for x in range(maxx):
        param['numerator']=6
        func(x, **param)

if __name__ == '__main__':
    #With list or tuples
    #itrerator(3, doer_function, 2)

    #with dictionaries
    #
    itre(4, doer_func, numerator=4, denominator=2)