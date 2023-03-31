import unittest
from src.cellular_automata import CellularAutomata


class TestCellularAutomata(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_inialisation_of_cellular_automata(self) -> None:
        ca = CellularAutomata((10, 10), None, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        self.assertEqual(ca.grid_size, (10, 10))
        self.assertEqual(ca.rule, None)
        self.assertEqual(ca.seed, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        self.assertListEqual(
            ca.grid,
            [
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                [1, 0, 0, 1, 1, 1, 0, 1, 0, 0],
                [1, 1, 0, 0, 0, 1, 1, 0, 1, 1],
                [0, 1, 1, 1, 1, 1, 0, 1, 0, 0],
                [1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
                [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
                [1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 0, 0, 1, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
            ],
        )

    def test_create_grid(self) -> None:
        ca = CellularAutomata((10, 10), None, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        self.assertListEqual(
            ca.create_grid(),
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
        )


if __name__ == "__main__":
    unittest.main()
