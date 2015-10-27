#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import random
from turtle import *
import time
import pygame
#  import os

class Timer(Frame):
    def __init__(self, master=None):

        Frame.__init__(self, master)

        # False = timer deactivated
        self.state = False
        self.box_game = False

        # Change to max resolution
        root.minsize(1920, 1080)
        root.maxsize(1920, 1080)

        # Full screen
        root.overrideredirect(1)

        # Saves each climber's score
        self.scores = {}

        # Allows first score to become high score
        self.last_score = 999

        # Tracks the lowest time
        self.highscore_var = StringVar()
        self.highscore_var.set('No Highscore')

        # Different pre-made dot arrangements, each time app is opened one will be chosen randomly
        # Images are in same directory as code (GIF ONLY)
      #  directory = os.getcwd()
        self.image_list = ['dots.gif', '4_up_left.gif', '5_up_left.gif', '6_up_left.gif']

        # Set background image
        self.this_image = random.choice(self.image_list)
        self.background_image = PhotoImage(file=self.this_image)
        self.background_label = Label(root, image=self.background_image)
        self.background_label.photo = self.background_image
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Time structure [min, sec, centsec]
        self.timer = [0, 0, 0]

        # Minutes are not used, but available for longer games
        self.pattern = '{1:02d}:{2:02d}'
        # self.pattern = '{0:02d}:{1:02d}:{2:02d}'

        # Display time
        self.timeText = Label(root, text='00:00', font=('Evogria', 60), foreground='white', background='black')
        self.timeText.pack(side='top', expand=False)

        # Display high score
        self.highscore = Label(root, textvariable=self.highscore_var, font=('Evogria', 20), foreground='yellow', background='black')
        self.highscore.pack(side='top', expand=False)

        # When space is pressed, timer starts/stops
        root.bind('<Tab>', self.start)
        root.bind('<Escape>', self.quit)
        root.bind('<Right>', self.next)
        root.bind('<Left>', self.next)
        root.bind('<Down>', self.reset)
        root.bind('<F1>', self.randomize)
        root.bind('<F2>', self.box)
        root.bind('<Return>', self.save)

        # Initialize app
        self.pack()
        self.update_timeText()


    # All widgets are deleted and re-made, used to keep formatting correct when displaying new info
    def reset(self, event):

        self.background_image = PhotoImage(file=self.this_image)
        self.background_label = Label(root, image=self.background_image)
        self.background_label.photo = self.background_image
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.timeText.destroy()
        self.highscore.destroy()

        # If reset is used before timer has started, AttributeError will occur
        try:
            self.nameEntry.destroy()
        except AttributeError:
            pass

        # If reset is used before a score is recorded, AttributeError will occur
        try:
            self.all_scores.forget()
        except AttributeError:
            pass

        # Remake all the widgets)
        self.timer = [0, 0, 0]
        self.pattern = '{1:02d}:{2:02d}'
        self.timeText = Label(root, text='00:00', font=('Evogria', 60), foreground='white', background='black')
        self.timeText.pack(side='top', expand=False)
        self.highscore = Label(root, textvariable=self.highscore_var, font=('Evogria', 20), foreground='yellow', background='black')
        self.highscore.pack(side='top', expand=False)


    # Constantly running when self.state is true (timer is running)
    def update_timeText(self):

        if self.state:

            # Every time this function is called, increment 1 centisecond (1/100 of a second)
            self.timer[2] += 1

            # Every 100 centisecond is equal to 1 second
            if self.timer[2] >= 100:
                self.timer[2] = 0
                self.timer[1] += 1

            # Every 60 seconds is equal to 1 min
            # Due to the short nature of the game, currently the timer resets once it hits 1 minute
            if self.timer[1] >= 60:
                self.timer[0] += 1
                self.timer[1] = 0

            # Grab time
            self.timeString = self.pattern.format(self.timer[0], self.timer[1], self.timer[2])

            # Display current time
            self.timeText.configure(text=self.timeString)

        # Updates every 1 centisecond
        root.after(10, self.update_timeText)

    # Both starts and stops the timer
    def start(self, event):

        # New instance, reset variables and widgets
        if not self.state:
            self.reset(event='null')

            # Begin
            self.state = True

        # End instance, display results
        else:
            self.state = False
            self.enter()

    # Save name and score
    def enter(self):
        try:
            self.nameEntry.destroy()
        except AttributeError:
            pass

        self.name = StringVar()
        self.name.set('')

        self.nameEntry = Entry(root, textvariable=self.name, background='black', foreground='white', font=('Evogria', 10), justify=CENTER)
        self.nameEntry.pack(side='top', expand=False, pady=10)
        self.nameEntry.focus()


    def save(self, event):
        try:
            self.nameEntry.winfo_exists() # Enter screen is up
        except AttributeError: # If name entry does NOT exist, then pressing enter should do nothing
            return

        # Gets name from previous function
        try:
            name = self.nameEntry.get()
            if len(name) == 0: # If name is empty, let the user try again
                self.enter()
                return
        except:
            return

        # Store name:score in dict
        try:
            self.scores[self.timeString].append(name.upper())

        # Climber hasn't been entered yet
        except KeyError:
            try:
                self.scores[self.timeString] = [name.upper()]

            # Happens if time is empty (possibly only replicable when testing code)
            except AttributeError:
                pass

        # Calculate score by total amount of seconds
        temp_score = int(self.timeString[0])*10 + int(self.timeString[1]) + int(self.timeString[3])/10 + int(self.timeString[4])/100

        # Lowest int becomes the new high score
        if temp_score < self.last_score:
            self.last_score = temp_score

            # Climber is shown during game in yellow
            self.highscore_var.set(name.upper() + '\n' + str(self.timeString))

        # Clear widgets for next run
        self.nameEntry.destroy()

        self.display()

    # Table of all scores
    def display(self):
        # Not using reset() because it remakes the widgets, we want a blank canvas
        self.timeText.destroy()
        self.highscore.destroy()
        self.nameEntry.destroy()

        self.background_image = PhotoImage(file='scores.gif') # Background for after the game
        self.background_label = Label(root, image=self.background_image)
        self.background_label.photo = self.background_image
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Essential barebone widgets
        self.all_scores = Label(root, text='Scores\n\n', background='black', foreground='white', font=('Evogria', 24))


        # Display all scores
        for score in sorted(self.scores.items()): # Sorts the dictionary lowest score to highest score
            name = str(score[1])
            self.all_scores['text'] +=  str(name[2:-2]) + ' ' + str(score[0]) + '\n\n'

        # Position of the start of scores
        self.all_scores.pack(side='top', pady=50, padx=30)

    # Cycles through images
    def next(self, event):

        index = self.image_list.index(self.this_image)
        if event.keysym == 'Right':
            try:
                self.this_image=self.image_list[index+1]

            # IndexError when the end of the list is reached, simply reset it to the first index
            except IndexError:
                self.this_image=self.image_list[0]
        if event.keysym == 'Left':
            try:
                self.this_image=self.image_list[index-1]
            except IndexError:
                self.this_image=self.image_list[-1]

        self.reset(event='null')

    # Necessary because of fullscreen
    def quit(self, event):
        root.destroy()

    # Creates random dots
    def randomize(self, event):
        t = Pen()
        t.speed(1) # Below .5 = normal speed - .6-1 is the slowest
        win = Screen()
        win.bgcolor('black')
        win.setup(width=1920, height=1080, startx=0, starty=0) # CANNOT make full screen, need a different module called pygsear
        #t.hideturtle() - Makes the cursor invisible (looks better), but will speed up the drawings too much

        t.color('white')
        for i in range(0, 1000):

            t.begin_fill()
            radius = random.randint(25, 40)
            t.circle(radius)
            t.end_fill()
            t.up()
            t._delay(20)
            # Waits 5 seconds on first circle for climber to get to it
            if i == 0:
                time.sleep(5)

            # Waits 1 second to slow the process
            else:
                time.sleep(1)

            t.down() # Remove if you don't want the lines to be traced - it helps the climbers predict where it's going

            t.goto(0, 0) # Go back to center to avoid going off screen
            distance = random.randint(200, 500)
            direction = random.randint(0, 360)

            # If turtle is facing left or right, it can go a further distance and still stay on screen

            # Left/Up or Left/Down
            if 130 < direction < 220:

                # Left
                if 150 < direction < 210:
                    distance = random.randint(200, 875)
                else:
                    distance = random.randint(200, 600)

            # Right/Up or Right/Down
            elif 300 < direction < 360 or 0 < direction < 50:

                # Right
                if 330 < direction < 360 or 0 < direction < 30:
                    distance = random.randint(200, 875)
                else:
                    distance = random.randint(200, 600)
            t.seth(direction)

            t.forward(distance)
            t.down()

    # Climber stays within box, simple timer, no scores
    def box(self, empty):
        pygame.init()

        # Change to max your display
        SCREEN_WIDTH = 1920
        SCREEN_HEIGHT = 1080

        # Full screen
        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.FULLSCREEN)

        # Change to max slower or faster
        FPS = 60

        # Box image
        wall_img = pygame.image.load('wall.png')
        wall_list = pygame.sprite.Group()

        BLACK = (0, 0, 0)
        wall = Squeeze(wall_img)

        # Change if you change resolution
        wall.rect.x = 600 # Left pixel of image
        wall.rect.y = 200 # Top pixel of image

        wall_list.add(wall)
        move = False
        done = False

        clock = pygame.time.Clock()
        screen.fill(BLACK)
        playtime = 0

        # Timer font+text
        font = pygame.font.SysFont('Evogria', 36)
        text = font.render('Time: {0:.2f}'.format(playtime), 1, (250, 250, 250))
        textpos = text.get_rect()
        textpos.centerx = screen.get_rect().centerx
        screen.blit(text, textpos)
        time = False

        # Checks for key presses, updates timer and display
        while not done:
            milliseconds = clock.tick(FPS)
            playtime += milliseconds / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    done = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not move:
                    move = True
                    time = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and move:
                    move = False
                    time = False
                    playtime = 0
            if time:
                screen.fill(BLACK)
                text = font.render('Time: {0:.2f}'.format(playtime), 1, (250, 250, 250))
                screen.blit(text, textpos)

            wall_list.draw(screen)
            wall_list.update(move)

            clock.tick(FPS)
            pygame.display.flip()

        pygame.quit()

# Main code for the box game
class Squeeze(pygame.sprite.Sprite):

    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.img_load(img)
        self.counter = 0
        self.choice = random.choice(['left', 'right'])
        self.choice2 = random.choice(['up', 'down'])
        self.too_right = False
        self.too_left = False
        self.too_high = False
        self.too_low = False

    # Moves and checks boundaries of the box
    def update(self, move):
        if move: # Only starts when space is pressed
            # Note: the image used will change all values here
            # Pixels are based off of the left edge (x) and the top edge (y)
            # In the future, there should be ratios implemented to work for all resolutions
            # walls.png is currently 734x700 pixels
            # scale it down, along with the right and bottom pixel values, to match other resolutions

            ###### CHECKS AND CORRECTS BOUNDARIES FOR X ######
            if self.rect.x >= 1200: # Right side hits right edge
                self.too_right = True
            elif self.rect.x <= 0: # Left side hits left edge
                self.too_left = True

            if self.too_right:
                self.rect.x += random.randint(-1, -1) # The amount of pixels the box will move per frame
                if self.rect.x <= 650: # 650 = x center
                    self.too_right = False
                    self.choice = random.choice(['left', 'right'])

            elif self.too_left:
                self.rect.x += random.randint(1, 1)
                if self.rect.x >= 650:
                    self.too_left = True
                    self.choice = random.choice(['left', 'right'])

            # Move a random direction after returning to center
            else:
                if self.choice == 'left':
                    self.rect.x += random.randint(-1, -1)

                elif self.choice == 'right':
                    self.rect.x += random.randint(1, 1)

            ###### CHECKS AND CORRECTS BOUNDARIES FOR Y ######
            if self.rect.y <= 50: # Box stops before text
                self.too_high = True
            elif self.rect.y >= 385: # Bottom side hits bottom of screen
                self.too_low = True

            if self.too_high:
                self.rect.y += random.randint(1, 1)
                if self.rect.y <= 200:
                    self.too_high = False
                    self.choice2 = random.choice(['up', 'down'])
            elif self.too_low:
                self.rect.y += random.randint(-1, -1)
                if self.rect.y >= 200:
                    self.too_low = False
                    self.choice2 = random.choice(['up', 'down'])

            else:
                if self.choice2 == 'up':
                    self.rect.y += random.randint(1, 1)
                else:
                    self.rect.y += random.randint(-1, -1)
            #################################################

    # Could be put in constructor
    def img_load(self, img):
        self.image = img
        self.rect = self.image.get_rect()



# Run class
root = Tk()
root.wm_title('Hit the Dots!')
app = Timer(master=root)
app.mainloop()


