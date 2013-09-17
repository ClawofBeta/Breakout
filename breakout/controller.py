#Extensions: I improved the user control bounces, exactly as it says on the assignment:
#For example, suppose the ball is coming down toward the right (or left).
#If it hits the left (or right) 1/4 of the paddle, the ball goes back the way it came (both vx and vy are negated).

#I also implemented sound effects when the ball hits a boundary, paddle, or a brick.

#I increase the speed of the ball by 2% everytime it hits the paddle

#I added a lives scoreboard and a score scoreboard at the top of the screen.

# controller.py
# Andrew Ou (aco43)
# 11/28/12
"""Controller module for Breakout

This module contains a class and global constants for the game Breakout.
Unlike the other files in this assignment, you are 100% free to change
anything in this file. You can change any of the constants in this file
(so long as they are still named constants), and add or remove classes."""
import colormodel
import random
from graphics import *

# CONSTANTS

# Width of the game display (all coordinates are in pixels)
GAME_WIDTH  = 480
# Height of the game display
GAME_HEIGHT = 620

# Width of the paddle
PADDLE_WIDTH = 58
# Height of the paddle
PADDLE_HEIGHT = 11
# Distance of the (bottom of the) paddle up from the bottom
PADDLE_OFFSET = 30

# Horizontal separation between bricks
BRICK_SEP_H = 5
# Vertical separation between bricks
BRICK_SEP_V = 4
# Height of a brick
BRICK_HEIGHT = 8
# Offset of the top brick row from the top
BRICK_Y_OFFSET = 70

# Number of bricks per row
BRICKS_IN_ROW = 10
# Number of rows of bricks, in range 1..10.
BRICK_ROWS = 10
# Width of a brick
BRICK_WIDTH = GAME_WIDTH / BRICKS_IN_ROW - BRICK_SEP_H

# Diameter of the ball in pixels
BALL_DIAMETER = 18

# Number of attempts in a game
NUMBER_TURNS = 3

# Basic game states
# Game has not started yet
STATE_INACTIVE = 0
# Game is active, but waiting for next ball
STATE_PAUSED   = 1
# Ball is in play and being animated
STATE_ACTIVE   = 2
# Game is over, deactivate all actions
STATE_COMPLETE = 3

# ADD MORE CONSTANTS (PROPERLY COMMENTED) AS NECESSARY

# Distance from the left side of the paddle from the left side of the screen.
# Invariant: Must be a pixel location lower than (GAME_WIDTH - PADDLE_WIDTH)
# and greater than 0.
DEFAULT_X = 210

# Default distance from the left side of the ball to the left side of the wall
# Invariant: Must be a pixel location lower than (GAME_WIDTH - BALL_DIAMETER)
# and greater than 0
BALL_X = 225

# Default distance from the bottom of the ball to the bottom wall
# Invariant: Must be a pixel location lower than (GAME_HEIGHT - BALL_DIAMETER)
# and greater than 0.
BALL_Y = 200


# CLASSES
class Breakout(GameController):
    """Instance is the primary controller for Breakout.

    This class extends GameController and implements the various methods
    necessary for running the game.

        Method initialize starts up the game.

        Method update animates the ball and provides the physics.

        The on_touch methods handle mouse (or finger) input.

    The class also has fields that provide state to this controller.
    The fields can all be hidden; you do not need properties. However,
    you should clearly state the field invariants, as the various
    methods will rely on them to determine game state."""
    # FIELDS.

    # Current play state of the game; needed by the on_touch methods
    # Invariant: One of STATE_INACTIVE, STATE_PAUSED, STATE_ACTIVE
    _state  = STATE_INACTIVE

    # List of currently active "bricks" in the game.
    #Invariant: A list of  objects that are instances of GRectangle (or a
    #subclass) If list is  empty, then state is STATE_INACTIVE (game over)
    _bricks = []

    # The player paddle
    # Invariant: An object that is an instance of GRectangle (or a subclass)
    # Also can be None; if None, then state is STATE_INACTIVE (game over)
    _paddle = None

    # The ball to bounce about the game board
    # Invariant: An object that is an instance of GEllipse (or a subclass)
    # Also can be None; if None, then state is STATE_INACTIVE (game over) or
    # STATE_PAUSED (waiting for next ball)
    _ball = None

    # ADD MORE FIELDS (AND THEIR INVARIANTS) AS NECESSARY
    # Invariant: Holds a GLabel object that is a string which is the welcome message.
    # Also can be None to prevent the view window from messing up.
    _welcome = None
        
    # Determines if the mouse has clicked inside the paddle or not
    # Credits to https://piazza.com/class#fall2012/cs1110/683
    # Invariant: A boolean which is True if the paddle has been clicked, False otherwise
    _click = False
    
    # Invariant: Holds a GLabel object that is a string which is the amount of lives the user has
    # Also can be none to show that it hasnt' been initialized yet
    _lifeLabel = None
    
    # The amount of lives the user has. The default is 3, and if 0, then the game is over.
    # Player loses a life whenever the ball goes over the bottom boundary.
    #Invariant: An int that is >=0.
    _life = NUMBER_TURNS
   
    # Invariant: Holds a GLabel object that is a string
    #which is the message when the player loses a life
    # Also can be None, which indicates the user hasn't lost a life yet.
    _lostLife = None

    # Invariant: Holds a GLabel object that is a string which is the score
    # Also can be none to show that it hasnt' been initialized yet
    _score = None
    
    # Invariant: Holds an integer which is the user's score
    # Starts at 0 and increases by 10 for every block the user gets.
    # Decreases by 100 whenever the user loses a life.
    _intScore = 0

    # METHODS
    def initialize(self):
        """Initialize the game state.

        Initialize any state fields as necessary to statisfy invariants.
        When done, set the state to STATE_INACTIVE, and display a message
        saying that the user should press to play a game."""
        # IMPLEMENT ME
        self._welcomeScreen()
        self._state = STATE_INACTIVE
        
    def update(self, dt):
        """Animate a single frame in the game.

        This is the method that does most of the work.  It moves the ball, and
        looks for any collisions.  If there is a collision, it changes the
        velocity of the ball and removes any bricks if necessary.

        This method may need to change the state of the game.  If the ball
        goes off the screen, change the state to either STATE_PAUSED (if the
        player still has some tries left) or STATE_COMPLETE (the player has
        lost the game).  If the last brick is removed, it needs to change
        to STATE_COMPLETE (game over; the player has won).

        Precondition: dt is the time since last update (a float).  This
        parameter can be safely ignored."""
        # IMPLEMENT ME
        if self._score != None:
            self._score.text = ('Score: ' + `self._intScore`)
        if self._lifeLabel != None:
            self._lifeLabel.text = ('Lives: ' + `self._life`)
        if self._ball != None:
            self._ball.center_x = self._ball._vx + self._ball.center_x
            self._ball.center_y = self._ball._vy + self._ball.center_y
            self._checkBoundaries(self._ball)
        collidedObject = self._getCollidingObject()
        if collidedObject == self._paddle:
            self._paddleCollision()
        elif isinstance(collidedObject, GRectangle):
            self._blockCollision(collidedObject)
        if len(self._bricks) == 0 and self._state == STATE_ACTIVE:
            self._victory()
            self._state = STATE_COMPLETE

    def on_touch_down(self,view,touch):
        """Respond to the mouse (or finger) being pressed (but not released)

        If state is STATE_ACTIVE or STATE_PAUSED, then this method should
        check if the user clicked inside the paddle and begin movement of the
        paddle.  Otherwise, if it is one of the other states, it moves to the
        next state as appropriate.

        Precondition: view is just the view attribute (unused because we have
        access to the view attribute).  touch is a MotionEvent (see
        documentation) with the touch information."""
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE:
            self.view.remove_widget(self._welcome)
            self._state = STATE_PAUSED
            self._placeBricks()
            self._score = GLabel(text = 'Score: ' + `self._intScore`)
            self._score.center= (400, 625)
            self._score.font_size = 20
            self.view.add_widget(self._score)
            self._lifeLabel = GLabel(text = 'Lives: ' + `self._life`)
            self._lifeLabel.center= (75, 625)
            self._lifeLabel.font_size = 20
            self.view.add_widget(self._lifeLabel)
            self._makePaddle()
            self.delay(self._makeBall, 3)
            self._state == STATE_ACTIVE

    def on_touch_move(self,view,touch):
        """Respond to the mouse (or finger) being moved.

        If state is STATE_ACTIVE or STATE_PAUSED, then this method should move
        the paddle. The distance moved should be the distance between the
        previous touch event and the current touch event. For all other
        states, this method is ignored.

        Precondition: view is just the view attribute (unused because we have
        access to the view attribute).  touch is a MotionEvent (see
        documentation) with the touch information."""
        # IMPLEMENT ME
        if self._state == STATE_PAUSED or self._state == STATE_ACTIVE:
            if (self._paddle.collide_point(touch.x, touch.y) == True):
                self._click = True
            self._controlPaddle(touch.x, touch.y)

    def on_touch_up(self,view,touch):
        """Respond to the mouse (or finger) being released.

        If state is STATE_ACTIVE, then this method should stop moving the
        paddle. For all other states, it is ignored.

        Precondition: view is just the view attribute (unused because we have
        access to the view attribute).  touch is a MotionEvent (see
        documentation) with the touch information."""
        # IMPLEMENT ME
        self._click = False

    # ADD MORE HELPER METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def _welcomeScreen(self):
        """Displays the welcome screen
        
        On program startup, a welcome screen saying 'Welcome to Breakout!'
        along with 'Partially Programmed by Andrew Ou' in addition to a 
        'Click the paddle to control it' and a 'Click the screen to start.' with a
        'FYI the ball will drop after 3 seconds.' will be displayed"""
        self._welcome = GLabel(text='Welcome to Breakout!' +
                               '\n\nPartially Programmed by Andrew Ou' +
                               '\nClick the paddle to control it.'
                               +'\nClick the screen to start.'
                               +'\nFYI the ball will drop after 3 seconds.')
        self._welcome.halign = 'center'
        self._welcome.center=(230, 400)
        self._welcome.font_size = 20
        self.view.add_widget(self._welcome)
        
    def _makeBall(self):
        """Makes the ball
        
        The ball is BALL_DIAMETER in diameter. It starts in the (BALL_X, BALL_Y) in the game display."""
        self._ball = Ball(pos = (BALL_X, BALL_Y), size = (BALL_DIAMETER, BALL_DIAMETER))
        self.view.add(self._ball)
        self._state = STATE_ACTIVE
        
    def _makePaddle(self):
        """Makes the paddle
        
        The paddle is PADDLE_WIDTH long and PADDLE_HEIGHT high. The distance from the bottom of
        the screen to bottom of the paddle is PADDLE_OFFSET. The paddle starts at the DEFAULT_X
        x-coordinate."""
        self._paddle = GRectangle(pos = (DEFAULT_X, PADDLE_OFFSET), size = (PADDLE_WIDTH, PADDLE_HEIGHT))
        self.view.add(self._paddle)

    def _placeBricks(self):
        """Places bricks down
        
        There are BRICKS_IN_ROW bricks per row that are each BRICK_HEIGHT high and BRICK_WIDTH long.
        They are each separated horizontally BRICK_SEP_H and vertically BRICK_SEP_V. There are
        BRICK_ROWS rows of bricks. The top row of bricks
        is BRICK_Y_OFFSET from the top.
        
        The color of bricks remains constant for two rows and run in the following sequence:
        RED, ORANGE, YELLOW, GREEN, CYAN. If there are more than ten rows, the sequence is repeated."""
        column = 0
        row = 0
        x = BRICK_SEP_H / 2
        y = GAME_HEIGHT - BRICK_Y_OFFSET
        while row < BRICK_ROWS:
            while column < BRICKS_IN_ROW:
                color = self._determineColor(row)
                brick = GRectangle(pos =(x, y), size = (BRICK_WIDTH, BRICK_HEIGHT), fillcolor = color)
                self.view.add(brick)
                self._bricks.append(brick)
                x = x + BRICK_WIDTH + BRICK_SEP_H
                column = column + 1
            
            column = 0
            x = BRICK_SEP_H /    2
            y = y - BRICK_SEP_V - BRICK_HEIGHT
            row = row + 1
    
    def _determineColor(self, row):
        """Determines the color of the row.
        
        The color of bricks remains constant for two rows and run in the following sequence:
        RED, ORANGE, YELLOW, GREEN, CYAN. If there are more than ten rows, the sequence is repeated."""
        
        number = row % 10
        if number == 0 or number == 1:
            return colormodel.RED
        elif number == 2 or number ==3:
            return colormodel.ORANGE
        elif number == 4 or number ==5:
            return colormodel.YELLOW
        elif number ==6 or number ==7:
            return colormodel.GREEN
        else:
            return colormodel.CYAN
        
    def _controlPaddle(self, x, y):
        """Determines how the paddle moves.
        
        The x-position of the paddle's center aligns with the current touch position."""
        if (x < GAME_WIDTH and x > 0 and self._click == True):
            self._paddle.center_x = (x)
            
    def _checkBoundaries(self, ball):
        """Changes the velocity of ball if it hits the side of the game.
        
        If any part of ball goes over a boundary,
        then the velocity is reversed to the opposite direction. If the ball goes over
        a bottom boundary, the game is reset.
        Also, when a side boundary is hit, saurcer1.wav is played, and when the top
        boundary is hit, saucer2.wav is played"""
        if ball.right >= GAME_WIDTH:
            ball._vx = -ball._vx
            bounceSound = Sound('saucer1.wav')
            bounceSound.play()
        if ball.top  >= GAME_HEIGHT:
            ball._vy = -ball._vy
            bounceSound = Sound('saucer2.wav')
            bounceSound.play()
        if ball.x <= 0:
            ball._vx = -ball._vx
            bounceSound = Sound('saucer1.wav')
            bounceSound.play()
        if ball.y <= 0:
            self._resetGame()
            
    def _resetGame(self):
        """When the ball crosses the bottom boundary, the game is reset, unless _life is
        0. Then the game is over.
        
        Whenever the ball crosses the bottom boundary _life is decreased by one, and the ball
        is returned to the center and dropped after 3 seconds."""
        self._life = self._life - 1
        self.view.remove(self._ball)
        self._ball = None
        self.view.remove(self._paddle)
        self._paddle = None
        if self._life == 0 and self._state != STATE_COMPLETE:
            self._state = STATE_COMPLETE
            gameOver = GLabel(text = 'Game Over! You just lost the Game!')
            gameOver.halign = 'center'
            gameOver.center=(230, 300)
            gameOver.font_size = 20
            self.view.add_widget(gameOver)
            
        else:
            if self._state != STATE_COMPLETE:
                self._state = STATE_PAUSED
                self._makePaddle()
                self._loseLife()
                self.delay(self._makeBall, 3)
                self.delay(self._removeLoseLife, 3)
                self._state = STATE_ACTIVE
            
    def _loseLife(self):
        """Displays the _loseLife message onto the screen.
        
        Displays 'You just lost a life!
                You have ' + `self._life` + more!
                You have 3 seconds
                to get ready for your next try!'
        The amount of points is also decreased by 100 whenver a live is lost."""
        self._lostLife = GLabel(text = 'You just lost a life! \nYou have ' + `self._life` +
        ' more!\n You have 3 seconds \nto get ready for your next try!')
        self._lostLife.halign = 'center'
        self._lostLife.center=(230, 300)
        self._lostLife.font_size = 20
        self.view.add_widget(self._lostLife)
        self._intScore = self._intScore - 100
    
    def _removeLoseLife(self):
        """Removes the _loseLife message from the screen.
        
        This method's only purpose is to make delay work properly."""
        self.view.remove_widget(self._lostLife)
        
    def _victory(self):
        """Shows that the user has won.
        
        Displays the victory label which says 'You just won the Game!
                                                 'Wait. No. You lost. I dunno.')"""
        victory = GLabel(text = 'You just won the Game! \nWait. No. You lost. I dunno.')
        victory.halign = 'center'
        victory.center=(230, 300)
        victory.font_size = 20
        self.view.add_widget(victory)

    def _getCollidingObject(self):
        """Returns: GObject that has collided with the ball
    
        This method checks the four corners of the ball, one at a 
        time. If one of these points collides with either the paddle 
        or a brick, it stops the checking immediately and returns the 
        object involved in the collision. It returns None if no 
        collision occurred."""
        if (self._ball != None):
            xRight = self._ball.x + BALL_DIAMETER
            xLeft = self._ball.x
            yTop = self._ball.y + BALL_DIAMETER
            yBot = self._ball.y
        
            if (self._paddle != None):
                if self._paddle.collide_point(xRight, yTop) == True:
                    return self._paddle
                if self._paddle.collide_point(xLeft, yTop) == True:
                    return self._paddle
                if self._paddle.collide_point(xRight, yBot) == True:
                    return self._paddle
                if self._paddle.collide_point(xLeft, yBot) == True:
                    return self._paddle
                
                if (self._bricks != None):
                    x = 0
                    while x < len(self._bricks):
                        if self._bricks[x].collide_point(xRight, yTop) == True:
                            return self._bricks[x]
                        if self._bricks[x].collide_point(xLeft, yTop) == True:
                            return self._bricks[x]
                        if self._bricks[x].collide_point(xRight, yBot) == True:
                            return self._bricks[x]
                        if self._bricks[x].collide_point(xLeft, yBot) == True:
                            return self._bricks[x]
                        x = x + 1
        return None
    
    def _paddleCollision(self):
        """Coordinates the interaction between the ball and a paddle
        
        If the ball has a downwards velocity when it hits the paddle, the
        velocity in the y direction switches to the opposite direction. Also, the
        velocity increases by 1.01x in both directions each time it hits the paddle.
        Whenever the ball hits the paddle it also plays bounce.wav"""
        if self._ball != None and self._ball._vy < 0:
            firstQuarterPaddle = self._paddle.x + (PADDLE_WIDTH * 0.25)
            thirdQuarterPaddle = self._paddle.x + (PADDLE_WIDTH * 0.75)
            bounceSound = Sound('bounce.wav')
            bounceSound.play()
            if self._ball.center_x < firstQuarterPaddle and self._ball._vx > 0:
                self._ball._vx = -self._ball._vx
                self._ball._vy = -self._ball._vy
                self._ball._vy = self._ball._vy * 1.02
                self._ball._vx = self._ball._vx * 1.02
            elif self._ball.center_x > thirdQuarterPaddle and self._ball._vx < 0:
                self._ball._vx = -self._ball._vx
                self._ball._vy = -self._ball._vy
                self._ball._vy = self._ball._vy * 1.02
                self._ball._vx = self._ball._vx * 1.02
            else:
                self._ball._vy = -self._ball._vy
                self._ball._vy = self._ball._vy * 1.02
                self._ball._vx = self._ball._vx * 1.02
            
    def _blockCollision(self, collidedBrick):
        """Coordinates the interaction between the ball and a block (collidedBrick)
        
        If the ball collides with a brick, then the brick is removed. Also, the
        velocity of the ball in the y direction switches to the opposite direction.
        plate1.wav is also played when the paddle is hit.
        The score is also increased by 10 whenever a block is hit."""
        if self._ball != None:
            bounceSound = Sound('plate1.wav')
            bounceSound.play()
            self._intScore = self._intScore + 10
            self._ball._vy = -self._ball._vy
            self.view.remove(collidedBrick) # Remove from view
            self._bricks.remove(collidedBrick) # Remove from controller
            
            
class Ball(GEllipse):
    """Instance is a game ball.

    We extends GEllipse because a ball does not just have a position; it
    also has a velocity.  You should add a constructor to initialize the
    ball, as well as one to move it.

    Note: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above."""
    # FIELDS.  You may wish to add properties for them, but that is optional.

    # Velocity in x direction.  A number (int or float)
    _vx = 0.0   
    # Velocity in y direction.  A number (int or float)
    _vy = -5.0

    # ADD MORE FIELDS (INCLUDE INVARIANTS) AS NECESSARY

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def __init__(self, **keywords):
        """Constructor: Creates a new Ball.
        
        Velocity is initially -5.0 in the y direction, and random in the x direction."""
        super(Ball, self).__init__(**keywords)
        self._vx = random.uniform(1.0,5.0)
        self._vx = self._vx * random.choice([-1, 1])
        self._vy = -5.0
    
# ADD MORE CLASSES AS NECESSARY