import unittest
from cellular_automata import CellularAutomata

class TestCellularAutomata(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_inialisation_of_cellular_automata(self):
        ca = CellularAutomata((10, 10), 10, None, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        self.assertEqual(ca.grid_size, (10, 10))
        self.assertEqual(ca.cell_size, 10)
        self.assertEqual(ca.rule, None)
        self.assertEqual(ca.seed, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        self.assertEqual(ca.grid, [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    
    def test_create_grid(self):
        ca = CellularAutomata((10, 10), 10, None, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        self.assertEqual(ca.create_grid(), [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])



if __name__ == '__main__':
    unittest.main()