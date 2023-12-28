#include <stdio.h>
#include <stdlib.h>
#include "Topology_sort.h"

#define MAX 100

//Global variables
int vertexCount;
int adjacencyArr[MAX][MAX];
int verticesDegree[MAX];
int queue[MAX];
int topologicalOrder[MAX];
int edgeStart = -1, edgeStop = -1;
int count = 0;
int tmp;

int main() {
    
    printf("===========================\nTopological sorting program\n===========================\n\n");
    printf("Enter count of vertices:\n");
    scanf("%d", &vertexCount);

    //Creates graph of adjacency
    CreateGraph();
    
    //Print graph of adjacency
    PrintGraph();

    //Check degree of every vertex
    VerticesDegree();

    while(!IsEmpty() && count < vertexCount) {
        tmp = DeleteArr();
        topologicalOrder[++count] = tmp;
        for(int i = 0; i < vertexCount; i++) {
            if(adjacencyArr[tmp][i] == 1) {
                adjacencyArr[tmp][i] = 0;
                verticesDegree[i]--;
                if(verticesDegree[i] == 0) {
                    Insert(i);
                }
            }
        }
    }

    //Check if the graph has circle
    CheckCycle();

    //Print topological sorted list
    PrintSorted();

    return 0;
}

void CreateGraph() {
    int edgesCount = 0;
    printf("\nNow you will start entering edges\nMake sure that your inputs are in range [0 ; vertices count - 1]\nRemember that vertices stars from 0\nEnter -1 value to stop entering\n\n");
    while(edgesCount < (vertexCount*(vertexCount-1))) {
        printf("Enter (start) --and--> (end) of the edge:\n");
        scanf("%d %d", &edgeStart, &edgeStop);
        if((edgeStart == -1) || (edgeStop == -1)) {
            break;
        }
        else if((edgeStart >= vertexCount) || (edgeStop >= vertexCount) || (edgeStart < 0) || (edgeStop < 0)) {
            printf("Invalide input\n");
            continue;
        }
        else {
            adjacencyArr[edgeStart][edgeStop] = 1;
        }
        edgesCount++;
    }
}

void PrintGraph() {
    printf("\nYour graph of adjacency:\n");
    for (int i = 0; i < vertexCount; i++) {
        for (int j = 0; j < vertexCount; j++) {
            printf("%d ", adjacencyArr[i][j]);
        }
        printf("\n");
    }
}

void VerticesDegree() {
    for (int i = 0; i < vertexCount; i++) {
        verticesDegree[i] = Degree(i);
        if(verticesDegree[i] == 0) {
            Insert(i);
        }
    }
}

int Degree(int var) {
    int degree = 0;
    for(int i = 0; i < vertexCount; i++) {
        if(adjacencyArr[i][var] == 1) {
            degree++;
        }
    }
    return degree;
}

void Insert(int ver) {
    if(edgeStart == MAX - 1) {
        printf("Overflow error\n");
    }
    else {
        if(edgeStop == -1) {
            edgeStop = 0;
        }
        edgeStart++;
        queue[edgeStart] = ver;
    }
}

int IsEmpty() {
    if((edgeStop == -1) || (edgeStop > edgeStart)) {
        return 1;
    }
    else {
        return 0;
    }
}

int DeleteArr() {
    int tmp2;
    if((edgeStop == -1) || (edgeStop > edgeStart)) {
        printf("Underflow error\n");
        exit(1);
    }
    else {
        tmp2 = queue[edgeStop];
        edgeStop++;
        return tmp2;
    }
}

void CheckCycle() {
    if (count < vertexCount) {
        printf("Cannot find topological order because graph contains cycle\n");
        exit(1);
    }
}

void PrintSorted() {
    printf("\nVertices in topological order:\n");
    for (int i = 1; i <=count; i++) {
        printf("%d", topologicalOrder[i]);
        if (i != count) {
            printf("-->");
        }
    }
    printf("\n");
}