Projet L2 Informatique - 6 janvier 2026
Auteurs : Laldji Dani et Honoré Hugo

Description :
Ce programme compare les performances de différentes structures de données 
pour compter les occurrences de mots dans un texte.


1. COMPILATION

Le programme a été codé en C standard.
Il nécessite les bibliothèques classiques : <stdio.h>, <stdlib.h>, <string.h>, <ctype.h>, <time.h>.

Pour compiler via un terminal :
   clang Projet.c -o projet

2. EXECUTION

Commande :
   ./projetg [fichier_texte] [num_algo] [taille_min]

Paramètres :
   - [fichier_texte] : Le chemin du livre à analyser (ex: text-1.txt).
   - [num_algo]      : Le choix de la structure de données (voir liste ci-dessous).
   - [taille_min]    : (Optionnel) Ignore les mots inférieurs à cette taille. Mettre 0 pour tout prendre.

Liste des Algorithmes :
   1 : Liste Chaînée Simple
   2 : Arbre de Recherche
   3 : Tableau de liste
   4 : Liste Chaînée Triée

Exemple d'utilisation :
   ./projetg text-1.txt 2 4
   (Lance l'Arbre Binaire sur le texte, en gardant uniquement les mots de 4 lettres ou plus).

3. RESULTATS

Le programme affiche le TOP N des mots les plus fréquents dans la console.

Fichiers générés :
- resultat.txt     : Contient la liste des mots trouvés (si demandé par l'utilisateur).
- performances.csv : Ajoute une ligne avec le temps d'exécution et la mémoire utilisée (pour les graphes).

Plus d'infos dans le rapport PDF.