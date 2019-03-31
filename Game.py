import pygame
import random
import time
import os

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BALL_SIZE = 25
BRICK_SIZE = 25

# new code
_image_library = {}
_name_ = "_main_"


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


# new code
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image




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
    """
    This is our main program.
    """
    pygame.init()

    start = time.time()
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Bouncing Balls")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    ball_list = []

    ball = make_ball()
    ball_list.append(ball)

    brick_list = []

    brick = make_brick()
    brick_list.append(brick)

    pig_list = []

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
                    print
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

        for pig in pig_list:
            # Move the ball's center
            pig.x += 0#pig.change_x
            #pig.y += pig.change_y

         # --- Drawing
        # Set the screen background
        screen.fill(BLACK)

        # Draw the balls
        for ball in ball_list:
           # pygame.image.load(os.path.join('Images', 'coin.png')) #pygame.draw.circle(screen, (255, 255, 255), [ball.x, ball.y], BALL_SIZE)
             screen.blit(pygame.transform.scale(get_image('coin.png'),(30,30)),(ball.x, ball.y))

        # Draw the bricks
        for brick in brick_list:
            #pygame.draw.circle(screen, (255, 255, 255), [ball.x, ball.y], BALL_SIZE)
            screen.blit(pygame.transform.scale(get_image('brick.png'),(50,50)),(brick.x, brick.y))

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

if _name_ == "_main_":
    main()
