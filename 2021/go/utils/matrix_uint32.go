package utils

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
