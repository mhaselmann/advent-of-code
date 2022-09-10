package main

import (
	"os"

	"aoc2021/utils"
)

func main() {
	input, err := os.ReadFile("input.txt")
	if err != nil {
		os.Exit(1)
	}
	intSlice, _ := utils.StringToUInt8Matrix(string(input))
	print(intSlice)
}
