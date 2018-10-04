from decorator import good_decorator

class Father:
    def f_method(self):
        print("Father method")

class Mother:
    @good_decorator
    def m_method(self):
        return "Mother method"

class Child(Mother, Father):
    def c_method(self):
        print("Child method") 


if __name__ == "__main__":

    child = Child()
    child.f_method()
    print(child.m_method())
    child.c_method()
    #print(child.__getattribute__("p_method"))