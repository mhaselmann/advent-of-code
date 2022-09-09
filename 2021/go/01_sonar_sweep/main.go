package main

import (
	"errors"
	"fmt"
	"os"

	"aoc2021/utils"
)

func slidingWindowSum(input []int, window_size int) ([]int, error) {
	if len(input)-window_size < 0 {
		return nil, errors.New("size of sliding window exceeds length of input slice")
	}
	sum := make([]int, len(input)-2)
	for i := range sum {
		for j := i; j < i+window_size; j++ {
			sum[i] += input[j]
		}
	}
	return sum, nil
}

func numberOfRisingElements(input []int) int {
	var counter int
	for i := range input {
		if i == 0 {
			continue
		}
		if input[i] > input[i-1] {
			counter += 1
		}
	}
	return counter
}

func main() {
	input, err := os.ReadFile("input.txt")
	if err != nil {
		os.Exit(1)
	}
	intSlice, _ := utils.StringToIntSlice(string(input))
	answerPart1 := numberOfRisingElements(intSlice)
	fmt.Printf("Answer part 1: %v\n", answerPart1)
	intSliceAvg, _ := slidingWindowSum(intSlice, 3)
	answerPart2 := numberOfRisingElements(intSliceAvg)
	fmt.Printf("Answer part 2: %v\n", answerPart2)
}
