from fltk import*
import random
import math
import json
#################### Fonction du plateau ########################

###################################################################################################################
#                                                                                                                 #
# TOUTES LES COORDONNEES OU LES TAILLES DES OBJETS AFFICHEE A L'ECRAN SONT ECRITES EN FONCTION DE LA              #
# TAILLE DE LA FENETRE. POUR MODIFIER RAPIDEMENT LA TAILLE DE L'INTERFACE, MODIFIER X.                            #
#                                                                                                                 #
###################################################################################################################


e = 100 # écart à droite et en haut de la page pour afficher le score, qui a le tour et le bouton menu.
X = 601 + e # largeur de la fenêtre. Modifier seulement la valeur avant  "+ e"
Y = X - 50 # longueur de la fenêtre.


plt1 =[['x','x','x','x','x','x','x','x'], # Plateau du jeu
       ['x','x','x','x','x','x','x','x'],
       ['x','x','x','x','x','x','x','x'],
       ['x','x','x','R','J','x','x','x'],
       ['x','x','x','B','V','x','x','x'],
       ['x','x','x','x','x','x','x','x'],
       ['x','x','x','x','x','x','x','x'],
       ['x','x','x','x','x','x','x','x']]


def cadrillage() :
    """ Dessine la grille que l'on voit dans la partie"""
    for i in range(9) :
        ligne(float((X-e)/8)*i,e,float(((X-e)/8))*i,Y,'white')
        ligne(0,(float((Y-e)/8)*i)+e,X-e,(float((Y-e)/8)*i)+e,'white')
    ligne(X-e,0,X-e,Y,'white')
    ligne(0,e,X,e,'white')
    ligne(0,((Y-e)/8)*2+e,X,((Y-e)/8)*2+e,'white')
    ligne(0,((Y-e)/8)*4+e,X,((Y-e)/8)*4+e,'white')
    ligne(0,((Y-e)/8)*6+e,X,((Y-e)/8)*6+e,'white')
    

def place_case(x,y):
    """Convertit les coordonnées du clique du joueur en indices du plateau."""
    largeur_case = (X - e) / 8
    hauteur_case = (Y - e) / 8
    
    colonne = int(x // largeur_case)
    ligne = int((y - e) // hauteur_case)

    return ligne, colonne


################### comptent le score et affiche le(s) gagant(s) ######### (presque fini) ###############


def score(liste,j):
    """Affiche le score a la fin de la partie et prend en compte les égalités"""
    # compte le score
    bleu = 0
    rouge = 0
    jaune = 0
    vert = 0
    for k in range(len(liste)):
        for i in range(len(liste)):     
            if liste[k][i] == 'B':
                bleu += 1
            elif liste[k][i] == 'R':
                rouge += 1
            elif liste[k][i] == 'J':
                jaune +=  1
            elif liste[k][i] == 'V':
                vert += 1
    score = [rouge,vert,jaune,bleu]
    joueurs = ["joueur Rouge","joueur Vert","joueur Jaune ","joueur Bleu"]
    color = ['red','green','yellow','blue']
    # Le plus gros score
    max_score = max(score)
    ############
    # Crée la liste de tous les joueur qui on un score égale au max_score
    gagnants = [joueurs[i] for i in range(j) if score[i] == max_score]
    # Donne la liste des couleurs gagnantes
    clr = [color[i] for i in range(j) if score[i] == max_score]
    # affiche les joueurs qui sont égalités
    if len(gagnants) == 2:
        texte(X/2,Y/8,f"Il y a égalité entre le {gagnants[0]} et le {gagnants[1]}", ancrage ='center', taille=int(X/32))
    elif len(gagnants) == 3:
        texte(X/2,Y/8,f"Il y a égalité entre le {gagnants[0]}, le {gagnants[1]} et le {gagnants[2]}", ancrage ='center', taille=int(X/42))
    elif len(gagnants) == 4:
        texte(X/2,Y/8,f"Il y a égalité entre le {gagnants[0]}, {gagnants[1]}, {gagnants[2]} et {gagnants[3]}", ancrage = 'center', taille=int(X/45))
    else :
        # Si il n'y a pas d'egalité, affiche le gagnant
        texte(X/2,Y/10,f"Le {gagnants[0]} a gagné ! ",taille=40, couleur = clr,ancrage = 'center', police = 'Impact')
    # Affiche le score de tout le monde
    if j == 4 :
        texte(X/2,Y/5,'Le joueur Rouge a '+str(rouge)+' points','red', ancrage = 'center')
        texte(X/2,2*Y/5,'Le joueur Vert a '+str(vert)+' points','green', ancrage = 'center')
        texte(X/2,3*Y/5,'Le joueur Jaune a '+str(jaune)+' points','yellow', ancrage = 'center')   
        texte(X/2,4*Y/5,'Le joueur Bleu a '+str(bleu)+' points','blue', ancrage = 'center')
    elif j == 3 :
        texte(X/2,Y/5,'Le joueur Rouge a '+str(rouge)+' points','red', ancrage = 'center')
        texte(X/2,2*Y/5,'Le joueur Vert a '+str(vert)+' points','green', ancrage = 'center')
        texte(X/2,3*Y/5,'Le joueur Jaune a '+str(jaune)+' points','yellow', ancrage = 'center')
    else :
        texte(X/2,2*Y/5,'Le joueur Rouge a '+str(rouge)+' points','red', ancrage = 'center')
        texte(X/2,3*Y/5,'Le joueur Vert a '+str(vert)+' points','green', ancrage = 'center')
        
        
def score_en_continue(liste,nb_j):
    """Affiche le score en direct pendant la partie"""
    # Compte le score
    bleu = 0
    rouge = 0
    jaune = 0
    vert = 0
    for k in range(len(liste)):
        for i in range(len(liste)):     
            if liste[k][i] == 'B':
                bleu += 1
            elif liste[k][i] == 'R':
                rouge += 1
            elif liste[k][i] == 'J':
                jaune +=  1
            elif liste[k][i] == 'V':
                vert += 1
    score = [rouge,vert,jaune,bleu] 
    # Affichage pour chaque cas
    # Si il y a 4 joueur
    if nb_j == 4 :
        texte(X-e/2,e +(X/32),'Rouge','red', ancrage = 'center',taille = int(e/5))
        r = texte(X-(e)/2,e + (X/12),str(score[0]),'red', ancrage = 'center',taille = int(e/5))
        texte(X-e/2,e +(X/7),'points','red', ancrage = 'center',taille = int(e/5))
        texte(X-e/2,((Y-e)/8)*2+e+(X/32),'Vert','green',ancrage = 'center',taille = int(e/5))
        v = texte(X-e/2,((Y-e)/8)*2+e+(X/12),str(score[1]),'green', ancrage = 'center', taille = int(e/5))
        texte(X-e/2,((Y-e)/8)*2+e+(X/7),'points','green', ancrage = 'center',taille = int(e/5))
        texte(X-e/2,((Y-e)/8)*4+e+(X/32),'Jaune','yellow', ancrage = 'center',taille = int(e/5))
        y = texte(X-e/2,((Y-e)/8)*4+e+(X/12),str(score[2]),'yellow', ancrage = 'center', taille = int(e/5))
        texte(X-e/2,((Y-e)/8)*4+e+(X/7),'points','yellow', ancrage = 'center',taille = int(e/5))
        texte(X-e/2,((Y-e)/8)*6+e+(X/32),'Bleu','blue', ancrage = 'center',taille = int(e/5))
        b = texte(X-e/2,((Y-e)/8)*6+e+(X/12),str(score[3]),'blue', ancrage = 'center', taille = int(e/5))
        texte(X-e/2,((Y-e)/8)*6+e+(X/7),'points','blue', ancrage = 'center',taille = int(e/5))
        return r,v,y,b
    # Si il y a 3 joueurs
    elif nb_j == 3 :
        r = texte(X-(e)/2,e + (X/12),str(score[0]),'red', ancrage = 'center',taille = int(e/5))
        v = texte(X-e/2,((Y-e)/8)*2+e+(X/12),str(score[1]),'green', ancrage = 'center',taille = int(e/5))
        y = texte(X-e/2,((Y-e)/8)*4+e+(X/12),str(score[2]),'yellow', ancrage = 'center',taille = int(e/5))
        texte(X-e/2,e +(X/32),'Rouge','red', ancrage = 'center',taille = int(e/5))
        texte(X-e/2,e +(X/7),'points','red', ancrage = 'center',taille = int(e/5))
        texte(X-e/2,((Y-e)/8)*2+e+(X/32),'Vert','green',ancrage = 'center',taille = int(e/5))
        texte(X-e/2,((Y-e)/8)*2+e+(X/7),'points','green', ancrage = 'center',taille = int(e/5))
        texte(X-e/2,((Y-e)/8)*4+e+(X/32),'Jaune','yellow', ancrage = 'center',taille = int(e/5))
        texte(X-e/2,((Y-e)/8)*4+e+(X/7),'points','yellow', ancrage = 'center',taille = int(e/5))
        return r,v,y
    # Si il y a 2 joueurs
    else :
        r = texte(X-(e)/2,e + (X/12),str(score[0]),'red', ancrage = 'center',taille = int(e/5))
        v = texte(X-e/2,((Y-e)/8)*2+e+(X/12),str(score[1]),'green', ancrage = 'center',taille = int(e/5))
        texte(X-e/2,e +(X/32),'Rouge','red', ancrage = 'center',taille = int(e/5))
        texte(X-e/2,e +(X/7),'points','red', ancrage = 'center',taille = int(e/5))
        texte(X-e/2,((Y-e)/8)*2+e+(X/32),'Vert','green',ancrage = 'center',taille = int(e/5))
        texte(X-e/2,((Y-e)/8)*2+e+(X/7),'points','green', ancrage = 'center',taille = int(e/5))
        return r,v
    
        

################### Fonctions : horizontal, vertical, diagonale ##########################
    

def horizontal(plt,l,c):
    """Si deux boules de même couleur sont relié horizontalement par d'autres boules alors, les 
             boules situé entre celle-ci deviennent de la même couleur"""
    
    # Le processus est le même pour chaque fonction, mais adapter pour chaque fonction
    #  Toutes les ligne i = 8, r = 8... Représente l'arrêt de la fonction
    
    # On vas regarde si deux boules ne sont pas aligné horizontalement à droite
    #    de la où on pose la boule
    i = 0                                      
    while i <= 7:                               
        i +=1
        # On s'assure qu'on ne sort pas du plateau
        if c+i <= 7:
            # Si on trouve du vide on s'arrête
            if plt[l][c+i] != 'x' :
                # Si on trouve une boule de la même couleur
                if plt[l][c+i] == plt[l][c] :
                    # On remplace ce qu'il ya entre les deux boules
                    for y in range(c,c+i):       
                        plt[l][y] = plt[l][c]    
                        i = 8                    
            else :                               
                i = 8
                
    # On vas regarde si deux boules ne sont pas aligné horizontalement à gauche
    #    de la où on pose la boule
    r = 0                                  
    while r <= 7 :                           
        r +=1                                
        if c-r >= 0 :
            if plt[l][c-r] != 'x' :
                if plt[l][c-r] == plt[l][c] :   
                    for y in range(r) :
                        plt[l][c-y] = plt[l][c]
                        r = 8
            else :
                r = 8


def vertical(plt,l,c):
    """Si deux boules de même couleur sont relié a la verticale par d'autres boules alors, les 
             boules situé entre celle-ci deviennent de la même couleur"""
    
    # Le principe est le même que pour la fonction horizontale sauf
    #    que là on vas regarder verticalement
    
    # On vas regarde si deux boules ne sont pas aligné verticalement
    #   en dessous de la où on pose la boule
    i = 0
    while i <= 7:
        i += 1
        if l+i <= 7:
            if plt[l+i][c] != 'x' :
                if plt[l+i][c] == plt[l][c] :   
                    for y in range(l,l+i):      
                        plt[y][c] = plt[l][c]   
                        i = 8
            else :
                i = 8
                
    # On vas regarde si deux boules ne sont pas aligné verticalement
    #   au dessus de la où on pose la boule
    r = 0                                  
    while r <= 7:                           
        r +=1                               
        if l-r >= 0 :
            if plt[l-r][c] != 'x' :
                if plt[l-r][c] == plt[l][c] :    
                    for y in range(r) :       
                        plt[l-y][c] = plt[l][c] 
                        r = 8
            else :
                r = 8
                
            
def diagonale(plt,l,c):
    """Si deux boules de même couleur sont relié en diagonale par d'autres boules alors, les 
             case situé entre celle-ci deviennent de la même couleur"""
    
    # Ici on vas chercher a regarder verticalement et horizontalement
    #   pour obtenir une diagonale
    
    # En bas à droite
    i = 0                          
    while i <= 7 :                                
        i+=1                                    
        if c+i <= 7 and l+i <= 7:
            if plt[l+i][c+i] != 'x' :
                if plt[l+i][c+i] == plt[l][c] :     
                    for y in range(i):              
                        plt[l+y][c+y] = plt[l][c]   
                        i = 8
            else :
                i = 8
    # En bas à gauche
    r = 0                                       
    while r <= 7 :
        r+=1                                    
        if 0 <= c+r <= 7 and 0 <= l-r <= 7 :
            if plt[l-r][c+r] != 'x' :
                if plt[l-r][c+r] == plt[l][c] :     
                    for y in range(r):              
                        plt[l-y][c+y] = plt[l][c]   
                        r = 8
            else :
                r = 8
                
    # En haut à droite
    z = 0
    while z <= 7 :                              
        z+=1                                    
        if 0 <= c-z <= 7 and 0 <= l+z <= 7 :
            if plt[l+z][c-z] != 'x' :
                if plt[l+z][c-z] == plt[l][c] :     
                    for y in range(z):              
                        plt[l+y][c-y] = plt[l][c]   
                        z = 8
            else :
                z = 8
                
    # En haut à gauche
    k = 0
    while k <= 7 :                              
        k+=1                                    
        if 0 <= c-k <= 7 and 0 <= l-k <= 7 :
            if plt[l-k][c-k] != 'x' :
                if plt[l-k][c-k] == plt[l][c] :     
                    for y in range(k):              
                        plt[l-y][c-y] = plt[l][c]
                        k = 8
            else :
                k = 8


########################## Fonction verif ######################################################


def verif_case(liste,l,c):
    """Empêche le joueur de poser sa boule si il n'est pas adjacent a une autre boule"""
    for i in range(-1,2):
        for r in range(-1,2):
            if 0 <= l+i <= 7 and 0<= c+r <= 7:
                if liste[l+i][c+r] != 'x':
                    return True
    return False


def verif_plateau(liste):
    """Verifie si dans le plateau il reste au moin une case vide"""
    for b in range(len(liste)):
        for i in range(len(liste)):
            if liste[b][i] == 'x':
                return True
    return False


#################################################################################


def pose_couleur(liste):
    """ Pose les boules graphiquement en fonction du plateau"""
    # Taille des cercles
    t = (Y-e)/17
    #############
    for i in range(8):
        for b in range(8):
            if liste[i][b] == 'B' :
                cercle(b *(X-e)/8 + (((X-e)/2)/8),(i *((Y - e)/8))+e+(((Y - e)/2)/8),t,'black','blue',2)
            elif liste[i][b] == 'R' :
                cercle(b *(X-e)/8 + ((X-e)/2/8),(i *((Y - e)/8))+e+(((Y - e)/2)/8),t,'black','red',2)
            elif liste[i][b] == 'J' :
                cercle(b *(X-e)/8 + ((X-e)/2/8),(i *((Y - e)/8))+e+(((Y - e)/2)/8),t,'black','yellow',2)
            elif liste[i][b] == 'V' :
                cercle(b *(X-e)/8 + ((X-e)/2/8),(i *((Y - e)/8))+e+(((Y - e)/2)/8),t,'black','green',2)
            elif liste[i][b] == 'x' :
                cercle(b *(X-e)/8 + ((X-e)/2/8),(i *((Y - e)/8))+e+(((Y - e)/2)/8),t-5,'grey','grey')


def jeu(joueur,plt,h,nb_j):
    """Pose les couleur, verifie si la case est valide et effectue les opérations
         en diagonale,verticale et horizontale et affiche les erreur du joueurs"""
    # Regarde quel joueur joue
    if joueur == 1:
        couleur = 'red'
    elif joueur == 2 :
        couleur = 'green'
    elif joueur == 3 :
        couleur = 'yellow'
    elif joueur == 4 :
        couleur = 'blue'
    pose_couleur(plt)
    while True :
        ev = attend_ev()
        if type_ev(ev) == 'ClicGauche':
            x = abscisse(ev)
            y = ordonnee(ev)
            if y > e and x < X-e :
                l,c = place_case(x,y)
                if plt[l][c] == 'x':
                    if verif_case(plt,l,c) :
                        if joueur == 1 :
                            plt[l][c] = 'R'
                        elif joueur == 2 :
                            plt[l][c] = 'V'
                        elif joueur == 3 :
                            plt[l][c] = 'J'
                        elif joueur == 4 :         
                            plt[l][c] = 'B'
                        horizontal(plt,l,c)
                        vertical(plt,l,c)
                        diagonale(plt,l,c)
                        efface(h)
                        return True
                    else :
                        efface(h)
                        h = texte(X*2/5,e/2,"Tu n'as pas le droit de faire ça !",couleur ,ancrage='center')
                else :
                    efface(h)
                    h = texte(X*2/5,e/2,"  Il y a déja une couleur sur cette case !",couleur ,ancrage='center')
            elif y < e and x > X-e :
                with open('sauvegarde_jeu', 'w') as fichier :
                    sauv = {'plateau' : plt , 'tour_joueur' : joueur , 'nombre_de_joueur' : nb_j}
                    json.dump(sauv, fichier, indent = 4)
                return False
            else :
                efface(h)
                h = texte(X*2/5,e/2,"Veuillez choisir une case du plateau ",couleur ,ancrage='center')
        elif type_ev(ev) == 'Quitte' :
            with open('sauvegarde_jeu', 'w') as fichier :
                sauv = {'plateau' : plt , 'tour_joueur' : joueur , 'nombre_de_joueur' : nb_j}
                json.dump(sauv, fichier, indent = 4)
            ferme_fenetre()


def ordre_joueurs(j,nb_j):
    """Donne l'ordre des joueurs sur le plateau et l'affiche"""
    if j == nb_j :
        j = 1
    else :
        j = j + 1
    if j == 1 :
        h = texte(X*2/5,e/2,'Au tour du joueur Rouge','red' ,ancrage='center',police = 'calibri',taille = int(X/28))
    elif j == 2 :
        h = texte(X*2/5,e/2,'Au tour du joueur Vert','green' ,ancrage='center',police = 'calibri',taille = int(X/28))
    elif j == 3 :
        h = texte(X*2/5,e/2,'Au tour du joueur Jaune','yellow' ,ancrage='center',police = 'calibri',taille = int(X/28))
    elif j == 4 :
        h = texte(X*2/5,e/2,'Au tour du joueur Bleu','blue' ,ancrage='center',police = 'calibri',taille = int(X/28))
    return j,h


def choix_nb_joueur():
    """ Renvoie le choix du nombre de joueurs"""
    # Interface
    rectangle(0,0,X,Y,'black','black')
    cercle((X/4),(Y/2)+X/12,int(X/9),'white',remplissage = 'blue',epaisseur = 5)
    cercle((X/2),(Y/2)+X/12,int(X/9),'white',remplissage = 'red',epaisseur = 5)
    cercle((3*X/4),(Y/2)+X/12,int(X/9),'white',remplissage = 'green',epaisseur = 5)
    texte(X/2, Y/4, 'Quel est le nombre de joueur ?','white', ancrage= 'center', taille = int(X/19))
    texte((X/4),(Y/2+X/12), '2','white', ancrage='center',taille = int(X/8))
    texte((X/2),(Y/2+X/12), '3','white', ancrage='center',taille = int(X/8))
    texte((3*X/4),(Y/2+X/12), '4','white', ancrage='center',taille = int(X/8))
    while True :
        # Donne le choix du joueur en fonction des coordonnées du clique
        ev = attend_ev()
        if type_ev(ev) == 'ClicGauche':
            x =  abscisse(ev)                
            y = ordonnee(ev)
            if math.sqrt(((y - ((Y/2)+X/12))**2)+((x - (X/4))**2)) <= int(X/9) :
                return 2
            elif math.sqrt(((y - ((Y/2)+X/12))**2)+((x - (X/2))**2)) <= int(X/9) :
                return 3
            elif math.sqrt(((y - ((Y/2)+X/12))**2)+((x - (3*X/4))**2)) <= int(X/9) :
                return 4
        elif type_ev(ev) == 'Quitte':
            ferme_fenetre()


def menu():
    """ Demande si le joueur veut jouer une nouvelle partie ou si il veut continuer la précedente
            et permet aussi au joueur de revoir les règles du jeu"""
    while True :
        # Interface
        hauteur_case = (2*Y/15)
        rectangle(0,0,X,Y, 'white','white')
        texte(X/2,Y/6, 'ROLIT', ancrage = 'center', taille = int(X/6),couleur = 'black', police = 'david libre')
        rectangle((X/6),3*Y/7+hauteur_case/2,X-(X/6),3*Y/7-hauteur_case/2,'red',epaisseur = 3)
        rectangle((X/6),(5*Y/8)+hauteur_case/2,X-(X/6),(5*Y/8)-hauteur_case/2,'green',epaisseur = 3)
        rectangle((X/6),(9*Y/11)+hauteur_case/2,X-(X/6), (9*Y/11)-hauteur_case/2,'yellow', epaisseur = 3)
        texte(X/2,3*Y/7,'Continuer la partie', ancrage = 'center', taille = int(X/20),police = 'dejavu math tex gyre')
        texte(X/2,5*Y/8,'Nouvelle partie', ancrage = 'center', taille = int(X/20),police = 'dejavu math tex gyre')
        texte(X/2,9*Y/11,'Règles', ancrage = 'center', taille = int(X/20),police = 'dejavu math tex gyre')
        while True :
            clic = attend_ev()
            # Regarde le choix du joueur
            if type_ev(clic) == 'ClicGauche' :  
                if (X/6) < abscisse(clic) < X-(X/6) :
                    if (3*Y/7)-hauteur_case/2 < ordonnee(clic) < (3*Y/7)+hauteur_case/2 :
                        return 'partie_sauvegarde'
                    elif (5*Y/8)-hauteur_case/2 < ordonnee(clic) < (5*Y/8)+hauteur_case/2 :
                        return 'nvl_partie'
                    elif (9*Y/11)-hauteur_case/2 < ordonnee(clic) < (9*Y/11)+hauteur_case/2 :
                        rectangle(e,e,X-e,(9*Y/11)+hauteur_case/2,'black','black')
                        # REGLES DU JEU
                        texte(e+10,e+20,"- Le joueur qui commence est choisi aléatoirement",'white',taille = int(X/45))
                        texte(e+10,e+70,"- Chaque joueur doit placer une seule boule par tour",'white', taille = int(X/45))
                        texte(e+10,e+120,"- Le joueur doit poser sa boule sur une case vide", 'white', taille = int(X/43))
                        texte(e+10,e+170,"- Le joueur doit placer sa boule adjacente à une autre.",'white', taille = int(X/45))
                        texte(e+10,e+220,"- Une capture est effectué lorsqu'on pose une boules,",'white',taille = int(X/45))
                        texte(e+10,e+240,"  et qu'elle est relié a une autre boule de sa couleur par",'white',taille = int(X/45))
                        texte(e+10,e+260,"  les boules des autres couleurs",'white',taille = int(X/45))
                        texte(e+10,e+310,"- Plusieurs captures peuvent être éffectué avec",'white',taille = int(X/45))
                        texte(e+10,e+330,"  une seul boule",'white',taille = int(X/45))
                        texte(e+10,e+360,"- Le jeu prend fin dès que le plateau est remplie",'white', taille = int(X/45))
                        texte(e+10,Y-e-60,"- Le joueur avec le plus de boule à la fin de la partie",'white', taille = int(X/43))
                        texte(e+10,Y-e-40,'  a gagné','white', taille = int(X/43))
                        while type_ev(clic) == 'ClicGauche' and e < abscisse(clic) < X-e and e < ordonnee(clic) < (9*Y/11)+hauteur_case/2 :
                            clic = attend_ev()
                            if type_ev(clic) == 'Quitte' :
                                ferme_fenetre()
                        efface_tout()
                        break
                
            elif type_ev(clic) == 'Quitte' :
                ferme_fenetre()
            

def sauvegarde_presente():
    """verifie qu'il y a une sauvegarde à chargé"""
    try:
        with open('sauvegarde_jeu', 'r'):
            return True 
    except FileNotFoundError:
        return False


def sauvegarde():
    """ Renvoie les données de la partie sauvegardé """
    try :
        with open('sauvegarde_jeu','r') as fichier :
            sauvegarde = json.load(fichier)
            j = sauvegarde['tour_joueur']
            nb_j = sauvegarde['nombre_de_joueur']
            plt = sauvegarde['plateau']
        return j,nb_j,plt
    except FileNotFoundError :
        return None


def parti():
    """Fonction principale du jeu"""
    cree_fenetre(X,Y)
    while True :
        choix = menu()
        # Le joueur choisi de continuer la partie
        if choix == 'partie_sauvegarde' and sauvegarde_presente() :
            j, nb_j, plt = sauvegarde()
        # Le joueur choisi de joueur une nouvelle partie
        else :
            efface_tout()
            plt = [['x','x','x','x','x','x','x','x'],
           ['x','x','x','x','x','x','x','x'],
           ['x','x','x','x','x','x','x','x'],
           ['x','x','x','R','J','x','x','x'],
           ['x','x','x','B','V','x','x','x'],
           ['x','x','x','x','x','x','x','x'],
           ['x','x','x','x','x','x','x','x'],
           ['x','x','x','x','x','x','x','x']]
            nb_j = choix_nb_joueur()
            j = random.randint(1,nb_j)
        efface_tout()
        rectangle(0,0,X,Y, 'black','black')
        rectangle(0,0,X-1,Y-1,'white')
        cadrillage()
        if j == 1 :
            h = texte(X*3/7,e/2,'Le joueur Rouge commence','red', ancrage = 'center',taille = int(X/28),police='calibri')
        elif j == 2 :
            h = texte(X*3/7,e/2,'Le joueur Vert commence','green', ancrage = 'center',taille = int(X/28),police='calibri')
        elif j == 3 :                                                     
            h = texte(X*3/7,e/2,'Le joueur Jaune commence','yellow', ancrage = 'center',taille = int(X/28),police='calibri')
        elif j == 4 :
            h = texte(X*3/7,e/2,'Le joueur Bleu commence','blue', ancrage = 'center',taille = int(X/28),police='calibri')
        # Dessine le bouton menu
        rectangle(X-e+20,40,X-20,e-20, 'white','white')
        polygone([X-e+10,40,X-10,40,X-e/2,10],'white','white')
        while verif_plateau(plt): # Tant qu'il reste des cases vides dans le plateau :
            
            # Actualise le score en direct
            if nb_j == 4 :
                r,v,y,b = score_en_continue(plt,nb_j)
            elif nb_j == 3 :
                r,v,y = score_en_continue(plt,nb_j)
            else :
                r,v = score_en_continue(plt,nb_j)
            ################
            # Fais jouer le joueur
            home = jeu(j,plt,h,nb_j)
            j,h = ordre_joueurs(j,nb_j)
            ################
            # Efface le score en direct
            if nb_j == 4 :
                efface(r)
                efface(v)
                efface(y)
                efface(b)
            elif nb_j == 3 :
                efface(r)
                efface(v)
                efface(y)
            else :
                efface(r)
                efface(v)
            ##############
            # Si le joueur clique sur le bouton menu le jeu s'arrête
            if not home :
                break
        # Si le joueur n'as pas cliqué sur le bouton menu
        if home :
            # Fin de la partie, attend une action pour le retour au menu
            pose_couleur(plt)
            attend_ev()
            efface_tout()
            rectangle(0,0,X,Y,'white','white')
            score(plt,nb_j)
            fin = attend_ev()
            if type_ev(fin) == 'Quitte':
                ferme_fenetre()


if __name__ == '__main__' :


    parti()