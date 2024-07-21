import pygame
import os

'''
prérequis de la classe Animation pour toute objet qui souhaite l'utiliser :
        
        self.image --> objet de pygame.image.load pour contenir la frame à afficher 
        self.current_sprite --> int  = numéro de l'image de l'animation qui est afficher 
        self.etape --> str  = nom d'une animation dans un dictionnaire

        self.animation --> dictionnaire = dictionnaire qui contient toutes les animations
        exemple :
        
        animation = {'Marche:Animation.compil("Ressource\joueur\Marche"),
                             'Attaque:Animation.compil("Ressource\joueur\Attaque")}

        Pour information Animation.compil est une méthode qui prend en paramètre un chemin 
        vers un fichier rempli d'image et qui renvoie une liste contenant les images de ce fichier 
        prêt pour l'affichage dans pygame grâce à pygame.image.load.
'''
class Animation:
    def update(objet,speed,flip=False,boucle=1):#méthode qui permet l'animation d'un sprite 

        objet.current_sprite += speed
        if int(objet.current_sprite) >= len(objet.animation[objet.etape]):
            if boucle == 0: #si c'est 0 l'animation ne boucle pas et est joué une seule fois
                objet.current_sprite=len(objet.animation[objet.etape])-1
            else:
                objet.current_sprite = 0
        
        img=objet.animation[objet.etape][int(objet.current_sprite)].copy()
        if flip != False :
            objet.image = pygame.transform.flip(img, True, False)
        else:
            objet.image=img
    
    def is_finish(objet):
        if int(objet.current_sprite) == len(objet.animation[objet.etape])-1:
            return True
        return False
    
    def compil(path):
        liste=[]
        for tile in os.listdir(path):
            liste.append(pygame.image.load(path+"/"+tile).convert_alpha())
        return liste    
    
