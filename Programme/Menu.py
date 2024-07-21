import pygame 
from pygame.locals import *
import sys

from Programme.Outils.Text import *
from Programme.Outils.compil import compil
from Programme.Outils.Animation import *

class Menu:
    def __init__(self,game):
        self.screen_width=game.screen.get_width()
        self.screen_height=game.screen.get_height()
        self.screen=game.screen
        self.game=game 

        self.text=TEXT(None,self.screen)
        self.mouvement=0
        self.vec=0

        self.position="main"
#__________rangement des ressources propres à chaques menu________
        
#-------Images des différents menus 
        self.contenu={'game':[],
                      'main':compil("Ressource\Menu\MainMenu"),
                      'pause':compil("Ressource\Menu\Pause"),
                      'Game_over':compil("Ressource\Menu\Game_over")}
#-------Boutton des différents menus   
        self.button_liste={'game':[],
                           'main':[],
                           'pause':[button((450, 300),(200, 50),(0, 0, 0),(100,50,50),self.change,'main','Main menu',30,[255,255,255]),
                                    button((750, 300),(200, 50),(0, 0, 0),(100,50,50),self.change,'game','Continue',30,[255,255,255])],
                            'Game_over':[button((600, 300),(200, 150),(0, 0, 0),(20,20,20),self.change,'main','The End',50,[255,255,255])]}
    
#-------Musique des différents menus    
        self.musique={'game':'Ressource\Musique\Jeu\Battle!!!.mp3',
                      'main':'Ressource\Musique\Menu\menu.mp3',
                      'pause':None,
                      'Game_over':None}
    def active(self):
        if self.position == "main":
            self.main_menu()
        elif self.position== "pause":
            self.pause()
        elif self.position == "Game_over":
            self.Game_over()
        
    def Change_Music(self):
        if self.musique[self.position]==None:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.load(self.musique[self.position])
            pygame.mixer.music.play(-1)

    def change(self,new_position):
        if self.position == 'Game_over' and new_position == 'main':
            self.game.set_reset()
            
        self.position=new_position
        self.Change_Music()

    
    def render(self,pos):
        for image in self.contenu[self.position]:
            self.screen.blit(image,pos[self.contenu[self.position].index(image)])
        for button in self.button_liste[self.position]:
            button.draw(self.screen)

    def main_menu(self):
#-------affichage du menu principale----------
        pos_img=[(-50,-10)]
        self.screen.fill((100,50,50))
        self.render(pos_img)
        self.text.text_screen(50," ~~~~Press (A) to start your aventure !~~~~",(0,0,0),(125,500+self.mouvement))
#-------événement du menu pricipale------------
        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_a:
                     self.change("game")
        
        if self.mouvement > 10:
            self.vec = 1
        elif self.mouvement < -10:
            self.vec = 0

        if self.vec==1:
            self.mouvement -= 0.2
        else:
            self.mouvement += 0.2

    def pause(self):
        pos_img=[(200,100)]

        self.render(pos_img)
        self.text.text_screen(100,"Pause",(255,255,255),(400,150))

        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type==MOUSEBUTTONDOWN:
                for button in self.button_liste[self.position]:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                            button.call_back(button.parametre)
        
    def Game_over(self):
        pos_img=[]

        self.screen.fill((0,0,0))
        self.render(pos_img)
        self.text.text_screen(100,"End of your quest...",(255,255,255),(200,50))

        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type==MOUSEBUTTONDOWN:
                for button in self.button_liste[self.position]:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                            button.call_back(button.parametre)


class button:
    def __init__(self, position, size, clr=[100, 100, 100], cngclr=None, func=None,parametre=None,text='', font_size=16, font_clr=[0, 0, 0]):
        self.clr    = clr
        self.size   = size
        self.func   = func
        self.parametre = parametre
        self.surf   = pygame.Surface(size)
        self.rect   = self.surf.get_rect(center=position)

        if cngclr:
            self.cngclr = cngclr
        else:
            self.cngclr = clr

        if len(clr) == 4:
            self.surf.set_alpha(clr[3])

        self.font=pygame.font.Font("Ressource/Text/alagard.ttf", font_size)
        self.txt = text
        self.font_clr = font_clr
        self.txt_surf = self.font.render(self.txt, 1, self.font_clr)
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])

    def draw(self, screen):
        self.mouseover()

        self.surf.fill(self.curclr)
        self.surf.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surf, self.rect)

    def mouseover(self):
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.curclr = self.cngclr

    def call_back(self, *args):
        if self.parametre==None:
            self.func()
        else:
            if self.func:
                return self.func(*args)



    


