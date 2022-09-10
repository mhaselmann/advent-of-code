package utils

import (
	"errors"
	"strconv"
	"strings"
)

func StringToUInt8Matrix(input string) ([][]uint8, error) {
	rows := strings.Split(strings.TrimSuffix(input, "\n"), "\n")
	nRows := len(rows)
	nCols := len(strings.Split(strings.TrimSuffix(input, "\n"), "\n")[0])
	matrix, _ := MatrixUint8(nRows, nCols)
	for rowI, row := range rows {
		for colI, lit := range row {
			number, err := strconv.Atoi(string(lit))
			if err != nil {
				return nil, errors.New("character %v is not a valid literal")
			}
			matrix[rowI][colI] = uint8(number)
		}
	}
	return matrix, nil
}

func MatrixUint8(nRows int, nCols int) ([][]uint8, error) {
	if nRows < 1 || nCols < 1 {
		return nil, errors.New("nRows and nCols must be at least 1")
	}
	matrix := make([][]uint8, nRows)
	for i := range matrix {
		matrix[i] = make([]uint8, nCols)
	}
	return matrix, nil
}

type MatrixU32 struct {
	E     [][]uint32
	NRows int
	NCols int
}

func (m *MatrixU32) SetAllElementsTo(value uint32) {
	for rowI, row := range m.E {
		for colI := range row {
			m.E[rowI][colI] = value
		}
	}
}

// is there a effective difference when leaving away * and &?
func CreateMatrixU32(nRows int, nCols int) *MatrixU32 {
	data := make([][]uint32, nRows)
	for i := range data {
		data[i] = make([]uint32, nCols)
	}
	matrix := &MatrixU32{
		E:     data,
		NRows: nRows,
		NCols: nCols,
	}
	return matrix
}
