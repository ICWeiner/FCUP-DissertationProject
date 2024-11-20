class Shape():
    def __init__(self,color):
        self.color = color
    
    def foo(self):
        print("This is FOO")

    def printColor(self):
        print(self.color)

class Square(Shape):
    def __init__(self, color, side):
        super().__init__(color)
        self.side = side
    
    def printSide(self):
        print(self.side)

def test():
    return "OLA"

shape = Shape("Red")

square = Square("Blue",5)

shape.printColor()

square.printColor()

square.printSide()

square.foo()
    