import pygame
from Programme.Outils.Text import *
from Programme.Outils.Animation import *
from Programme.Monster import *

def carte(world,map,cube):
        for x in range(world.taille):
            for y in range(world.taille):
                pygame.draw.rect(map,world.Tile[world.Type[y][x]]['color'],(x*cube,y*cube,cube,cube))
        return map

class GUI :
    def __init__(self,game,clock):
        
        self.world=game.world
        self.vague=game.Vague
        self.joueur=game.joueur
        self.Monstre=game.monstre

        self.color=[(100,50,50),(100,150,150),(100,150,120)] #couleur de statut du joueur --> [vie,magie,endurance]

        self.screen=game.screen
        self.display=game.display

        self.fps=clock
        self.texte=TEXT(self.display,self.screen)
        
        self.cube=5 #taille d'un carré sur la carte
        self.map=pygame.Surface((self.world.taille*self.cube,self.world.taille*self.cube)) #Carte qui sera afficher
        self.map=carte(self.world,self.map,self.cube) #dessin de la carte 
        self.map_location=(self.screen.get_width()-self.map.get_width(),0)

        self.images={'HB':Animation.compil('Ressource\GUI\HealthBar'), #image de la bar de vie,magie et endurance
                     'MB':None,
                     'EB':None}
        
        self.Dev=False #pour aider au développement du jeu
        self.affiche_carte=False
        
    def DevMod(self,screen=None):
        #pour afficher le Mode développeur sur "screen" (doit se faire après le blit dans main)
        if screen:
            self.texte.text_screen(50,f'Co:({round(self.joueur.x,0)-self.world.taille//2},{round(self.joueur.y,0)-self.world.taille//2})',(255,255,255),(0,0),(0,0,0))
            self.texte.text_screen(50,f'{self.joueur.look}',(255,255,255),(0,50),(0,0,0))
            self.texte.text_screen(50,f'Tile:-{self.joueur.tile}-',(255,255,255),(0,100),(0,0,0))
            self.texte.text_screen(50,f'FPS:{int(self.fps.get_fps())}',(255,255,255),(0,150),(0,0,0))
            self.texte.text_screen(50,f'roulade:{self.joueur.is_rolling}',(255,255,255),(0,200),(0,0,0))
            self.texte.text_screen(50,f'attack:{self.joueur.is_attacking}',(255,255,255),(0,250),(0,0,0))

            self.texte.text_screen(50,f'PV: {self.joueur.statut["PV"]}',(255,255,255),(0,300),(255,0,0))
            self.texte.text_screen(50,f'PM:{self.joueur.statut["PM"]}',(255,255,255),(0,350),(0,0,255))
            self.texte.text_screen(50,f'E:{int(self.joueur.statut["E"])}',(255,255,255),(0,400),(0,255,0))
            
        #pour afficher le Mode développeur sur "display" (doit se faire après tout les autres affichages du display)
        pygame.draw.circle(self.display,(0,255,0),self.world.origine,5)
        pygame.draw.circle(self.display,(255,0,0),self.joueur.rect.center,2)
        pygame.draw.rect(self.display,(200,0,0),self.joueur.rect,2)
        if self.joueur.is_attacking:
            pygame.draw.rect(self.display,(255,255,255),self.joueur.weapon.hitbox,1)
        #ce qui permet de voir le centre du décalage (qui doit être le joueur au niveau de ses jambes)
        #cela permet d'aider pour le calcul
        pygame.draw.circle(self.display,(0,0,255),(self.world.offset[0],self.world.offset[1]),5)
        for monstre in self.Monstre.Groupe:
            pygame.draw.rect(self.display,(255,0,0),monstre.rect,1)
        
    def carte(self):
        self.screen.blit(self.map,(self.map_location[0],self.map_location[1]))
        pygame.draw.rect(self.screen,(255,255,255),(self.joueur.x*self.cube+self.map_location[0],self.joueur.y*self.cube+self.map_location[1],self.cube,self.cube))

    def UI(self):

        value=list(self.joueur.stat.values())
        value2=list(self.joueur.statut.values())
        for H in range(3) :
            pygame.draw.rect(self.screen,(0,0,0),(100,H*30,value[H],25))
            pygame.draw.rect(self.screen,self.color[H],(100,H*30,value2[H],25))
            self.screen.blit(self.images['HB'][0],(100-self.images['HB'][0].get_width()//2,H*30))
            self.screen.blit(self.images['HB'][1],(100+value2[H]-self.images['HB'][0].get_width()//2,H*30))
        
        pygame.draw.circle(self.screen,(0,0,0),(50,50),40)
        pygame.draw.circle(self.screen,(212,185,150),(50,50),40,5)
        self.texte.text_screen(80,f'{self.vague.vague}',(255,255,255),(35,20))


    def update(self):
        self.UI()
        if self.Dev == True:
            self.DevMod(True)
        if self.affiche_carte == True:
            self.carte()


