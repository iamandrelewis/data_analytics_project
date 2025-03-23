import turtle
import random
import time

"""wn = turtle.Screen()
wn.bgcolor("light green")
wn.title("Turtle")
skk = turtle.Turtle()
skk.forward(100)    
turtle.done()"""

print("This program draws shapes based on the number you enter in a uniform pattern.")
num_str = input("Enter the side number of the shape you want to draw")
try:

    squares = int(num_str)
    angle = 180 -180 * (squares-2)/squares

    turtle.up
    x = 0
    y = 0
    turtle.setpos(x,y)

    numshapes = 8
    for x in range(numshapes):
        turtle.color(random.random(),random.random(),random.random())
        x+=5
        y+=5
        turtle.forward(x)
        turtle.left(y)
        for i in range(squares):
            turtle.begin_fill()
            turtle.down()
            turtle.forward(10)
            turtle.left(angle)
            turtle.forward(40)
            print(turtle.pos())
            turtle.up()
            turtle.end_fill()
    time.sleep(11)
    turtle.bye()
    class Player:
        def __init__(self,name,symbol):
            self.name = name
            self.symbol = symbol
except:
    print('Enter a valid number')