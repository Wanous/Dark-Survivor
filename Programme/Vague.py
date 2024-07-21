import pygame
from random import randint,choice
from Programme.Monster import *

class Vague:
    def __init__(self,game):
#-------importation des objets dont la classe à besoin 
        self.joueur=game.joueur     #pour l'envoyer au monstre
        self.world=game.world       #pour le 'hors zone' (les ennemis ont besoin d'apparaître hors de la visibilté du joueur)
        self.Monstre=game.monstre  #pour ajouter des monstres on a besoin de la classe monstre

#-------Attribut de la classe        
        self.vague=0                #numéro de la vague
        self.intensite=1            #intensité maximum des monstre qui peuvent apparaître
        self.quantity=2             #quantité de monstre qui doit apparaître au cours d'une vague
        
        self.multiplicateur={'Attaque':1.05,'Vitesse':1.02}    #multiplication des stats des monstres entre chaques vagues
        self.next_spawn=0           #temps avant de faire spawn le prochain ennmemi
        self.horsZ=[i for i in range(10)]               #liste qui va contenir des points d'apparation des monstres
        self.time=0                 #temps depuis le dernier spawn d'un ennemi
        
        self.monstres=[]            #liste de monstre qui seront rajouter au cours du temps
        self.Monstre.add(0,self.world.taille//2-10,self.world.taille//2-10)
    
    def is_finish(self):
        '''renvoie True si tout d'abord tout les monstres sont morts 
           et si il reste plus de monstre à apparître sinonn renvoie False '''
        if len(self.Monstre.Groupe)==0 and len (self.monstres)==0:
            return True
        return False
    
    def next_wave(self):
        self.vague+=1
        self.quantity+=randint(1,3)
        for stat in self.Monstre.type:
            if self.vague%2==0: #toute les 2 vagues les monstres voit leurs points de vies multiplié
                stat['vie']*=self.multiplicateur['Attaque']
            if self.vague%5==0: #toute les 5 vagues les monstres voit leurs dégâts multiplié
                stat['speed']*=self.multiplicateur['Vitesse']
        self.vague_making()
            
    def spawning(self,temps):
        if temps - self.time > self.next_spawn and len(self.monstres)!=0:
            self.Monstre.add(self.monstres[0][0],self.monstres[0][1],self.monstres[0][2])
            self.monstres.pop(0)
            self.time=pygame.time.get_ticks()
            self.next_spawn=randint(3000,5000) 
            
    def hors_zone(self):
        '''méthode qui renvoie une liste de tuple qui sont des coordonnées
        ayant pour but de créeer des lieux d'apparation des monstres proche du joueur 
        mais hors de sa vue d'où l'utilisation de world.chunk'''
        #ici on créer 10 points d'apparation des monstres
        for i in range(10):
            x=self.joueur.x+choice([self.world.chunk//2,-self.world.chunk//2])
            y=self.joueur.y+choice([self.world.chunk//2,-self.world.chunk//2])
            self.horsZ[i]=(x,y)

              
    def vague_making(self):
        self.monstres=[]
        self.hors_zone()
        for m in range(self.quantity):
            x,y=choice(self.horsZ)
            self.monstres.append([randint(0,self.intensite),x,y])
 
    
        