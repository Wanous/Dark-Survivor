from json import load

import pygame, sys
from pygame.locals import *

#----------------Configuration avant l'importation des sous-programmes------------------

with open("config.json", encoding="utf-8") as f:
    CONFIG = load(f)
WIDTH=CONFIG["dimensions"]["width"]
HEIGHT=CONFIG["dimensions"]["height"]
FPS = CONFIG["fps"]
TITLE = CONFIG["title"]
#change la division par 4 pour + de zoom
X_CENTER, Y_CENTER = CENTER = (WIDTH // 4, HEIGHT // 4)
ORIGINE=[X_CENTER//2,Y_CENTER//2]

screen = pygame.display.set_mode((WIDTH, HEIGHT),0,32)
display = pygame.Surface(CENTER)

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
curseur=pygame.image.load('Ressource\JEU\Curseur\curseur.png')
icon=pygame.image.load('Ressource\JEU\Icon\icon.png')

pygame.display.set_icon(icon)
#-------------importation des sous-programmes---------------------
'''Lorsque l'on créé un programme massif il est intéressant de séparer 
les grandes parties afin de mieux s'y retrouver et avoir une meilleur 
organisation .L'inconvénient est que plus il y a de fichier plus il y aura 
d'importation '''
from Programme.Player import *
from Programme.Monster import *
from Programme.World import *
from Programme.GUI import *
from Programme.Menu import *
from Programme.Vague import *

#-------------importation des outils---------------------
from Programme.Outils.Isometrique import * 
from Programme.Outils.Text import *


'''Classe mère du jeu qui permet le fonctionnement de celui-ci c'est à dire 
le rafraîchissemnt de l'affichage ,du joueur, des monstres ...
De plus il gère le système de vague d'ennemi et le passage vers les menus
(menu principale, pause, option etc..)'''
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.mixer.music.load('Ressource\Musique\Menu\menu.mp3')
        pygame.mixer.music.play(-1)

        self.origine=[X_CENTER//2,Y_CENTER//2]
        self.time=0#pour le délai entre les coups et autres
#--------écran et surface---------------------------   
        self.screen = screen
        self.display = display
        self.set_reset()

#-------tout les composants du jeu (mis dans une méthode pour reset)-----------------
    def set_reset(self):
        self.Game_entities=pygame.sprite.Group()
        
        self.menu=Menu(self)
        self.world=World(self)

        self.joueur=Player(self)
        self.Game_entities.add(self.joueur)

        self.monstre=Monstre(self)
        #voir le fichier Isometrique pour comprendre l'intérêt de ceci :
        self.convert=Convert(self,64) 
    
        self.Vague=Vague(self)
        self.Vague.vague_making()
        self.gui = GUI(self,clock) 
    
    def main(self):
        while True:
            if self.menu.position != 'game':
                    self.menu.active()
                
            else:
                    if self.joueur.statut['PV']<=0:
                        self.menu.position='Game_over'                    
                    self.event()

                    self.display.fill((0,0,0))
                    
                    self.Game_entities.update(self)
                    self.monstre.Groupe.update(self)

                    self.world.optimise(self.joueur)
                    self.world.render(self.display,self.joueur,self.time,self.convert)

                    for sprite in sorted(self.Game_entities.sprites(),key = lambda sprite: sprite.rect.centery):
                        if (round(sprite.x,0),round(sprite.y,0)) in self.world.opti :
                            self.display.blit(sprite.image,(sprite.rect.x,sprite.rect.y))

                    for monstre in self.monstre.Groupe:
                        pygame.draw.rect(self.display,(0,0,0),(monstre.rect.x,monstre.rect.y-10,monstre.type['vie'],2))
                        pygame.draw.rect(self.display,(0,255,0),(monstre.rect.x,monstre.rect.y-10,monstre.vie,2))
                        
                    if not self.Vague.is_finish():
                        self.Vague.spawning(self.time)
                    else:
                        self.Vague.next_wave()          

                    if self.gui.Dev==True:
                        self.gui.DevMod()
                    
                    self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                    self.gui.update()
                    self.time=pygame.time.get_ticks()

            self.cursor()
            clock.tick(FPS)
            pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            self.joueur.events(event,self.time)#---> event du joueur dans la classe Player (car c'est plus lisible)

            if event.type == KEYDOWN:

                if event.key == K_f:
                    if self.gui.Dev==False:
                        self.gui.Dev=True
                    else:
                        self.gui.Dev=False

                elif event.key == K_m:
                    if self.gui.affiche_carte==False:
                        self.gui.affiche_carte=True
                    else:
                        self.gui.affiche_carte=False

                elif event.key == K_ESCAPE:
                     self.menu.position="pause"
                #pour faire apparître plein de monstre pour les tests
                elif event.key == K_a and self.gui.Dev==True:
                     co = (self.joueur.x+randint(-3,3),self.joueur.y+randint(-3,3)) #apparaît aléatoirement autour de 3 blocs du joueur
                     if self.world.Type[int(round(co[1],0))][int(round(co[0],0))]!=0: #pour pas qu'il apparaissent sur l'eau (certain peuvent être bloqués)
                        self.monstre.add(randint(0,2),co[0],co[1])
    def cursor(self):
        m_x,m_y=pygame.mouse.get_pos()
        self.screen.blit(curseur,(m_x,m_y))
    
game=Game()
game.main()
