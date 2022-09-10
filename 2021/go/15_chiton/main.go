package main

import (
	"fmt"
	"os"

	"aoc2021/utils"
)

type point struct {
	x, y int
}

func FindShortestPathCost(weights *utils.MatrixU8) (bool, error) {
	// initialize cost matrix
	costs := utils.CreateMatrixU32(weights.NRows, weights.NCols)
	costs.SetAllElementsTo(4294967295)
	costs.E[0][0] = 0
	visited := utils.CreateMatrixBool(weights.NRows, weights.NCols)
	return visited.E[0][0], nil
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
