package utils

import (
	"strconv"
	"strings"
)

func StringToIntSlice(input string) ([]int, error) {
	var slice []int
	for _, line := range strings.Split(strings.TrimSuffix(input, "\n"), "\n") {
		i, err := strconv.Atoi(line)
		if err != nil {
			return nil, err
		}
		slice = append(slice, i)
	}
	return slice, nil
}
