package main

import (
	"container/heap"
	"os"

	"aoc2021/utils"
)

type Node struct {
	x, y int
}

// Priority Queue Implementation adapted from https://pkg.go.dev/container/heap#example__priorityQueue
// An Item is something we manage in a priority queue.
type Item struct {
	node Node   // The value of the item; arbitrary.
	cost uint32 // The priority of the item in the queue.
	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

// A PriorityQueue implements heap.Interface and holds Items.
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

// update modifies the priority and value of an Item in the queue.
func (pq *PriorityQueue) Update(item *Item, node Node, cost uint32) {
	item.node = node
	item.cost = cost
	heap.Fix(pq, item.index)
}

// ---------------------------------------------------------------

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

func FindShortestPathCost(weights *utils.MatrixU8) int {
	// initialize cost matrix
	start := Node{
		x: 0,
		y: 0,
	}
	end := Node{
		x: weights.NCols - 1,
		y: weights.NRows - 1,
	}
	costs := utils.CreateMatrixU32(weights.NRows, weights.NCols)
	costs.SetAllElementsTo(4294967295)
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
		cost := int(costs.E[node.y][node.x])
		if node.x == end.x && node.y == end.y {
			return cost
		}
		visited.E[node.y][node.x] = true
		for _, nb := range getUnvisitedNeighbors(node, *visited) {
			newNeighborCost := cost + int(weights.E[nb.y][nb.x])
			if newNeighborCost < int(costs.E[nb.y][nb.x]) {
				costs.E[nb.y][nb.x] = uint32(newNeighborCost)
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
	cost := FindShortestPathCost(weights)
	print(cost)
}
