#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void aleatoire(){
    for (int i=1;i<=20;i++){
        srand(time(NULL));
        printf("%d, %d\n",i,rand());
    }
}

void initAlea(int tab[], int taille, int max) {
    for (int i = 0; i < taille; i++) {
        srand(time(NULL)+i);
        *(tab+i) = rand() % max;
    }
}


int main() {
    int tab[10] = {2,5,8,12,25,32,45,78,96,102};
    initAlea(tab, 10, 100);
    for (int i = 0; i < 10; i++) {
        printf("%d \n", tab[i]);
    }
    return 0;
}
