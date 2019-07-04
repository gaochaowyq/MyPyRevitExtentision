class test(object):
    def what(self):
        print('what')

class test1(test):
    def never(self):
        print("bad")
        super().what()

class test2(test):

    def never(self):
        print("good")
        super().what()

class test3(object):
    def __new__(cls, *args, **kwargs):
        cls=test2
        return object.__new__(cls)
    def __init__(self,c):
        self.c=c
    def never(self):
        print(self.c)
        print(self.b)


c=test3(4)
c.never()