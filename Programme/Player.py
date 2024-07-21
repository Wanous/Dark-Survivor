import pygame
from pygame.locals import *
from Programme.Weapon import *
from Programme.Outils.Animation import Animation
if '__name__'=='__main__':
	from Weapon import *
	from Outils.Animation import Animation

''' Attention cette classe produit le joueur certe mais est aussi responsable de la caméra
car le monde tourne autour du joueur  
(ici self.rect.x et self.rect.y c'est aussi traité dans la classe world avec world.offset)
offset c'est compenser en anglais ici world.offset compense le déplacement du joueur en bougeant le monde
pour que le joueur soit toujours au milieu (moins la où la souris pointe) avec les variables énoncé précédemment)'''


class Player(pygame.sprite.Sprite):
	def __init__(self,game):
		super().__init__()

		self.image = pygame.image.load('Ressource/Character/Idle/Idle-0.png').convert_alpha()
		self.rect = pygame.Rect(game.origine[0],game.origine[1],self.image.get_width(),self.image.get_height())#hitbox du joueur (au départ il est à l'origine)

		self.direction = pygame.math.Vector2() #vecteur qui déplace le joueur
		self.look = pygame.math.Vector2() #vecteur entre la souris est le joueur
		self.tile = None

		self.x=game.world.taille//2 #coordonnée y
		self.y=game.world.taille//2 #coordonnée x
		self.speed = 0.1 #vitesse de déplacement

		self.weapon=Weapon('Epée',self)
		self.is_attacking=False
		self.is_rolling=False #le joueur voit c'est dégat annuler si il est en esquive
		self.roulade={'time':0,'delay':900 ,'cout':15} #temps de la dernière roulade et délai

		self.stat={'PVMAX':200,'PMMAX':100,'EMAX':50} #point de vie/magie et endurance maximum autorisée  
		self.statut={'PV':200,'PM':100,'E':50} #point de vie/magie et endurance du joueur qui sera modifié au cours de la partie(dégats etc...)
		self.inventory={'potionVie':5,'potionMagie':5}
	
		#pour bouger tout dans le sens inverse
		self.origine=game.origine

		#prérequis de la classe animation 
		self.animation=animation
		self.current_sprite=0
		self.etape='Idle'

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_z]:	self.direction.y = -1
		elif keys[pygame.K_s]:	self.direction.y = 1
		else:	self.direction.y = 0
			
		if keys[pygame.K_d]:	self.direction.x = 1
		elif keys[pygame.K_q]:	self.direction.x = -1
		else:	self.direction.x = 0
			
		if abs(self.direction.x)+abs(self.direction.y) == 2 :
			self.direction.x=0
			self.direction.y=0
	
	def move(self,world):
		
		x,y=(self.x,self.y)
		#modification des coordonnées vecteur*vitesse
		self.x+=self.direction[0]*self.speed 
		self.y+=self.direction[1]*self.speed

		if self.verification(world) == False:
			self.x,self.y=x,y
			self.direction.x,self.direction.y=(0,0)
			pass

		self.rect.x=self.origine[0]-self.look.x//7-self.rect.width//2
		self.rect.y=self.origine[1]-self.look.y//7-self.rect.height//2

		self.tile=world.Tile[world.Type[int(round(self.y,0))][int(round(self.x,0))]]['nom']

	def verification(self,world):
		'''Fonction qui renvoie False si le déplacement du joueur est impossible'''
		if round(self.x,0) > world.taille-1 or round(self.y,0) > world.taille-1 or round(self.x,0) < 0 or round(self.y,0)< 0:
			return False
		elif world.Tile[world.Type[int(round(self.y,0))][int(round(self.x,0))]]['nom'] == 'Eau':
			return False
		return True
	
	def point (self):
		mx,my=pygame.mouse.get_pos()
		self.look.x = mx - self.origine[0] * 4
		self.look.y = my - self.origine[1] * 4
	
	def events(self,event,temps):
		if event.type==KEYDOWN:
			if event.key==K_SPACE and temps-self.roulade['time'] > self.roulade['delay']: #0.5s entre chaque roulade
				if self.statut['E']>self.roulade['cout'] and self.direction!=[0,0]:
					self.is_rolling=True #mis sur True 
					self.roulade['time']=pygame.time.get_ticks()
					self.statut['E']-=self.roulade['cout']

#-------Si on souhaite attaqué + que le délai est respecter
		if event.type == MOUSEBUTTONDOWN and temps-self.weapon.time > self.weapon.delay:
			if self.statut['E']>self.weapon.cout: #et qu'il a assez d'endurance (il a était mis ici car sinon c'est peu lisible)
				self.is_attacking = True
				self.weapon.time=pygame.time.get_ticks()
				self.statut['E']-=self.weapon.cout


	def update(self,game):
		if self.is_rolling == False: #il ne faut pas qu'il bouge pendant une roulade
			self.input() 		     #mouvement
		self.point() 				 #caméra avec la souris
		self.move(game.world) 		 #se déplace si les conditions lui permet de le faire
		self.update_statut(game.time,game.world)
		self.weapon.update() 		 #update son arme (son animation,etc...)

		self.animation_()
	
	def update_statut(self,time,world):
		key=pygame.key.get_pressed()
#-------avant tout déplacement on vérifie qu'il n'est pas dans une roulade
		if self.is_rolling==True:
			self.speed=0.11
			if time -self.roulade['time'] > self.roulade['delay'] :
				self.is_rolling=False
#-------cours si la touche e est appuyée + il a assez d'endurance + son vecteur n'est pas 0 (évite le gaspillage d'endurance)
		elif key[K_e] and self.statut['E']>0.3 and self.direction!=[0,0]: 
			if self.verification(world)==True:
				self.statut['E']-=0.3
				self.speed=0.15
#-------sinon on rempli sa barre d'endurance car il l'a consomme pas 
		elif self.statut['E']<self.stat['EMAX']: #marche ou ne fait rien
			self.statut['E']+=0.1
			self.speed=0.1

	def direction_(self):
		'''méthose qui retourne un str qui décrit là où l'utilisateur regarde 
		   avec la souris (aide pour l'orientation de l'attaque à l'épée)'''
		if self.look.x < 0:
			if self.look.y<0:
				return 'haut_gauche'
			else:
				return 'bas_gauche'
		elif self.look.x >= 0 :
			if self.look.y<=0:
				return 'haut_droit'
			else:
				return 'bas_droit'
	
	def animation_(self):
		changement=self.etape #variable pour savoir si il y a un changement d'animation 
#-------évaluation de l'état du joueur et en déduire ces animation
		if self.is_rolling==True: self.etape='Roulade'
		elif self.is_attacking == True:self.etape='Attaque_1'
		elif self.direction != [0,0]:self.etape='Marche'
		else :self.etape='Idle'
#-------Si il y a changement alors on met la nouvelle animation à son image de départ
		if self.etape != changement:
			self.current_sprite=0
		'''fonction qui gére le rafraichissement des animations,leurs vitesses et si les images sont a inversées horizontalement
		   car les animations du personnage à droite sont les même que à gauche mais il faut les inversées d'où le 
		   paramètre bool qui permet de oui ou non inversées les images de l'animation'''
		def flip(bool):
				if self.etape=='Roulade': Animation.update(self,0.2,bool)
				else:Animation.update(self,0.1,bool)
					
		if self.etape=='Attaque_1': #attaque est un cas à part car c'est la souris qui oriente l'image est non le vecteur du joueur
			if self.direction_() in ['haut_droit','bas_droit']: flip(False)
			else: flip(True)	
		else:  						#si il attaque pas et que le personnage va vers la gauche ou en bas ses animation sont inversées
			if self.direction == [-1,0] or self.direction == [0,1]:flip(True)
			else: flip(False)
				



#----------Animation du joueur-------------

animation={'Idle':Animation.compil('Ressource\Character\Idle'),
		   'Marche':Animation.compil('Ressource\Character\Run'),
		   'Roulade':Animation.compil('Ressource\Character\Roll'),
		   'Attaque_1':Animation.compil('Ressource\Character\AttackN1'),
		   'Mort':Animation.compil('Ressource\Character\Death')}



