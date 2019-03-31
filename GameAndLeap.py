################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import os, sys, inspect, thread, time, random, pygame
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
#arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
BALL_SIZE = 30
BRICK_SIZE = 50
_image_library = {}
_sound_library = {}
ball_list = []
brick_list = []
pig_list = []



class Ball:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0

class Brick:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0


class Pig:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self):
        self.x = 0
        self.y = 0

class scoreTracking:
    score = 0
    lives = 3
    handStatus =  'open' # fist, pinch, open

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # Get hands
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"
    #        print "%s, grab strength %f, pinch strength %f, palm position: %s" % (
    #        handType, hand.grab_strength, hand.pinch_strength, hand.palm_position[0])
            for pig in pig_list:
                # Move the ball's center
                pig.x = hand.palm_position[0]+275
            if hand.grab_strength >= 0.8:
                #print "closed fist"
                scoreTracking.handStatus = 'fist'
                print scoreTracking.handStatus
            if hand.pinch_strength >= 0.8 and hand.grab_strength <= 0.8:
                #print "good pinch"
                scoreTracking.handStatus = 'pinch'
                print scoreTracking.handStatus
            if hand.grab_strength <= 0.2 and hand.pinch_strength <= 0.2:
            #    print "open hand"
                scoreTracking.handStatus = 'open'
                print scoreTracking.handStatus


    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


def play_sound(path):
  global _sound_library
  sound = _sound_library.get(path)
  if sound == None:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    sound = pygame.mixer.Sound(canonicalized_path)
    _sound_library[path] = sound
  sound.play()


def make_ball():
    """
    Function to make a new, random ball.
    """
    ball = Ball()
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.

    ball.y = 0
    ball.x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)

    # Speed and direction of rectangle
    ball.change_x = 0
    ball.change_y = 2

    return ball

def make_brick():
    """
    Function to make a new, random ball.
    """
    brick = Brick()
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.

    brick.y = 0
    brick.x = random.randrange(BRICK_SIZE, SCREEN_WIDTH - BRICK_SIZE)

    # Speed and direction of rectangle
    brick.change_x = 0
    brick.change_y = 2

    return brick

def make_pig():
    """
    Function to make a new, random ball.
    """
    pig = Pig()
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    pig.x = 250
    pig.y = 400


    return pig

def main():

    pygame.init()
    start = time.time()
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    scoring = scoreTracking()


    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Bouncing Balls")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()


    ball = make_ball()
    ball_list.append(ball)

    brick = make_brick()
    brick_list.append(brick)

    pig = make_pig()
    pig_list.append(pig)

    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        if time.time()-start> 2:
                start= time.time()
                chance = random.randrange(0,2)
                print chance
                if chance >0:
                    ball = make_ball()
                    ball_list.append(ball)
                else:
                    brick = make_brick()
                    brick_list.append(brick)


        # --- Logic
        for ball in ball_list:
            # Move the ball's center
            ball.x += ball.change_x
            ball.y += ball.change_y

        for brick in brick_list:
            # Move the ball's center
            brick.x += brick.change_x
            brick.y += brick.change_y



         # --- Drawing
        # Set the screen background
        #screen.fill(BLACK)
        screen.blit(pygame.transform.scale(get_image('Bg.png'),(SCREEN_WIDTH,SCREEN_HEIGHT)),(0,0))
        basicfont = pygame.font.SysFont(None, 32)
        livesText = 'Lives: %.0f' % (scoring.lives)
        scoreText = 'Score: %.0f' % (scoring.score)

        textL = basicfont.render(livesText, True, (0, 0, 0), (255, 255, 255))
        textS = basicfont.render(scoreText, True, (0, 0, 0), (255, 255, 255))

        screen.blit(textL, (0, 0))
        screen.blit(textS, (560, 0))

        # Draw the balls
        for ball in ball_list:
           # pygame.image.load(os.path.join('Images', 'coin.png')) #pygame.draw.circle(screen, (255, 255, 255), [ball.x, ball.y], BALL_SIZE)
             screen.blit(pygame.transform.scale(get_image('coin.png'),(30,30)),(ball.x, ball.y))
             if (ball.x>pig.x and ball.x<pig.x+60 and ball.y>pig.y and ball.y<pig.y+60 and scoreTracking.handStatus=='fist'):
                 scoring.score += 10;
                 print "points scored"
                 play_sound('chaching.wav')

        # Draw the bricks
        for brick in brick_list:
            #pygame.draw.circle(screen, (255, 255, 255), [ball.x, ball.y], BALL_SIZE)
            screen.blit(pygame.transform.scale(get_image('brick.png'),(50,50)),(brick.x, brick.y))
            if (brick.x>pig.x and brick.x<pig.x+60 and brick.y>pig.y and brick.y<pig.y+60):
                scoring.lives -= 0.035
                print "lost a life"
                play_sound('brickbreak.wav')
                if scoring.lives <= 0:
                    screen.fill(BLACK)
                    done = True


        for pig in pig_list:
           #pygame.draw.circle(screen, (255, 255, 255), [ball.x, ball.y], BALL_SIZE)
           screen.blit(pygame.transform.scale(get_image('pig.png'),(125,100)),(pig.x, pig.y))



        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Close everything down
    pygame.quit()


    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
