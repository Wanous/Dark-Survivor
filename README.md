# Dark Survivor
# ![Logo.png](photos/Logo.png)

<div align=center>
  <img alt="Taille du code GitHub" src="https://img.shields.io/github/languages/code-size/Wanous/Dark-Survivor?label=taille%20du%20code">
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Wanous/Dark-Survivor?logo=github&style=plastic">
  <img alt="License" src="https://img.shields.io/github/license/Wanous/Dark-Survivor?style=plastic">
</div>

Dark Survivor is a game where your fighting differents waves of various ennemies (3 to be honest). The more your progress, more the ennemies will be **stronger** and **faster**.
 Your objectif is to survive the most waves you can. Every game you playing is different because the map is generated with the Perlin noise and the waves of ennemies are completely random.

## How to play it 

- Download the latest version of Python with [this link](https://www.python.org/downloads/)
- Download this depot using the download button
- Open a terminal in the folder where you have download the depot
- Execute the command `python -m pip install -r requirements.txt` to install the dependencies
- Execute the command  `python main.py` to lunch the programm

## Interface
Le logiciel débutera par une fenêtre dans laquelle vous pourrez choisir un type de graphe à crée 
ou vous pouvez directement en importer un .

Suite à cela vous serez accueilli par l'interface principale dans laquelle vous pourrez laisser
libre cours à votre créativité pour votre graphe .Vous y retrouverez un tableur dans lequel il sera afficher les informations
des noeuds de votre graphe puis un canevas qui illustrera votre graphe et permetra d'intéragir avec celui-ci.
Aussi l'interface de l'application a été produit avec la bibliothèque Tkinter et est complétement redimensionnable à votre souhait .

Voici une photo pour illuster l'interface en mettant en valeur les possibilités offertes :

<div align=center><img alt="Image de l'interface" height="50%" width="50%" src="photos/Interface.png"></div>
(Dans cette exemple un fichier `.graf` à été importé)



## Interragir avec votre graphe 
Il est possible d'ajouter,de supprimer ou même de modifier un noeud de 
votre graphe à partir de quelques cliques :

- `Clic droit sur un noeud` : Modifier ou supprimer un noeud
- `Clic droit hors d'un noeud` : Ajouter un noeud
- `Clic gauche sur un noeud` : Permet de sélectionner un noeud pour le déplacer

Voici à quoi ressemble ces menus :

<div align=center>
  <img alt="Image du menu d'édition d'un noeud" height="25%" width="25%" src="photos/EditionNoeud.png">
  <img alt="Image du menu de création d'un noeud" height="25%" width="25%" src="photos/CreationNoeud.png">
</div>

## Controls

Here are the buttons to play the game  :

| Button | Action |
| ------ | ------ |
| Z↗S↘Q→D←| Move the character.|
| SPACE | Role (make you invincible a short moment).  |
| Left click |  Attack (The direction of the attack is based on the position of the mouse).  |
| M | Show the map. |
|ESCAPE| Put the pause menu where you can quit.|
| F | Enable Developer Mod to see more details. |
| A (during Devmod)| Spawn monster.|

  
### Raccourci
Quelques raccourcies sont aussi disponible :
#### Raccourcis pour des sous-menus de la barre de menu
- `ctrl + s` : sauvegarder un graphe
- `ctrl + o` : importer un graphe
- `ctrl + n` : commencer un nouveau graphe

- #### Raccourcis pour la console
- `flèche du haut` : ancienne commande (comme dans une invite de commande)
- `flèche du bas` : supprime la commande
- `entrée` : envoie la commande

## Extension .graf 
Graphe Studio posséde sa propre extension de fichier nommée `.graf` .Cela permet de relier ce type de fichier à l'application
  




