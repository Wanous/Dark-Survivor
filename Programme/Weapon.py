import pygame 

Arme={'Epée':{'nom':'Epée',     #nom 
          'type':'Epée',
          'attaque':10,  #dégat 
          'delay':1000,  #temps avant de frapper (ici 2s)
          'cout':10,     #coût en endurance
          'image':pygame.image.load('Ressource\Weapons\Sword.png'),
          'hitbox':(70,50)}}

class Weapon:
    def __init__(self,ID,Joueur):
        self.type=Arme[ID]
        self.joueur=Joueur
        self.time=0
        self.frame=0
        
        self.degat=self.type['attaque']
        self.delay=self.type['delay']
        self.cout=self.type['cout']
        self.image=self.type['image']
        
        self.hitbox_value=self.type['hitbox']
        self.hitbox=pygame.Rect(self.joueur.rect.center[0],self.joueur.rect.center[1]-self.hitbox_value[1]/2,self.hitbox_value[0],self.hitbox_value[1])

    def animation(self):
        self.frame+=0.1
        if int(self.frame)>2:
            self.frame=0
            self.joueur.is_attacking=False
    
    def update(self):
        if self.joueur.direction_() in ['haut_droit','bas_droit']:
            self.hitbox.x,self.hitbox.y = self.joueur.rect.center[0],self.joueur.rect.center[1]-self.hitbox_value[1]/2
        else:
            self.hitbox.x,self.hitbox.y = self.joueur.rect.center[0]-self.hitbox_value[1],self.joueur.rect.center[1]-self.hitbox_value[1]/2
        if self.joueur.is_attacking==True :
            self.animation()
    
    

    