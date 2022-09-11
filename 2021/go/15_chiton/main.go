package main

import (
	"container/heap"
	"fmt"
	"os"

	"aoc2021/utils"
)

type Point struct {
	x, y int
}

// Priority Queue Implementation from https://pkg.go.dev/container/heap#example__priorityQueue
// An Item is something we manage in a priority queue.
type Item struct {
	value    Point  // The value of the item; arbitrary.
	priority uint32 // The priority of the item in the queue.
	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].priority > pq[j].priority
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
func (pq *PriorityQueue) Update(item *Item, value Point, priority uint32) {
	item.value = value
	item.priority = priority
	heap.Fix(pq, item.index)
}

// ---------------------------------------------------------------

func FindShortestPathCost(weights *utils.MatrixU8) (int, error) {
	// initialize cost matrix
	start := Point{
		x: 0,
		y: 0,
	}
	end := Point{
		x: weights.NCols,
		y: weights.NRows,
	}
	print(start.x)
	print(end.x)
	costs := utils.CreateMatrixU32(weights.NRows, weights.NCols)
	costs.SetAllElementsTo(4294967295)
	costs.E[0][0] = 0
	visited := utils.CreateMatrixBool(weights.NRows, weights.NCols)
	print(visited.NCols)
	pq := make(PriorityQueue, 0)
	heap.Push(&pq, &Item{
		value:    start,
		priority: costs.E[start.y][start.x],
	})
	// for len(pq) > 0 {
	// 	item := heap.Pop(&pq).(*Item)
	// 	cost := int(costs.E[item.value.y][item.value.x])
	// 	if item.value.x == end.x && item.value.y == end.y {
	// 		return cost, nil
	// 	}
	// 	visited.E[item.value.y][item.value.x] = true

	// }
	return 0, nil
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
	cost, _ := FindShortestPathCost(weights)
	print(cost)
	print(weights.E)
	fmt.Printf("%v", weights.E)
}
