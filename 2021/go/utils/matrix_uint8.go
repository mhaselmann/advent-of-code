package utils

import (
	"errors"
	"strconv"
	"strings"
)

type MatrixU8 struct {
	E     [][]uint8
	NRows int
	NCols int
}

func (m *MatrixU8) SetAllElementsTo(value uint8) {
	for rowI, row := range m.E {
		for colI := range row {
			m.E[rowI][colI] = value
		}
	}
}

// is there a effective difference when leaving away * and &?
func CreateMatrixU8(nRows int, nCols int) *MatrixU8 {
	data := make([][]uint8, nRows)
	for i := range data {
		data[i] = make([]uint8, nCols)
	}
	matrix := &MatrixU8{
		E:     data,
		NRows: nRows,
		NCols: nCols,
	}
	return matrix
}

func StringToMatrixU8(input string) (*MatrixU8, error) {
	rows := strings.Split(strings.TrimSuffix(input, "\n"), "\n")
	nRows := len(rows)
	nCols := len(strings.Split(strings.TrimSuffix(input, "\n"), "\n")[0])
	matrix := CreateMatrixU8(nRows, nCols)
	for rowI, row := range rows {
		for colI, lit := range row {
			number, err := strconv.Atoi(string(lit))
			if err != nil {
				return nil, errors.New("character %v is not a valid literal")
			}
			matrix.E[rowI][colI] = uint8(number)
		}
	}
	return matrix, nil
}
