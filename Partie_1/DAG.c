#include <stdio.h>
#include <stdlib.h>

struct AdjListNode {
    char parent;
    int weight;
    struct AdjListNode* next;
};

struct AdjList {
    struct AdjListNode* head;
    int vertexWeight;
    char label;
};

struct Graph {
    int V;
    struct AdjList* array;
};

struct AdjListNode* newAdjListNode(char parent, int weight) {
    struct AdjListNode* newNode = (struct AdjListNode*) malloc(sizeof(struct AdjListNode));
    newNode->parent = parent;
    newNode->weight = weight;
    newNode->next = NULL;
    return newNode;
}

struct Graph* createGraph(int V) {
    struct Graph* graph = (struct Graph*) malloc(sizeof(struct Graph));
    graph->V = V;
    graph->array = (struct AdjList*) malloc(V * sizeof(struct AdjList));

    for (int i = 0; i < V; ++i) {
        graph->array[i].head = NULL;
        graph->array[i].vertexWeight = 0;
        graph->array[i].label = ' ';
    }

    return graph;
}

void addEdge(struct Graph* graph, char enfant, char parent, int weight) {
    int enfantIndex = enfant - 'a';
    int parentIndex = parent - 'a';

    struct AdjListNode* newNode = newAdjListNode(parent, weight);
    newNode->next = graph->array[enfantIndex].head;
    graph->array[enfantIndex].head = newNode;
}

void setVertex(struct Graph* graph, char label, int weight) {
    int index = label - 'a';
    graph->array[index].label = label;
    graph->array[index].vertexWeight = weight;
}

int main() {
    int V = 9;
    struct Graph* graph = createGraph(V);

    setVertex(graph, 'a', 4);
    setVertex(graph, 'b', 3);
    setVertex(graph, 'c', 1);
    setVertex(graph, 'd', 2);
    setVertex(graph, 'e', 2);
    setVertex(graph, 'f', 8);
    setVertex(graph, 'g', 2);
    setVertex(graph, 'h', 1);

    addEdge(graph, 'a', 'b', 4);
    addEdge(graph, 'b', 'e', 1);
    addEdge(graph, 'e', 'h', 2);
    addEdge(graph, 'f', 'g', 1);
    addEdge(graph, 'g', 'h', 5);
    addEdge(graph, 'c', 'd', 2);
    addEdge(graph, 'd', 'e', 2);

    printTree(graph);

    return 0;
}