#include <stdio.h>

void afficheTab(int tab[], int taille) {
    for (int i = 0; i < taille; i++) {
        printf("%d\n",*(tab+i));
    }
}

void changeTab(int tab[], int taille, int indice) { 
    if (indice >= 0 && indice < taille) {
     *(tab+indice) +=2;
    }
}

int main() {
    int tab[5]= {1,2,3,4,5};
    printf("%p\n",&tab[0]);
    printf("%p\n",&tab[1]);
    printf("%p\n",&tab[2]);
    printf("Avant modification :\n");
    afficheTab(tab,5);
    changeTab(tab,5,2);
    printf("Après modification :\n");
    afficheTab(tab,5);
    return 0;
}
