package utils

// https://stackoverflow.com/questions/6878590/the-maximum-value-for-an-int-type-in-go
const MaxUint = ^uint(0)
const MinUint = 0
const MaxInt = int(MaxUint >> 1)
const MinInt = -MaxInt - 1

////////////////////////////////////////////////////////////////////////////////

type MatrixInt struct {
	E     [][]int
	NRows int
	NCols int
}

func (m *MatrixInt) SetAllElementsTo(value int) {
	for rowI, row := range m.E {
		for colI := range row {
			m.E[rowI][colI] = value
		}
	}
}

func (m *MatrixInt) SetAllElementsToMin() { m.SetAllElementsTo(MinInt) }

func (m *MatrixInt) SetAllElementsToMax() { m.SetAllElementsTo(MaxInt) }

// is there a effective difference when leaving away * and &?
func CreateMatrixInt(nRows int, nCols int) *MatrixInt {
	data := make([][]int, nRows)
	for i := range data {
		data[i] = make([]int, nCols)
	}
	matrix := &MatrixInt{
		E:     data,
		NRows: nRows,
		NCols: nCols,
	}
	return matrix
}
