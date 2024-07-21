import pygame 
pygame.font.init()

'''

   Classe ayant pour but d'afficher du texte sur l'écran de manière plus explicite
   que la méthode traditionelle. 
   elle posséde 2 méthode :

        -text_screen qui prend en paramétre la couleur,taille,position ainsi que le texte 
         et l'affiche sur 'screen' 

        -text_display qui prend en paramétre la couleur,taille,position ainsi que le texte 
         et l'affiche sur 'display' 
         
'''

class TEXT :
    def __init__(self,display,screen):
        self.font=pygame.font.Font("Ressource/Text/alagard.ttf", 50)
        self.display=display
        self.screen=screen
        
    def text_screen(self,taille,texte,couleur,pos,background=None):
        self.font=pygame.font.Font("Ressource/Text/alagard.ttf", taille)
        texte=self.font.render(texte,True,couleur,background)
        self.screen.blit(texte,pos)
    
    def text_display(self,taille,texte,couleur,pos,background=None):
        self.font=pygame.font.Font("Ressource/Text/alagard.ttf", taille)
        texte=self.font.render(texte,True,couleur,background)
        self.display.blit(texte,pos)

        




        