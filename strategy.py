import abc

#Interface
class AbsStrategy(abc.ABCMeta):

    @abc.abstractmethod
    def calculate(self,order):
        pass

#context
class ShippingCost(object):
    def __init__(self, strategy:AbsStrategy):
        self._strategy = strategy
    
    def shipping_cost(self,order):
        return self._strategy.calculate(self,order)



#concrete strategies
class UPS(AbsStrategy):
    def calculate(self,order):
        return order*2    

class DHL(AbsStrategy):
    def calculate(self,order):
        return order 

if __name__ == '__main__':
    #implementation
    shop_cost = ShippingCost(DHL)
    dhl =shop_cost.shipping_cost(4)
    print(dhl)

    shop_cost = ShippingCost(UPS)
    ups =shop_cost.shipping_cost(4)
    print(ups)