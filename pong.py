import turtle

#screen
sc = turtle.Screen()
sc.title("Pong")
sc.bgcolor("black")
sc.setup(width=1000, height=1000)

#left paddle
left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape("square")
left_pad.color("white")
left_pad.shapesize(stretch_wid=6, stretch_len=2)
left_pad.penup()
left_pad.goto(-400,0)

#right paddle
right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape("square")
right_pad.color("white")
right_pad.shapesize(stretch_wid=6, stretch_len=2)
right_pad.penup()
right_pad.goto(400,0)

#ball
ball = turtle.Turtle()
ball.speed(40)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0,0)
ball.dx = 5
ball.dy =-5

#start score
left_player = 0
right_player = 0

# Displays the score 
sketch = turtle.Turtle() 
sketch.speed(0) 
sketch.color("white") 
sketch.penup() 
sketch.hideturtle() 
sketch.goto(0, 260) 
sketch.write("Player 1 : 0    Player 2 : 0", 
             align="center", font=("Courier", 24, "normal"))

#paddle movement
def paddle1Up():
    y = left_pad.ycor()
    y += 20
    left_pad.sety(y)

def paddle1Down():
    y = left_pad.ycor()
    y -= 20
    left_pad.sety(y)

def paddle2Up():
    y = right_pad.ycor()
    y += 20
    right_pad.sety(y)

def paddle2Down():
    y = right_pad.ycor()
    y -= 20
    right_pad.sety(y)

#keybinds
sc.listen()
sc.onkeypress(paddle1Up, "w")
sc.onkeypress(paddle1Down, "s")
sc.onkeypress(paddle2Up, "Up")
sc.onkeypress(paddle2Down, "Down")

while True:
    sc.update()

    ball.setx(ball.xcor()+ball.dx)
    ball.sety(ball.ycor()+ball.dy)

    #border check
    if ball.ycor() > 280:
        ball.sety(-280)
        ball.dy *= -1

    if ball.ycor() < -280:
        ball.sety(-280)
        ball.dy *= -1
    
    if ball.xcor() > 500:
        ball.goto(0,0)
        ball.dy *= -1
        left_player += 1
        sketch.clear()
        sketch.write("PLayer 1 : {} Player 2 : {}".format(
            left_player, right_player), align="center", 
            font=("Courier", 24, "normal"))

    if ball.xcor() < -500: 
        ball.goto(0, 0) 
        ball.dy *= -1
        right_player += 1
        sketch.clear() 
        sketch.write("Player 1 : {}    Player 2 : {}".format( 
                                 left_player, right_player), align="center", 
                                 font=("Courier", 24, "normal")) 
  
    # Paddle ball collision 
    if ((ball.xcor() > 360 and
                    ball.xcor() < 370) and
                    (ball.ycor() < right_pad.ycor()+40 and
                    ball.ycor() > right_pad.ycor()-40)): 
        ball.setx(360) 
        ball.dx*=-1
         
    if ((ball.xcor()<-360 and 
                    ball.xcor()>-370) and 
                    (ball.ycor()<left_pad.ycor()+40 and 
                    ball.ycor()>left_pad.ycor()-40)): 
        ball.setx(-360) 
        ball.dx*=-1