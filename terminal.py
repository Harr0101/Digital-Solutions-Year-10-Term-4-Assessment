import pygame
import sys

class Terminal():
    def __init__(self,control):    
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


        self.hints = False
        self.listening = True

        self.killClock = 300
        self.loopsPerSecond = 30

    def run(self):
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
                elif event.key == pygame.K_1:
                    self.text += '1'
                elif event.key == pygame.K_2:
                    self.text += '2'
                elif event.key == pygame.K_3:
                    self.text += '3'
                elif event.key == pygame.K_4:
                    self.text += '4'
                elif event.key == pygame.K_5:
                    self.text += '5'   
                elif event.key == pygame.K_6:
                    self.text += '6'
                elif event.key == pygame.K_7:
                    self.text += '7'
                elif event.key == pygame.K_8:
                    self.text += '8'
                elif event.key == pygame.K_9:
                    self.text += '9'
                elif event.key == pygame.K_0:
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

    def draw(self):
        pygame.draw.rect(self.win,(0,0,0),(0,0,self.screenSize[0],self.screenSize[1]))
        for i in range(len(self.previousTexts)):
            textPic = self.font.render(self.previousTexts[i], 1, (150,255,150))
            self.win.blit(textPic,(0,20*i+10))
        if self.cursorOn:
            textPic = self.font.render(self.text+self.cursor, 1, (0,255,0))
        else:
            textPic = self.font.render(self.text, 1, (0,255,0))
        self.win.blit(textPic,(0,self.screenSize[1]-20))

        if self.hints or "?" in self.text:
            if self.hints:
                possibleCommands = []
                for command in self.control.commandsToActions.keys(): 
                    if command[:len(self.text)] == self.text:
                        possibleCommands.append(command)

                for command in self.control.player.inventory + self.control.currentRoom.items:
                    command = command.name
                    if command[:len(self.text)] == self.text:
                        possibleCommands.append(command)

            else:
                possibleCommands = []
                for command in self.control.commandsToActions.keys(): 
                    possibleCommands.append(command)

            for i in range(len(possibleCommands)):
                textPic = self.font.render(possibleCommands[i], 1, (255,255,255),(0,0,0))
                #pygame.draw.rect(self.win,(0,0,0),textPic.get_rect())
                self.win.blit(textPic,(0,self.screenSize[1]-40-20*i))

        pygame.display.flip()

    def descriptionAdd(self,description):
        if self.listening:
            descriptions = []
            while len(description)>self.maxLength:
                descriptions.append(description[:self.maxLength])
                description = description[self.maxLength:]

            self.previousTexts.extend(descriptions)
            self.previousTexts.append(description)

    def toggleCommands(self,command):
        self.hints = not(self.hints)

    def endGame(self,command):
        pygame.quit()
        sys.exit()
    
    def stopCommands(self):
        self.listening = False
