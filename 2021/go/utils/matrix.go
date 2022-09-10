package utils

import (
	"errors"
	"fmt"
	"strconv"
	"strings"
)

func StringToUInt8Matrix(input string) ([][]uint8, error) {
	rows := strings.Split(strings.TrimSuffix(input, "\n"), "\n")
	nRows := len(rows)
	nCols := len(strings.Split(strings.TrimSuffix(input, "\n"), "\n")[0])
	print(len(rows))
	print("\n \n")
	print(nRows)
	print(nCols)
	matrix := make([][]uint8, nRows)
	for i := range matrix {
		matrix[i] = make([]uint8, nCols)
	}
	for rowI, row := range rows {
		for colI, lit := range row {
			number, err := strconv.Atoi(string(lit))
			if err != nil {
				return nil, errors.New("character %v is not a valid literal")
			}
			matrix[rowI][colI] = uint8(number)
		}
	}
	fmt.Printf("%v\n", matrix)
	return matrix, nil
}
