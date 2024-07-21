import pygame

from random import randint,gauss
from perlin_noise import PerlinNoise
from Programme.Outils.Isometrique import *
from Programme.Outils.compil import compil


class World :
    def __init__(self,game):

        self.Tile=[
                   {'nom':'Eau',
                    'image':compil("Ressource/Tile/Eau"),
                    'color':(93,160,212)},
                    {'nom':'Bord',
                    'image':compil("Ressource/Tile/Bord"),
                    'color':(187,195,137)},
                    {'nom':'Plaine',
                    'image':compil("Ressource/Tile/Plaine"),
                    'color':(123,223,126)},
                    {'nom':'PlaineSupérieur',
                    'image':compil("Ressource/Tile/PlaineSup"),
                    'color':(102,185,104)},
                    {'nom':'Bois',
                    'image':compil("Ressource/Tile/Bois"),
                    'color':(66,129,50)},
                    {'nom':'BoisSupérieur',
                    'image':compil("Ressource/Tile/BoisSup"),
                    'color':(37,75,27)},
                    ]
        
        self.taille=50
        self.chunk=10 #15 est idéal
        self.seed=randint(0, 100000)
        self.Type,self.Image,self.Hauteur=Perlin(self.taille,self.seed,self.Tile)
        self.opti=[]

        self.offset=[0,0]
        self.origine=game.origine

    def optimise(self,Player):
        self.opti=[]
        for x in range (self.chunk):
            for y in range(self.chunk):
                self.opti.append((int(Player.x+self.chunk//2-x),int(Player.y+self.chunk//2-y)))    
        self.opti=sorted(self.opti)  

    def render (self,display,Player,time,convert):

        self.offset[0]=Player.rect.x+Player.rect.width/2
        self.offset[1]=Player.rect.y+Player.rect.height

        for pos in self.opti:
            x,y=pos
            if 0<=x<self.taille and 0<=y<self.taille:
                Type=self.Type[y][x]# on consulte son type dans la liste ex :terre
                image=self.Image[y][x]# puis son image ex : terre fleuri
                hauteur=self.Hauteur[y][x]
                if Type == 0 and time%200<30:
                    new_height=gauss(0,1)
                    display.blit(self.Tile[Type]['image'][image],convert.Iso(x-1,y,new_height))  
                    self.Hauteur[y][x]=new_height
                else:
                    display.blit(self.Tile[Type]['image'][image],convert.Iso(x-1,y,hauteur))    
    def reset(self):
        self.seed=randint(0, 100000)
        self.Type,self.Image,self.Hauteur=Perlin(self.taille,self.seed,self.Tile)        

'''fonction qui renvoie une matrice du bruit de Perlin 
    qui sera utiliser pour optimiser le jeu 
    càd que pour savoir quel case est quoi il 
    suffit juste de regardé sa coordonnée dans cette matrice 
    exemple (0,0) --> liste[0][0] = 1 = EAU'''

def Perlin(taille,Seed,Tile):
    noise = PerlinNoise(octaves=6, seed=Seed)
    xpix, ypix = taille, taille
    pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

    Type= [[0]*taille for i in range(taille)] # matrice du type de case ex: Terre
    Image= [[0]*taille for i in range(taille)]# matrice de l'image de la case ex: Terre_1 (case Terre mais avec des fleurs)
    Hauteur=[[0]*taille for i in range(taille)]

    for x, row in enumerate(pic):
        for y, column in enumerate(row):
     
            if column>=0.09:    Type[y][x]=5     #boisSupérieur
            elif column >=0.009:Type[y][x]=4     #bois
            elif column >=-0.06:Type[y][x]=3     #plaineSupérieur
            elif column >=-0.3: Type[y][x]=2     #plaine
            elif column >=-0.31:Type[y][x]=1     #bord
            elif column >=-0.8: Type[y][x]=0     #eau        
                
            if Type[y][x]==0:
                Hauteur[y][x]=column*20+5
            else:
                Hauteur[y][x]=column*20-gauss(0,1)

            #5/8 que ce soit l'image de base et non une version modifiée
            #cela évite qu'il y ait trop de fleur ou autre
            case = randint(1,8)
            if case > 6 and len(Tile[Type[y][x]]['image'])-1 >0:
                img = randint(1,len(Tile[Type[y][x]]['image'])-1)
            else:
                img=0
            
            Image[y][x]=img
             
    return Type,Image,Hauteur





        




    
                    

                
