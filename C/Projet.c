#include <stdio.h>
#include <stdlib.h>
#include <string.h> 
#include <ctype.h>
#include <time.h> 


// 1. STRUCTURES (INTOUCHÉES)
//=====================================================

typedef struct {
    size_t cumul_alloc;
    size_t cumul_desalloc;
    size_t max_alloc;
} InfoMem;

// ALGO 1, 3 et 4 : CELLULE (Liste simple, Dico, Liste Triée)
typedef struct Cellule {
    char* mot;
    int occurence;
    struct Cellule* suivant;
} Cellule, *Liste;

// ALGO 2 : ARBRE
typedef struct Noeud {
    char* mot;
    int occurence;
    struct Noeud* gauche;
    struct Noeud* droite;
} Noeud, *Arbre;

// STRUCTURE POUR LE TRI FINAL
typedef struct {
    char* mot;
    int occurence;
} ElementTri;

// =========================================================


// Fonctions pour la memoire
void* myMalloc(size_t t, InfoMem* im) {
    void* p = malloc(t);
    if (im != NULL && p != NULL) {
        im->cumul_alloc += t;
        // calcul du max utilisé
        size_t actuel = im->cumul_alloc - im->cumul_desalloc;
        if (actuel > im->max_alloc) {
            im->max_alloc = actuel;
        }
    }
    return p;
}

void myFree(void* p, InfoMem* im, size_t t) {
    if (p != NULL) {
        free(p);
        if (im != NULL) {
            im->cumul_desalloc += t; 
        }
    }
}

void* myRealloc(void* p, size_t new_t, InfoMem* im, size_t old_t) {
    void* new_p = realloc(p, new_t);

    if (im && new_p != NULL) {
        if (new_p == p) {
            // meme adresse
            if (new_t > old_t) im->cumul_alloc += (new_t - old_t);
            else im->cumul_desalloc += (old_t - new_t);
        }
        else {
            // adresse change
            im->cumul_alloc += new_t;
            if (p != NULL) im->cumul_desalloc += old_t;
        }

        size_t act = im->cumul_alloc - im->cumul_desalloc;
        if (act > im->max_alloc) im->max_alloc = act;
    }
    return new_p;
}

// Lecture du fichier mot par mot
char* get_mot(FILE* f, InfoMem* im) {
    char buf[256];
    int i = 0;
    int c;

    // on saute les caracteres speciaux au debut
    while ((c = fgetc(f)) != EOF) {
        if (isalpha(c) || (unsigned char)c > 127) { 
            ungetc(c, f); 
            break;
        }
    }

    if (c == EOF) return NULL;

    // lecture
    while ((c = fgetc(f)) != EOF) {
        // on prend lettres et tirets
        if (isalpha(c) || c == '-' || (unsigned char)c > 127) {
            if (i < 255) buf[i++] = c;
        } else {
            break; 
        }
    }
    buf[i] = '\0';

    // si le mot fini par un tiret on l'enleve
    if (i > 0 && buf[i-1] == '-') {
        buf[i-1] = '\0';
        i--; 
    }

    // allocation de la chaine
    char* res = (char*)myMalloc((i + 1) * sizeof(char), im);
    if (res) strcpy(res, buf);
    
    return res;
}

// Verif si le mot est valide (pas juste de la ponctuation)
int check_mot(char* m) {
    if (m == NULL || strlen(m) == 0) return 0;
    if (strcmp(m, "«") == 0) return 0;
    if (strcmp(m, "»") == 0) return 0;
    if (strcmp(m, "—") == 0) return 0;
    if (strcmp(m, "–") == 0) return 0;
    if (strcmp(m, "-") == 0) return 0;
    return 1;
}


// --- ALGOS ---

// Algo 1
int ajoutListe(Liste *l, char *m, InfoMem *im) {
    Cellule *tmp = *l;
    // parcours pour voir si existe
    while (tmp) {
        if (strcmp(tmp->mot, m) == 0) {
            tmp->occurence++;
            myFree(m, im, strlen(m) + 1); 
            return 0; 
        }
        tmp = tmp->suivant;
    }
    // ajout en tete
    Cellule *new = (Cellule*)myMalloc(sizeof(Cellule), im);
    if (new) {
        new->mot = m;
        new->occurence = 1;
        new->suivant = *l;
        *l = new;
        return 1; 
    }
    return 0;
}

// Algo 2
int ajoutArbre(Arbre *r, char *m, InfoMem *im) {
    if (*r == NULL) {
        Noeud *new = (Noeud*)myMalloc(sizeof(Noeud), im);
        if (new) {
            new->mot = m;
            new->occurence = 1;
            new->gauche = NULL;
            new->droite = NULL;
            *r = new;
            return 1; 
        }
        return 0;
    } 
    int cmp = strcmp(m, (*r)->mot);
    if (cmp == 0) {
        (*r)->occurence++;
        myFree(m, im, strlen(m) + 1);
        return 0; 
    } else if (cmp < 0) {
        return ajoutArbre(&((*r)->gauche), m, im);
    } else {
        return ajoutArbre(&((*r)->droite), m, im);
    }
}

// Algo 3
int ajoutDico(Liste tab[], char *m, InfoMem *im) {
    char c = tolower(m[0]);
    int idx = c - 'a';
    if (idx < 0 || idx > 25) idx = 0;
    return ajoutListe(&tab[idx], m, im);
}

// Algo 4 (Trié)
int ajoutListeTriee(Liste *l, char *m, InfoMem *im) {
    Cellule *curr = *l;
    Cellule *prec = NULL;
    
    // on cherche la place
    while (curr != NULL && strcmp(curr->mot, m) < 0) {
        prec = curr;
        curr = curr->suivant;
    }
    
    if (curr != NULL && strcmp(curr->mot, m) == 0) {
        curr->occurence++;
        myFree(m, im, strlen(m) + 1);
        return 0; 
    }
    
    Cellule *new = (Cellule*)myMalloc(sizeof(Cellule), im);
    if (new) {
        new->mot = m;
        new->occurence = 1;
        new->suivant = curr; 
        if (prec == NULL) *l = new;
        else prec->suivant = new;
        return 1; 
    }
    return 0;
}


// --- RESULTATS ---

int compare(const void* a, const void* b) {
    const ElementTri* ea = (const ElementTri*)a;
    const ElementTri* eb = (const ElementTri*)b;
    return (eb->occurence - ea->occurence);
}

void recup_liste(Liste l, ElementTri* t, int* i) {
    while (l) {
        t[*i].mot = l->mot;
        t[*i].occurence = l->occurence;
        (*i)++;
        l = l->suivant;
    }
}

void recup_arbre(Arbre a, ElementTri* t, int* i) {
    if (a != NULL) {
        recup_arbre(a->gauche, t, i);
        t[*i].mot = a->mot;
        t[*i].occurence = a->occurence;
        (*i)++;
        recup_arbre(a->droite, t, i);
    }
}

void affichage(Liste l, Arbre a, Liste dico[], int algo, int total) {
    if (total == 0) {
        printf("Rien trouve.\n");
        return;
    }

    int n;
    printf("\nNb de mots a afficher ? : ");
    if (scanf("%d", &n) != 1) { 
        n = 10; 
        int c; while ((c = getchar()) != '\n' && c != EOF); 
    } 
    if (n > total) n = total;
    if (n < 1) n = 1;

    ElementTri* tab = malloc(total * sizeof(ElementTri));
    if (tab == NULL) return;

    int idx = 0;
    if (algo == 1 || algo == 4) recup_liste(l, tab, &idx);
    else if (algo == 2) recup_arbre(a, tab, &idx);
    else if (algo == 3) {
        for(int k=0; k<26; k++) recup_liste(dico[k], tab, &idx);
    }

    qsort(tab, total, sizeof(ElementTri), compare);

    printf("\n--- TOP %d ---\n", n);
    for (int i = 0; i < n; i++) {
        printf("%d. %s : %d\n", i + 1, tab[i].mot, tab[i].occurence);
    }

    // sauvegarde resultat.txt
    printf("\nSauvegarder dans 'resultat.txt' ? (o/n) : ");
    char rep;
    scanf(" %c", &rep); 

    if (rep == 'o' || rep == 'O') {
        FILE* out = fopen("resultat.txt", "w");
        if (out) {
            for (int i = 0; i < n; i++) {
                fprintf(out, "%s %d\n", tab[i].mot, tab[i].occurence);
            }
            fclose(out);
            printf("Fichier resultat.txt cree.\n");
        } else {
            printf("Erreur creation fichier\n");
        }
    }

    free(tab);
}

void save_perf(const char* algo, const char* fic, int nb, double t, size_t m) {
    FILE* f = fopen("performances.csv", "a");
    if (f == NULL) return;
    
    fseek(f, 0, SEEK_END);
    if (ftell(f) == 0) fprintf(f, "Algorithme,Fichier,NbMots,Temps,Memoire\n");

    fprintf(f, "%s,%s,%d,%f,%zu\n", algo, fic, nb, t, m);
    printf("Perf sauvegardee.\n");
    fclose(f);
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <fichier> <algo> [taille_min]\n", argv[0]);
        return 1;
    }

    int algo = atoi(argv[2]);
    int min = 0;
    if (argc >= 4) min = atoi(argv[3]);

    InfoMem im = {0, 0, 0};
    Liste ma_liste = NULL;
    Arbre mon_arbre = NULL;
    Liste dico[26];
    for(int i=0; i<26; i++) dico[i] = NULL;

    char* m;
    FILE* f = fopen(argv[1], "r");
    if (!f) { printf("Erreur fichier\n"); return 1; }

    printf("Lancement Algo %d sur %s (min: %d)\n", algo, argv[1], min);
    clock_t start = clock();
    
    int lus = 0;
    int gardes = 0; 
    int uniques = 0; 

    while ((m = get_mot(f, &im)) != NULL) {
        if (check_mot(m)) {
            lus++;
            if (strlen(m) >= min) {
                gardes++;
                int res = 0;
                switch(algo) {
                    case 1: res = ajoutListe(&ma_liste, m, &im); break;
                    case 2: res = ajoutArbre(&mon_arbre, m, &im); break;
                    case 3: res = ajoutDico(dico, m, &im); break;
                    case 4: res = ajoutListeTriee(&ma_liste, m, &im); break;
                    default: myFree(m, &im, strlen(m)+1); break;
                }
                if (res) uniques++; 
            } else {
                myFree(m, &im, strlen(m)+1);
            }
        } else {
            myFree(m, &im, strlen(m)+1);
        }
    }

    double temps = ((double)(clock() - start)) / CLOCKS_PER_SEC;
    fclose(f);

    affichage(ma_liste, mon_arbre, dico, algo, uniques);

    printf("\nTemps: %f s | Memoire Max: %zu octets\n", temps, im.max_alloc);
    printf("Mots lus: %d | Gardes: %d | Uniques: %d\n", lus, gardes, uniques);
    
    char* noms[] = {"?", "Liste", "Arbre", "Dico", "ListeTriee"};
    char* nom = (algo >= 1 && algo <= 4) ? noms[algo] : "Inconnu";
    save_perf(nom, argv[1], gardes, temps, im.max_alloc);

    return 0;
}
