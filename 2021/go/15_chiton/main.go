package main

import (
	"os"

	"aoc2021/utils"
)

type point struct {
	x, y int
}

func FindShortestPathCost(weights [][]uint8) (uint32, error) {
	// initialize cost matrix
	costs := utils.CreateMatrixU32(len(weights), len(weights[0]))
	costs.SetAllElementsTo(4294967295)
	costs.E[0][0] = 0
	return costs.E[0][1], nil
}

func main() {
	input, err := os.ReadFile("input.txt")
	if err != nil {
		os.Exit(1)
	}
	weights, err := utils.StringToUInt8Matrix(string(input))
	if err != nil {
		os.Exit(2)
	}
	cost, _ := FindShortestPathCost(weights)
	print(cost)
}
