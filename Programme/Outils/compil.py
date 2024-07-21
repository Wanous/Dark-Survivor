import pygame
import os

def compil(path):
        liste=[]
        for tile in os.listdir(path):
            liste.append(pygame.image.load(path+"/"+tile).convert_alpha())
        return liste    
 