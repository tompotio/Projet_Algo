#include <stdio.h>
#include <stdlib.h>

// Structure pour représenter un nœud de la liste de voisins
struct AdjListNode {
    char parent;
    int weight;
    struct AdjListNode* next;
};

// Structure pour représenter la liste de voisins
struct AdjList {
    struct AdjListNode* head;
    int vertexWeight;
    char label;
};

// Structure pour représenter le graphe
struct Graph {
    int V;
    struct AdjList* array;
};

// Fonction pour créer un nouveau nœud de la liste de voisins
struct AdjListNode* newAdjListNode(char parent, int weight) {
    struct AdjListNode* newNode = (struct AdjListNode*) malloc(sizeof(struct AdjListNode));
    newNode->parent = parent;
    newNode->weight = weight;
    newNode->next = NULL;
    return newNode;
}

// Fonction pour créer un graphe de V sommets
struct Graph* createGraph(int V) {
    struct Graph* graph = (struct Graph*) malloc(sizeof(struct Graph));
    graph->V = V;

    // Crée un tableau de listes de voisins. La taille du tableau est V
    graph->array = (struct AdjList*) malloc(V * sizeof(struct AdjList));

    // Initialise chaque liste de voisins comme vide en mettant la tête à NULL
    for (int i = 0; i < V; ++i) {
        graph->array[i].head = NULL;
        graph->array[i].vertexWeight = 0;
        graph->array[i].label = ' ';
    }

    return graph;
}

// Fonction pour ajouter une arête dans un graphe non orienté
void addEdge(struct Graph* graph, char enfant, char parent, int weight) {
    int enfantIndex = enfant - 'a';
    int parentIndex = parent - 'a';

    // Ajoute une arête de enfant à parent. Un nouveau nœud est ajouté à la liste de voisins de enfant.
    struct AdjListNode* newNode = newAdjListNode(parent, weight);
    newNode->next = graph->array[enfantIndex].head;
    graph->array[enfantIndex].head = newNode;
}

// Fonction pour définir le poids et le libellé d'un sommet
void setVertex(struct Graph* graph, char label, int weight) {
    int index = label - 'a';
    graph->array[index].label = label;
    graph->array[index].vertexWeight = weight;
}

// Fonction pour afficher l'arbre
void printTreeUtil(struct Graph* graph, char vertex, int level) {
    int index = vertex - 'a';

    for (int i = 0; i < level; i++) {
        printf("  ");
    }

    printf("%c (%d)\n", vertex, graph->array[index].vertexWeight);

    for (int i = 0; i < graph->V; i++) {
        struct AdjListNode* current = graph->array[i].head;
        while (current != NULL) {
            if (current->parent == vertex) {
                for (int j = 0; j < level + 1; j++) {
                    printf("  ");
                }
                printf("|-- %c (%d)\n", graph->array[i].label, current->weight);
                printTreeUtil(graph, graph->array[i].label, level + 2);
            }
            current = current->next;
        }
    }
}

void printTree(struct Graph* graph) {
    char root = ' ';
    int* hasParent = calloc(graph->V, sizeof(int));
    
    for (int i = 0; i < graph->V; i++) {
        struct AdjListNode* current = graph->array[i].head;
        while (current != NULL) {
            hasParent[current->parent - 'a'] = 1;
            current = current->next;
        }
    }
    
    for (int i = 0; i < graph->V; i++) {
        if (!hasParent[i] && graph->array[i].label != ' ') {
            root = 'a' + i;
            break;
        }
    }
    
    if (root != ' ') {
        printTreeUtil(graph, root, 0);
    }
    
    free(hasParent);
}

int main() {
    int V = 8;
    struct Graph* graph = createGraph(V);

    // Définit les sommets et leurs poids
    setVertex(graph, 'a', 4);
    setVertex(graph, 'b', 3);
    setVertex(graph, 'c', 1);
    setVertex(graph, 'd', 2);
    setVertex(graph, 'e', 2);
    setVertex(graph, 'f', 8);
    setVertex(graph, 'g', 2);
    setVertex(graph, 'h', 1);

    // Ajoute les arêtes avec leurs poids
    addEdge(graph, 'a', 'b', 4);
    addEdge(graph, 'b', 'e', 1);
    addEdge(graph, 'c', 'd', 2);
    addEdge(graph, 'd', 'e', 2);
    addEdge(graph, 'e', 'h', 2);
    addEdge(graph, 'g', 'h', 5);
    addEdge(graph, 'f', 'g', 1);

    // Affiche le graphe
    printTree(graph);

    return 0;
}