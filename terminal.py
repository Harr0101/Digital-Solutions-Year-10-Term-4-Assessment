#DOCSTRINGS DONE
import pygame
import sys

class Terminal():
    """
    A class to represent and control the terminal that outputs text and receives instructions

    ...

    Attributes
    ----------
    control : Control
        the control object currently used in the game
    screenSize : set
        size of terminal (x,y)
    win : Surface
        the representation of the screen that is drawn
    clock : Clock
        a timer used to make the number of ticks per second consistent
    font : Font
        the object used to render text into an image
    text : str
        what is currently being into the terminal by the player
    cursor : str
        what the cursor is viewed as on the screen
    cursorOn : bool
        whether the cursor is currently showing or not
    cursorTimerMax : int
        How many ticks the cursor is displayed for
    cursorTimer : int
        current number of ticks passed since cursor changed
    previousTexts : list
        current strings listed in the terminal in reverse order
    maxLength : int
        the maximum length of each line before characters are tuncated and moved to the following line
    commands : bool
        if possible commands are currently being shown in a HUD on the terminal
    listening : bool
        if the terminal is currently listening for player commands
    killClock : int
        number of ticks till the program is killed when the game stops
    loopsPerSecond : int
        number of ticks per second


    Methods
    -------
    run():
        adds to text, checks terminal, and draws
    keys(events):
        checks if any keys have been pressed and adds them to the command
    draw():
        draws all text on terminal 
    descriptionAdd(description):
        adds description to previous texts on terminal
    toggleCommands(command):
        turn hints on or off
    endGame(command):
        kills terminal and program
    stopCommands():
        sets commands to False to stop the player from typing.
    """
    def __init__(self,control):   
        '''
        Constructs necessary attributes for the control object

        Parameters: 
            control(Control) : link to current control object
        '''
        pygame.init()
        self.control = control

        #Sets up screen
        self.screenSize = (800,500)
        self.win = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption("Terminal")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("TimesNewRoman",18)
        self.text = ""
        self.cursor = "|"
        self.cursorOn = True
        self.cursorTimerMax = 10
        self.cursorTimer = self.cursorTimerMax
        self.previousTexts = []
        for i in range(23):
            self.previousTexts.append("")
        self.maxLength = 100


        self.commands = False
        self.listening = True

        self.killClock = 300
        self.loopsPerSecond = 30

    def run(self):
        '''
        Updates the terminal

        Parameters:
            None

        Returns
            None
        '''
        self.clock.tick(self.loopsPerSecond)
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        self.keys(events)

        self.cursorTimer-=1
        if self.cursorTimer<0:
            self.cursorTimer = self.cursorTimerMax
            self.cursorOn = not(self.cursorOn)

        if len(self.previousTexts)>23:
            self.previousTexts.pop(0)
        
        if not(self.listening):
            self.killClock -= 1
            if self.killClock == 0:
                self.endGame("")

        self.draw()

    def keys(self, events):
        '''
        Checks if any keys have been pressed in the last loop 
        Adds characters to current text
        Sends command to control object

        Parameters:
            events(list) : events that have happened in the last loop

        Returns
            None
        '''
        for event in events:
            if event.type == pygame.QUIT:
                self.endGame("")
            if event.type == pygame.KEYDOWN and self.listening:
                if event.key == pygame.K_a:
                    self.text += "a"
                elif event.key == pygame.K_b:
                    self.text += 'b'
                elif event.key == pygame.K_c:
                    self.text += 'c'
                elif event.key == pygame.K_d:
                    self.text += 'd'
                elif event.key == pygame.K_e:
                    self.text += 'e'
                elif event.key == pygame.K_f:
                    self.text += 'f'
                elif event.key == pygame.K_g:
                    self.text += 'g'
                elif event.key == pygame.K_h:
                    self.text += 'h'
                elif event.key == pygame.K_i:
                    self.text += 'i'
                elif event.key == pygame.K_j:
                    self.text += 'j'
                elif event.key == pygame.K_k:
                    self.text += 'k'
                elif event.key == pygame.K_l:
                    self.text += 'l'
                elif event.key == pygame.K_m:
                    self.text += 'm'
                elif event.key == pygame.K_n:
                    self.text += 'n'
                elif event.key == pygame.K_o:
                    self.text += 'o'
                elif event.key == pygame.K_p:
                    self.text += 'p'
                elif event.key == pygame.K_q:
                    self.text += 'q'
                elif event.key == pygame.K_r:
                    self.text += 'r'
                elif event.key == pygame.K_s:
                    self.text += 's'
                elif event.key == pygame.K_t:
                    self.text += 't'
                elif event.key == pygame.K_u:
                    self.text += 'u'
                elif event.key == pygame.K_v:
                    self.text += 'v'
                elif event.key == pygame.K_w:
                    self.text += 'w'
                elif event.key == pygame.K_x:
                    self.text += 'x'
                elif event.key == pygame.K_y:
                    self.text += 'y'
                elif event.key == pygame.K_z:
                    self.text += 'z'
                elif event.key in (pygame.K_1, pygame.K_KP_1):
                    self.text += '1'
                elif event.key in (pygame.K_2, pygame.K_KP_2):
                    self.text += '2'
                elif event.key in (pygame.K_3, pygame.K_KP_3):
                    self.text += '3'
                elif event.key in (pygame.K_4, pygame.K_KP_4):
                    self.text += '4'
                elif event.key in (pygame.K_5, pygame.K_KP_5):
                    self.text += '5'   
                elif event.key in (pygame.K_6, pygame.K_KP_6):
                    self.text += '6'
                elif event.key in (pygame.K_7, pygame.K_KP_7):
                    self.text += '7'
                elif event.key in (pygame.K_8, pygame.K_KP_8):
                    self.text += '8'
                elif event.key in (pygame.K_9, pygame.K_KP_9):
                    self.text += '9'
                elif event.key in (pygame.K_0, pygame.K_KP_0):
                    self.text += '0'   
                elif event.key == pygame.K_SLASH:
                    self.text += '?'
                elif event.key == pygame.K_SPACE:
                    self.text += ' '
                elif event.key == pygame.K_BACKSPACE:
                    self.text=self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.previousTexts.append(self.text)
                    self.control.command(self.text)
                    self.text = ""
                elif event.key == pygame.K_TAB:
                    self.text = self.possibleCommands[0]

    def draw(self):
        ''' Updates terminal window '''
        # Background
        pygame.draw.rect(self.win,(0,0,0),(0,0,self.screenSize[0],self.screenSize[1]))
        
        # Previous texts
        for i in range(len(self.previousTexts)):
            textPic = self.font.render(self.previousTexts[i], 1, (150,255,150))
            self.win.blit(textPic,(0,20*i+10))
        
        # Current command
        if self.cursorOn:
            textPic = self.font.render(self.text+self.cursor, 1, (0,255,0))
        else:
            textPic = self.font.render(self.text, 1, (0,255,0))
        self.win.blit(textPic,(0,self.screenSize[1]-20))

        # Possible commands
        if self.commands or "?" in self.text:
            if self.commands:
                self.possibleCommands = []
                for command in self.control.commandsToActions.keys(): 
                    if command[:len(self.text)] == self.text.lower():
                        self.possibleCommands.append(command)

                for command in self.control.player.inventory + self.control.currentRoom.items:
                    command = command.name
                    if command[:len(self.text)].lower() == self.text:
                        self.possibleCommands.append(command)

            else:
                self.possibleCommands = []
                for command in self.control.commandsToActions.keys(): 
                    self.possibleCommands.append(command)
                for command in self.control.player.inventory + self.control.currentRoom.items:
                    command = command.name
                    self.possibleCommands.append(command)

            for i in range(len(self.possibleCommands)):
                textPic = self.font.render(self.possibleCommands[i], 1, (255,255,255),(0,0,0))
                self.win.blit(textPic,(0,self.screenSize[1]-40-20*i))

        pygame.display.flip()

    def descriptionAdd(self,description):
        '''
        Adds text to previously texts to be displayed on the terminal

        Parameters:
            description (str) : string to be added to the terminal

        Returns
            None
        '''
        if self.listening:
            descriptions = []
            while len(description)>self.maxLength:
                descriptions.append(description[:self.maxLength])
                description = description[self.maxLength:]

            self.previousTexts.extend(descriptions)
            self.previousTexts.append(description)

    def toggleCommands(self,command):
        ''' Toggle showing commands '''
        self.commands = not(self.commands)

    def endGame(self,command):
        ''' Ends game and terminal '''
        pygame.quit()
        sys.exit()
    
    def stopCommands(self):
        ''' Stop player from inputting commands '''
        self.listening = False
