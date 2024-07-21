from numba import njit

'''
    Classe qui permet de transformer des coordonnées d'un repère orthonomée 
    en coordonnées d'un repère isometrique tout en appliquant les calcules
    requis pour donner l'effet du personnage qui bouge (c'est à dire retire 
    les coordonnées du joueur et le décalage)

    Tout cela est produit dans la méthode Iso qui prépare les variables
    a envoyé à la fonction Iso qui va faire la convertion de manière trés 
    rapide graçe à la fonction njit de la bibliothèque numba qui amèliore la rapidité 
    des calculs et ainsi ne pas perdre de performance.

    P.S : Si je prépare les variables au lieu de faire la convertion immédiatement c'est car 
    njit accepte pas des variables provenant de classe.

'''
class Convert:
    def __init__(self,game,Tile_square):
        self.Tile_square=Tile_square
        self.joueur=game.joueur
        self.world=game.world

    def Iso(self,x,y,hauteur=0):
        x-=self.joueur.x
        y-=self.joueur.y
        offsetX,offsetY=self.world.offset
        return Iso(x,y,offsetX,offsetY+hauteur)

Tile_square=64 #ici c'est ce à quoi correspond une case soit 64 pixels par 64 pixels
@njit(fastmath=True)
def Iso(x,y,offsetX,offsetY):
    return [x * Tile_square/2 - y * Tile_square/2 + offsetX,x * Tile_square/4 + y * Tile_square/4 + offsetY]

@njit(fastmath=True)
def Iso_x(x,y):
    return x * Tile_square/2 - y * Tile_square/2 

@njit(fastmath=True)
def Iso_y(x,y):
    return x * Tile_square/4 + y * Tile_square/4