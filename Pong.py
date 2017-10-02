# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = [[4, 0 ], [4, 80]]
paddle2_pos = [[596, 0], [596, 80]]
paddle1_vel = 0
paddle2_vel = 0
GO = 6
score_blue = 0
score_red = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    if direction == RIGHT:
        ball_vel = [random.randrange(120, 240) / 60, - random.randrange(60, 180) / 60]
    if direction == LEFT:
        ball_vel = [ - random.randrange(120, 240) / 60, - random.randrange(60, 180) / 60]
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(RIGHT)
    
def button_handler():
    global score_blue, score_red
    score_blue = 0
    score_red = 0
    new_game()
    

def keydown(key):
    global paddle1_vel, paddle2_vel 
    paddle1_vel = 0
    paddle2_vel = 0
    
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = GO
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -GO
    
    
    
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = GO
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -GO    
        
def keyup(key):
    global paddle1_vel, paddle2_vel
     
    
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0  
        
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
        
  
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, score_red, score_blue
    
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    #draw text
    c.draw_text(str(score_blue), (140, 50), 48, 'White')
    c.draw_text(str(score_red), (440, 50), 48, 'White')
    # update ball
    ball_pos[0] += ball_vel[0]    
    ball_pos[1] += ball_vel[1] 
    
    # Fof top and bottom
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if ball_pos[1] >= (HEIGHT - 1)- BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        
    # For gutter
                
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        
        if paddle1_pos[0][1] < ball_pos[1] < paddle1_pos[1][1]:
            ball_vel[0] = -ball_vel[0]
            ball_vel[1] += 1
            ball_vel[0] += 1
            
        else:
            spawn_ball(RIGHT)
            score_red += 1
    if ball_pos[0] >= (WIDTH - PAD_WIDTH - 1)- BALL_RADIUS:
        if paddle2_pos[0][1] < ball_pos[1] < paddle2_pos[1][1]:
            ball_vel[0] = -ball_vel[0]
            ball_vel[1] -= 1
            ball_vel[0] -= 1
            
        else:
            spawn_ball(LEFT)
            score_blue += 1
        
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 3, 'Blue', 'White')
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[0][1] <= 0:
        paddle1_pos[0][1] = paddle1_pos[0][1] + 1
        paddle1_pos[1][1] = paddle1_pos[1][1] + 1
    elif paddle1_pos[1][1] >= 400:
        paddle1_pos[0][1] = paddle1_pos[0][1] - 1
        paddle1_pos[1][1] = paddle1_pos[1][1] - 1
    else:
        paddle1_pos[0][1] = paddle1_pos[0][1] + paddle1_vel
        paddle1_pos[1][1] = paddle1_pos[1][1] + paddle1_vel
    
    if paddle2_pos[0][1] <= 0:
        paddle2_pos[0][1] = paddle2_pos[0][1] + 0.1
        paddle2_pos[1][1] = paddle2_pos[1][1] + 0.1
    elif paddle2_pos[1][1] >= 400:
        paddle2_pos[0][1] = paddle2_pos[0][1] - 0.1
        paddle2_pos[1][1] = paddle2_pos[1][1] - 0.1
    else:
        paddle2_pos[0][1] = paddle2_pos[0][1] + paddle2_vel
        paddle2_pos[1][1] = paddle2_pos[1][1] + paddle2_vel
        
    
    # draw paddles
    c.draw_polygon( paddle1_pos , 8, 'Blue')
    c.draw_polygon( paddle2_pos, 8, 'Red')
    

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)

frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_draw_handler(draw)
button = frame.add_button('Reset', button_handler)

# start frame
new_game()
frame.start()