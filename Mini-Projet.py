from tkinter import *                                               #J'importe Tkinter qui me permet d'ouvrir la fenetre d'affichage
#import pygame                                                      ; j'ai essauyé d'utilisé cette librairie pour le son mais elle n'est pas reconnue


# etatcase : 0 = case libre ; 1 = pion bleu ; 1.5 = croix bleu ; 2 = pion rouge ; 2.5 = croix rouge


class pion:                                                         #Je crée ma classe pion qui me permet de gerer le mode de fonctionnement de mes pions
                                                                    #Je ne l'ai pas trouvé l'utilité de cette classe donc elle n'est pas très remplie
    def __init__(self, joueur,etatcase):
        self.joueur= joueur
        self.etatcase= etatcase


class jeu:                                                          #Je créer ma classe jeu pour gérer l'affichage de mon jeu , j'ai commencer a coder pas a pas et sans m'en rendre compte tous mon code était ici
    def __init__(self, dimension=8,conditionvictoire=4,joueur=1,dernierecasej1=0 ,dernierecasej2=0,dernierecroixj1=0 ,dernierecroixj2=0):
        self.__dimension= dimension                                 #J'implémente mes différentes variables
        self.conditionvictoire= conditionvictoire
        self.joueur= joueur
        self.__dernierecasej1= dernierecasej1
        self.__dernierecasej2= dernierecasej2
        self.__dernierecroixj1 = dernierecroixj1
        self.__dernierecroixj2 = dernierecroixj2

        self.create_board()                                         #Tout d'abord je créer mon tableau
        #pygame.init()

        self.__root= Tk()                                           #Je créer aussi la fenêtre qui servira a afficher mon jeu
        self.__root.title('Mini-Projet 1ALGO')                      #Je l'a nomme

        self.__frame_principal= Frame(self.__root,bg="black")       #Je créer ma première frame où mon tableau sera déposé
        self.__frame_principal.grid(row=0,column=0,rowspan=1)       #Et je place ma frame sur ma fenêtre

        self.__frame1= Frame(self.__frame_principal)                #Ma deuxième frame où j'affichérais mes joueurs
        self.__frame1.grid(row=1,column=0,rowspan=1)                # Placement
        self.__frame1.pack()                                        #Mise en commun

        self.__canvas= Canvas(self.__frame1)                        # Paramètres de ma fenètre
        self.__canvas.config(highlightthickness=0,bd=0,bg="black")
        self.__canvas.pack()

        self.taillecellule= 550 // self.__dimension                 #Je paramètre aussi la future taille de mes cellules en fonction de la dimension plateau donné par le joueur
        board_width= self.__dimension * self.taillecellule          #Je paramètre aussi la taille de mon plateau par rapport aux cellules
        board_height= self.__dimension * self.taillecellule
        canvas_width= board_width + 180                             #Et la taille de ma fenetre est elle meme définit par rapport a la dimension du plateau
        canvas_height= board_height + 180

        self.drawGame(board_width,board_height,canvas_width,canvas_height)     #Je dessine enfin mon tabelau avec les parametres que je viens de définir
        self.__canvas.bind("<Button-1>",self.placercercle)                     #Je place aussi un bouton qui lance la fonction placer cercle a chaque clique

        self.__couleurjoueur= Label(self.__frame_principal,text=self.affichagejoueur(self.joueur),font=("Helvetica", 16), fg="blue" if joueur == 1 else "red",bg="black")
        self.__couleurjoueur.pack()                                            #Cette ligne permet l'affiche des joueurs en bleu et rouge sur ma frame

        self.__root.mainloop()                                                 #Enfin cette commande lance la fenetre où mon programme sera effectué



    def create_board(self):                                                     #cette fonction créer les liste où repose mon tableau , l'etat de la case est vide

        self.plateau= [[pion(0,0) for _ in range(self.__dimension)] for _ in range(self.__dimension)]

    def drawGame(self, board_width,board_height,canvas_width,canvas_height):          #cette fonction dessine mon tableau avec les paramètres definit plus haut

        self.__canvas.config(height=canvas_height,width=canvas_width)
        decalagex= (canvas_width - board_width) //2                                   #Je calcule la marge pour mon tableau par rapport a la fenetre
        decalagey= (canvas_height - board_height) //2                                 # //

        for x in range(self.__dimension):                                                               #Je créer un double if qui me permet de dessiner un tableau à double dimension
            for y in range(self.__dimension):
                x1= x * self.taillecellule + decalagex                                                  # Dans ces deux listes je repetes ces meme actions : calcules des coordonés du carré a placer
                y1= y * self.taillecellule + decalagey                                                  # Puis je dessines mes carrés en les décalent legerement pour créer le tableau demander
                x2= x1 + self.taillecellule
                y2= y1 + self.taillecellule
                self.__canvas.create_rectangle(x1,y1,x2,y2,fill="black",outline="white",width=1)


    def placercercle(self,event):                                                               #Cette fonction me permet de placer mes cercles avec le clique

        margex= (self.__canvas.winfo_width()- self.__dimension * self.taillecellule) //2        #je calcule la largeur totale du tableau grace a la taille du canvas
        margey= (self.__canvas.winfo_height()- self.__dimension * self.taillecellule) //2       #hauteur du tableau
        x= (event.x - margex) // self.taillecellule                                             #obtient les coordonés du clique en largeur sur notre tableau
        y= (event.y - margey) // self.taillecellule                                             #obtient les coordonés du clique en hauteur de notre tableau

        if 0 <=x < self.__dimension and 0 <=y < self.__dimension:                           #caclule si le cliqu se trouve bien dans notre zone de jeu
            x1= x * self.taillecellule + margex + self.taillecellule //4 - 7                #calcules les coordonées du cercles a placer x correspond a l'horizontale , y verticale , 1 point début cercle en haut a gauche , 2 en bas a droite
            y1= y * self.taillecellule + margey + self.taillecellule //4 - 7
            x2= x1 + self.taillecellule //2 + 14
            y2= y1 + self.taillecellule //2 + 14

            if self.plateau[x][y].etatcase== 0 and self.casevalide(x,y)== True:             #verifie si la case est sans pions et valide ( si la case se situe en L )
                if self.joueur== 1:                                                         # joueur 1 = bleu , joueur 2 = rouge
                    self.creercroix(self.__canvas,self.joueur)                              #fonction qui crée une croix bleu sur le cercle précedant
                    self.__canvas.create_oval(x1,y1,x2,y2,fill="blue")                      #crée un cercle bleu sur la case cliqué
                    self.plateau[x][y].etatcase = 1                                         #l'état de la case change ( pion bleu )
                    self.setDernierecroixj1(x,y)                                            # enrengistre les coordonés de la dernière croix
                    self.setDernierecasej1(x1,y1,x2,y2)                                     # enrengistre les coordoné de la dernière case
                    self.joueur= 2                                                          #fin de tour , c'est au joueur 2

                elif self.joueur== 2 and self.casevalide(x,y)== True:                       # //
                    self.creercroix(self.__canvas,self.joueur)                              # croix rouge  pion précedent
                    self.__canvas.create_oval(x1,y1,x2,y2,fill="red")                       #  cercle rouge case choisit
                    self.plateau[x][y].etatcase= 2                                          #  change etat case ( pion rouge )
                    self.setDernierecroixj2(x, y)                                           #  enrengiste coord. dernier croix
                    self.setDernierecasej2(x1,y1,x2,y2)                                     #  enrengistre coord. dernier cerlce
                    self.joueur= 1                                                          #  fin de tour , c'est au joueur 1
            self.__couleurjoueur.config(text=self.affichagejoueur(self.joueur),fg="blue" if self.joueur == 1 else "red")   #met a jour la couleur du joueur

    def affichagejoueur(self,joueur):                                           #Met a jour le contenu de l'affichage des joueurs

        if joueur== 1:
            return "Joueur 1"
        elif joueur== 2:
            return "Joueur 2"


    def creercroix (self,canvas,joueur) :                                      #fonction que me permet de créer des croix

        if joueur== 1 and self.__dernierecasej1 != 0:                          #pour créer un croix il doit y avoir déjà 1 tour de passé donc une valeur doit etre rentré
            x1, y1, x2, y2 = self.getDernierecasej1()                          #récupère la dernière case
            x,y = self.getDernierecroixj1()                                    #recupère la dernière croix
            self.__canvas.create_oval(x1,y1,x2,y2,fill="black")                #desiine un cercle noir sur le premier
            canvas.create_line  (x1,y1,x2 ,y2 ,fill="blue",width=4)            #dessine une première ligne bleu de haut gauche a bas droite
            canvas.create_line(x1+52-self.__dimension,y1,x2-52+self.__dimension,y2,fill="blue",width=4)     #en dessine une seconde de haut droite a bas gauche
            self.plateau[x][y].etatcase = 1.5                                  #l'etat de cette case change ( croix bleu )
            self.victoire()


        elif joueur ==2 and self.__dernierecasej2 != 0:                        # //
            x1,y1,x2,y2= self.getDernierecasej2()                              #recupère dern. case rouge
            x, y = self.getDernierecroixj2()                                   #recup. dern. croix rouge
            self.__canvas.create_oval(x1,y1,x2,y2,fill="black")                # //
            canvas.create_line(x1,y1,x2,y2,fill="red",width=4)                 # première ligne rouge
            canvas.create_line(x1+52-self.__dimension,y1,x2-52+self.__dimension,y2,fill="red",width=4)  # 2nd
            self.plateau[x][y].etatcase = 2.5                                   #l'etat de la case change ( croix rouge )
            self.victoire()


    def setDernierecasej1(self, x1=0,y1=0,x2=0,y2=0):                           #permet d'enrengistrer ma dernière case bleu
        self.__dernierecasej1= x1,y1,x2,y2
    def getDernierecasej1(self):                                                 # recuperer
        return self.__dernierecasej1
    def setDernierecasej2(self,x1=0,y1=0,x2=0,y2=0):                              # enrengistrer dernière case rouge
        self.__dernierecasej2= x1,y1, x2,y2
    def getDernierecasej2(self):                                                  #recuperer
        return self.__dernierecasej2


    def setDernierecroixj1(self, x,y):                                             #enrengistre dernière croix bleu
        self.__dernierecroixj1= x,y
    def getDernierecroixj1(self):                                                  #recuperer
        return self.__dernierecroixj1
    def setDernierecroixj2(self, x,y):                                              #enrengistrer dern . croix rouge
        self.__dernierecroixj2= x,y
    def getDernierecroixj2(self):                                                   #recuperer
        return self.__dernierecroixj2


    def casevalide(self,case_x,case_y):                                                    #verifie si la case choisit est en L par rapport a la précendente

        deplacementpossibles= [(-1,-2),(-2,-1),(-2,1),(-1,2),(1,-2),(2,-1),(2,1),(1,2)]  #repertorie les déplacement possibles

        x=0
        y=0

        if self.__dernierecasej1== 0 or self.__dernierecasej2== 0:                    #dans le cas du premier tour impossible de se déplacer en L
            return True
        elif self.joueur== 1:                                                         #recupère la dernière croix pour verifier le prochain déplacement
            x,y = self.getDernierecroixj1()
        elif self.joueur== 2:
            x,y = self.getDernierecroixj2()
                                                                                      # calcule si l'ancienne case + déplacement en L = nouvelle case
        for horizontalex , verticaley in deplacementpossibles:
            if (x+horizontalex== case_x) and (y+verticaley==case_y):
                return True

        return print("Déplacement non-valide")



    def victoire(self):

        nombrecroix=0

        for x in range(self.__dimension):
            for y in range(self.__dimension):

                if self.joueur== 1:
                    if self.plateau[x][y].etatcase== 1.5:
                        nombrecroix= nombrecroix + 1
                        if nombrecroix== self.conditionvictoire :
                            return True

                if self.joueur== 2:
                    if self.plateau[x][y].etatcase== 2.5:
                        nombrecroix= nombrecroix + 1
                        if nombrecroix== self.conditionvictoire:
                            return True






dimension = int(input("Quelle taille de jeu souhaitez-vous (8 - 12️) "))                           # demande la taille du plateau
while not 8 <= dimension <= 12:                                                                   #jusqu'à ce qu'elle convienne aux règles
    dimension = int(input("Quelle taille de jeu souhaitez-vous (8 - 12️) "))

conditionvictoire = int(input("Combien de pions faut-il aligner pour gagner (4 - 6) "))           #demande le nombre de pions pour gagner
while not 4 <= conditionvictoire <= 6:
    conditionvictoire = int(input("Combien de pions faut-il aligner pour gagner (4 - 6) "))

a = jeu(dimension, conditionvictoire)                                                             #lancer le constructeur de notre jeu


#J'ai beaucoup aimer travailler sur ce projet mais j'ai un peu manqué de temps pour faire quelque chose de plus propre ,
# j'aurais aimé travailler sur les bonus , ils avaient l'air abordable et interessant , ou aussi pouvoir créer une page de règles sympatique
# pour la dèrnière fonction je suis trop déçus de ne pas pouvoir la mener a bout mais je commençais un peu a saturer de python , je crois qu'on en est
#tous arrivé la en classe ,j'avais pour idée de faire une double boucle qui dès qu'elle rencontre un pion vérifie dans seulement 4 directions
# si les pions sont alignés , haut , diagonale haut droite droite diagonale bas droite , ainsi pas besoin de se demander si le dernier pion poser est en
# bout ou milieur de série , mais j'ai la  aussi manqué de temmps et de tests .
#Enfin je me suis inspiré des bout de codes de fireGUI et dawson_chess_GUI car j'avais oublié certaines mécaniques et fonctionnement