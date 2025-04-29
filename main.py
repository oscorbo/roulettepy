import pyglet
from pyglet.window import key
from pyglet.window import mouse
import random
import data
import math
import os

script_dir = os.path.dirname(__file__)
path = os.path.join(script_dir, 'images/')

window = pyglet.window.Window()

window.set_size(data.width, data.height)
window.maximize()

Batch = pyglet.graphics.Batch()

ball = pyglet.shapes.Circle(radius=10, x=data.center_x, y=data.center_y, batch=Batch)
path = os.path.join(script_dir, 'images/newrulet.png')

ruletimage = pyglet.image.load(path)
ruletimage.anchor_x = ruletimage.width // 2
ruletimage.anchor_y = ruletimage.height // 2

rulet = pyglet.sprite.Sprite(img=ruletimage, x=data.center_x, y=data.center_y, batch=Batch)
rulet.scale = .5

path = os.path.join(script_dir, 'images/deccider.png')
selectorimage = pyglet.image.load(path)
selectorimage.anchor_x = selectorimage.width // 2
selectorimage.anchor_y = selectorimage.height // 2

selector = pyglet.sprite.Sprite(img=selectorimage, x=data.center_x, y=data.center_y, batch=Batch)
selector.scale = .5
selector.opacity = 100

# Impact
label = pyglet.text.Label("osco game",
                          font_name='Times New Roman',
                          font_size=13,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center', batch=Batch)
label.opacity = 100



chances = [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,5,18,29,7,28,12,35,3,26,]

bit_of_chance = 360/len(chances)

# -.05
deacceleration_ball = -.05
# -20
multi = random.random()
print(multi)
angle_speed_ball = -7 * multi
angle_ball_teoric = bit_of_chance / 3
angle_ball_real = bit_of_chance / 3

deacceleration_rulet = 0.1
angle_speed_rulet = 2


@window.event
def on_key_press(symbol, modifiers):
    global angle_speed_ball, angle_ball_real, angle_ball_teoric

    if symbol == key.Y:
        angle_speed_ball = 0
        index = int((angle_ball_teoric + 360 + (0 * bit_of_chance / 3))/bit_of_chance)
        angle_ball_real = index * bit_of_chance + rulet.rotation + bit_of_chance / 3
        print(angle_ball_teoric, index, chances[index])
        selector.opacity = 150
    
    if symbol == key.I:
        angle_speed_ball = -7 * random.random()

# region mouse
@window.event
def on_mouse_press(x, y, button, modifiers):
    pass

@window.event
def on_mouse_release(x, y, button, modifiers):
    pass
# endregion

@window.event
def on_draw():
    window.clear()
    Batch.draw()

def update(dt):
    global angle_speed_rulet, angle_speed_ball, angle_ball_real, angle_ball_teoric
    rulet.rotation += angle_speed_rulet
    if not angle_speed_rulet < 0.5:
        angle_speed_rulet -= deacceleration_rulet

    if (angle_ball_teoric + angle_speed_ball) < -360:
        angle_ball_teoric += angle_speed_ball 
        angle_ball_teoric += 360

    angle_ball_real += angle_speed_rulet + angle_speed_ball
    angle_ball_teoric += angle_speed_ball
    ball.x = math.sin(angle_ball_real *  (3.14159 / 180)) * 275 + data.center_x
    ball.y = math.cos(angle_ball_real *  (3.14159 / 180)) * 275 + data.center_y

    selector.rotation = angle_ball_real - bit_of_chance / 3

    if selector.opacity != 0:
        selector.opacity /= 1.1

    if not angle_speed_ball >= 0:
        angle_speed_ball -= deacceleration_ball
    else: 
        angle_speed_ball = 0

    # print(angle_ball_teoric)

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()