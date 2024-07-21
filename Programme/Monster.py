import pygame 
from random import randint
from Programme.Outils.Animation import *
from Programme.Outils.Text import *

class Monstre(pygame.sprite.Sprite):
     def __init__(self,game):
          super().__init__()
#-------importation des objets dont la classe à besoin 
          self.cible=game.joueur
          self.world=game.world   
          self.entities=game.Game_entities   
#-------attribut de la classe
          self.Groupe=pygame.sprite.Group()
          self.Intensite=[]

          self.type=monstre #se refferer au bas du fichier car c'est illisible si c'est dans __init__
     
     def add(self,ID,x,y):
          self.Groupe.add(self.type[ID]['algo'](self.type[ID],x,y))#ajout dans la liste des monstres
          self.entities.add(self.type[ID]['algo'](self.type[ID],x,y))#ajout aux entités du jeu 
     
     def update(self,game):
          self.Groupe.update(game)


'''Premier algorithme de monstre'''
class Monstre_0(pygame.sprite.Sprite):
     def __init__(self,type,x,y):
          super().__init__()

          self.x=x
          self.y=y

          self.type=type
          self.vie=type['vie']
          self.Mort=False

          self.timeHit=0
          self.time=0
          self.next_attack=0
          self.prepa=False
          self.is_attacking=False

          self.etape='Marche'
          self.animation=self.type['animation']
          self.current_sprite=0

          self.image=self.type['animation']['Marche'][0]
          self.rect=pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())

     def deplacement(self,joueur,world,temps,entity):
          if Algorithme.collision_sword(self,joueur,temps):
               self.vie-= joueur.weapon.degat
               self.timeHit=pygame.time.get_ticks() 
          x,y=self.x,self.y
          if not Algorithme.collision_joueur(self,joueur):
               Algorithme.vecteur(self,joueur,self.type['speed']/100)
     
     def attaque(self,joueur,time):
          if self.is_attacking==True:
               if Algorithme.collision_joueur(self,joueur) and joueur.is_rolling !=True :
                    joueur.statut['PV']-=self.type['attaque']
               self.is_attacking=False

          if self.prepa != True:
               if  Algorithme.collision_joueur(self,joueur):
                    self.next_attack=randint(5000,10000)
                    self.prepa=True
          else:
               if time-self.time > self.next_attack:
                    self.is_attacking=True
                    self.time=pygame.time.get_ticks()
                    self.prepa=False
     
     def animation_(self,joueur):
          if self.vie<=0:
               self.etape='Mort'
          elif Algorithme.collision_joueur(self,joueur)==False:
               self.etape='Marche'
          elif self.is_attacking==True:
               self.etape='Attaque'
          else:
               if Animation.is_finish(self):
                    self.etape='Marche'


          Animation.update(self,0.2,False)



     def Etat(self):
          if self.vie <= 0:
               if Animation.is_finish(self):
                    self.Mort=True
                    self.kill()

     def update(self,game):
          if self.etape!='Mort':
               self.deplacement(game.joueur,game.world,game.time,game.Game_entities)
               self.attaque(game.joueur,game.time)
          
          self.animation_(game.joueur)
          self.Etat()
          
          self.rect.x,self.rect.y=game.convert.Iso(self.x,self.y,-game.joueur.rect.height/2)
          self.rect.x-=self.image.get_width()//2
          self.rect.y-=self.image.get_height()//2

#-----------------------Bibliothèque des monstres---------------------------

monstre=[{'nom':'Serpent',     #nom du monstre
          'vie':30,         #vie du monstre 
          'attaque':10,     #attaque du monstre
          'speed':3,        #vitesse de déplacement 
          'algo':Monstre_0, #algorythme de déplacement et d'attaque
          'niveau':1,       #dangerosité du monstre (aide à la conception des vague voir la classe Vague)
          'animation':{'Marche':Animation.compil('Ressource\monstre\Serpent\Walk'),#ses animation    
                       'Attaque':Animation.compil('Ressource\monstre\Serpent\Attack'),
                       'Mort':Animation.compil('Ressource\monstre\Serpent\Ded')}},
                       
                       
        {'nom':'Spiral',    
          'vie':20,       
          'attaque':5,    
          'speed':3,       
          'algo':Monstre_0, 
          'niveau':1,      
          'animation':{'Marche':Animation.compil('Ressource\monstre\Spiral\Walk'), 
                       'Attaque':Animation.compil('Ressource\monstre\Spiral\Attack'),
                       'Mort':Animation.compil('Ressource\monstre\Spiral\Ded')}},
                       
                       
        {'nom':'Faucheur',     
          'vie':35,        
          'attaque':15,     
          'speed':2,        
          'algo':Monstre_0, 
          'niveau':2,       
          'animation':{'Marche':Animation.compil('Ressource\monstre\Faucheur\Walk'),   
                       'Attaque':Animation.compil('Ressource\monstre\Faucheur\Attack'),
                       'Mort':Animation.compil('Ressource\monstre\Faucheur\Ded')}}
        
        ] 

#-----------------------Algorythme de déplacement + attaque--------------------------------
        
'''Classe qui effectue des tâches communes à beaucoup de monstres
    comme: ne pas traverser l'eau ou ne pas dépasser les frontières de la map
    De plus elle construit les vecteurs pour le déplacement des monstres
    En bref ceci simplifie la création et la compréhension des algorithme des monstres'''

class Algorithme:
     'Renvoie vrai si le monstre est sur de l eau'
     def hors_eau(M,world):
        if world.Type[round(M.y)][round(M.x)] == 0 :
             return True 
        return False
     'Renvoie vrai si le monstre à dépasser les frontière de la carte'
     def hors_map(M,world):
          if round(M.x,0) > world.taille-1 or round(M.y,0) > world.taille-1 or round(M.x,0) < 0 or round(M.y,0)< 0:
               return True
          return False
     'Renvoie vrai si la méthode hors_eau et hors_map renvoie vrai'
     def hors_all(M,world):
          if  not Algorithme.hors_eau(M,world) and not Algorithme.hors_map(M,world):
               return True
          return False
     'Renvoie vrai si il est en collision avec un des monstres les plus proches de lui '
     def collision_monstre(M,entity):
          for sprite in list(entity.sprites()):
               if M.rect.colliderect(sprite.rect) and sprite!=M:
                    return True
          return False
     
     'Renvoie vrai si le monstre touche le centre du joueur'
     def collision_joueur(M,joueur):
          if M.rect.collidepoint(joueur.rect.center):
               return True
          return False
     'Renvoie vrai si le monstre est touché par l épée du joueur si ce dernier attaque bien et qu il ne c est pas déjà pris des dégâts'
     def collision_sword(M,joueur,temps):
        if M.rect.colliderect(joueur.weapon.hitbox) and joueur.is_attacking==True:
            if temps-M.timeHit > joueur.weapon.delay: 
                 return True
        return False
     
     'renvoie le vecteur du monstre avec une vitesse mise en paramètre'
     def vecteur(M,joueur,speed):
        if M.x - joueur.x < 0:
                M.x+=speed
        elif M.x - joueur.x> 0:
                M.x-=speed
                
        if M.y - joueur.y < 0:
                M.y+=speed
        elif M.y - joueur.y > 0:
                M.y-=speed
                    