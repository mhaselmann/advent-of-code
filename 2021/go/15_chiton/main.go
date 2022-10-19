package main

import (
	"container/heap"
	"fmt"
	"os"
	"time"

	"aoc2021/utils"
)

type Node struct {
	x, y int
}

// Priority Queue Implementation ///////////////////////////////////////////////
// adapted from https://pkg.go.dev/container/heap#example__priorityQueue
// An Item is something we manage in a priority queue.
type Item struct {
	node  Node // payload
	cost  int  // The cost of the item in the queue
	index int  // The index of the item in the heap.
}

// A PriorityQueue implements heap.Interface and holds Items
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// priority queue should return element with the lowest cost
	return pq[i].cost < pq[j].cost
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x any) {
	n := len(*pq)
	item := x.(*Item)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() any {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // avoid memory leak
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

// End of Priority Queue Implementation ////////////////////////////////////////

// create enlarged matrix for part 2 (see puzzle description)
func createMatrixMxN(matrix *utils.MatrixU8, m int, n int) *utils.MatrixU8 {
	finalNRows := matrix.NRows * m
	finalNCols := matrix.NCols * n
	matrixMxN := utils.CreateMatrixU8(finalNRows, finalNCols)
	for rowI, row := range matrixMxN.E {
		for colI := range row {
			mI := rowI / matrix.NRows
			rootRowI := rowI % matrix.NRows
			nI := colI / matrix.NCols
			rootColI := colI % matrix.NCols
			value := matrix.E[rootRowI][rootColI]
			for i := 0; i < mI+nI; i++ {
				value += 1
				if value > 9 {
					value = 1
				}
			}
			matrixMxN.E[rowI][colI] = value
		}
	}
	return matrixMxN
}

// get a slice of all neighbors of the node that have not been visited yet according to visited matrix
func getUnvisitedNeighbors(node Node, visited utils.MatrixBool) []Node {
	nodes := []Node{}
	if node.y > 0 && !visited.E[node.y-1][node.x] {
		nodes = append(nodes, Node{x: node.x, y: node.y - 1})
	}
	if node.x > 0 && !visited.E[node.y][node.x-1] {
		nodes = append(nodes, Node{x: node.x - 1, y: node.y})
	}
	if node.y < visited.NRows-1 && !visited.E[node.y+1][node.x] {
		nodes = append(nodes, Node{x: node.x, y: node.y + 1})
	}
	if node.x < visited.NCols-1 && !visited.E[node.y][node.x+1] {
		nodes = append(nodes, Node{x: node.x + 1, y: node.y})
	}
	return nodes
}

// an implementation of the Dijkstra's algorithm optimized for the problem (Speed O(n));
// O(n) because number of neighbors at most 4 according the the grid structure of the nodes
func FindShortestPathCost(weights *utils.MatrixU8) int {
	start := Node{
		x: 0,
		y: 0,
	}
	end := Node{
		x: weights.NCols - 1,
		y: weights.NRows - 1,
	}
	costs := utils.CreateMatrixInt(weights.NRows, weights.NCols)
	costs.SetAllElementsToMax()
	costs.E[0][0] = 0
	visited := utils.CreateMatrixBool(weights.NRows, weights.NCols)
	pq := make(PriorityQueue, 0)
	heap.Push(&pq, &Item{
		node: start,
		cost: costs.E[start.y][start.x],
	})
	for len(pq) > 0 {
		item := heap.Pop(&pq).(*Item)
		node := item.node
		cost := costs.E[node.y][node.x]
		if node.x == end.x && node.y == end.y {
			return cost
		}
		visited.E[node.y][node.x] = true
		for _, nb := range getUnvisitedNeighbors(node, *visited) {
			newNeighborCost := cost + int(weights.E[nb.y][nb.x])
			if newNeighborCost < costs.E[nb.y][nb.x] {
				costs.E[nb.y][nb.x] = newNeighborCost
				heap.Push(&pq, &Item{node: nb, cost: costs.E[nb.y][nb.x]})
			}
		}
	}
	return -1
}

func main() {
	input, err := os.ReadFile("input.txt")
	if err != nil {
		os.Exit(1)
	}
	weights, err := utils.StringToMatrixU8(string(input))
	if err != nil {
		os.Exit(2)
	}
	startTime := time.Now()
	costPart1 := FindShortestPathCost(weights)
	elapsedTime := time.Since(startTime)
	fmt.Printf("Answer part 1: Shortest path's cost: %v after %v\n", costPart1, elapsedTime)

	weights5x5 := createMatrixMxN(weights, 5, 5)
	startTime = time.Now()
	costPart2 := FindShortestPathCost(weights5x5)
	elapsedTime = time.Since(startTime)
	fmt.Printf("Answer part 2: Shortest path's cost: %v after %v\n", costPart2, elapsedTime)
}
