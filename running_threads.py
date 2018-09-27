from threading import Thread
from time import sleep

class CookBook(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.message = "A threaded message"
    
    def preint_message(self):
        print(self.message)