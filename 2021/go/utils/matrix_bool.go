package utils

type MatrixBool struct {
	E     [][]bool
	NRows int
	NCols int
}

func (m *MatrixBool) SetAllElementsTo(value bool) {
	for rowI, row := range m.E {
		for colI := range row {
			m.E[rowI][colI] = value
		}
	}
}

// is there a effective difference when leaving away * and &?
func CreateMatrixBool(nRows int, nCols int) *MatrixBool {
	data := make([][]bool, nRows)
	for i := range data {
		data[i] = make([]bool, nCols)
	}
	matrix := &MatrixBool{
		E:     data,
		NRows: nRows,
		NCols: nCols,
	}
	return matrix
}
