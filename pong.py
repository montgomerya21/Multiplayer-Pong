import turtle
import socket
import threading
from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls') #windows OS
    else:
        _ = system('clear') #other OS

isHost = 'h' == input("Host or Client: ")[0].lower()

if (isHost):
    clear()
    HOST_ADDR = input("Enter IP address: ")
    HOST_PORT = int(input("Enter port: "))

    #start the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(1)
    clear()
    print("Give your IP and Port to a friend to begin playing \n")
    print("IP: " + HOST_ADDR)
    print("Port: " + str(HOST_PORT) + "\n")
    print("Waiting for other player to connect...")

    connected = False

    #waits for client to connecct
    while True:
        client_socket, client_address = server.accept()
        break

else:
    clear()
    while True:
        HOST_ADDR = input("Enter IP address: ")
        HOST_PORT = int(input("Enter port: "))
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST_ADDR, HOST_PORT))
            break
        except Exception as e:
            clear()
            print("Could not connect\n")

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

#host paddle
def paddle1Up():
    y = left_pad.ycor()
    y += 20
    left_pad.sety(y)

def paddle1Down():
    y = left_pad.ycor()
    y -= 20
    left_pad.sety(y)

#client paddle
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

#Host controls paddle1 while client controls paddle2
#both players use W for up and S for down
if (isHost):
    sc.onkeypress(paddle1Up, "w")
    sc.onkeypress(paddle1Down, "s")
else:
    sc.onkeypress(paddle2Up, "w")
    sc.onkeypress(paddle2Down, "s")

while True:
    sc.update()
    if isHost:
        ball.setx(ball.xcor()+ball.dx)
        ball.sety(ball.ycor()+ball.dy)
    
    #sending position data
    if (isHost):
        #this will be the send that is used I just commented it out to get the paddles to work with an alternate send
        #client_socket.send((str(left_pad.ycor()) + '%' + str(ball.xcor()) + '%' + str(ball.ycor())).encode())

        #this is an alternate send that only sends paddle info
        client_socket.send(str(left_pad.ycor()).encode())
        player2Update = client_socket.recv(HOST_PORT).decode()
        right_pad.sety(int(player2Update))
    else:
        from_host = client.recv(HOST_PORT).decode()
        client.send(str(right_pad.ycor()).encode())
        updateValues = from_host.split('%')
        left_pad.sety(int(updateValues[0]))
        #ball.setx(int(updateValues[1]))
        #ball.sety(int(updateValues[2]))

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