import unittest
from src.cellular_automata import CellularAutomata


class TestCellularAutomata(unittest.TestCase):
    """
    A class used to test the CellularAutomata class.

    ...

    Methods
    -------
    setUp():
        Sets up the test environment.

    test_inialisation_of_cellular_automata():
        Tests the initialisation of the CellularAutomata class.

    test_create_grid():
        Tests the creation of a grid in the CellularAutomata class.
    """

    def setUp(self) -> None:
        return super().setUp()

    def test_inialisation_of_cellular_automata(self) -> None:
        """
        Tests the initialisation of the CellularAutomata class.

        The test checks if the grid size, rule and seed are correctly set during initialisation.
        It also checks if the grid is correctly populated based on the seed.

        Returns
        -------
        None
        """
        ca = CellularAutomata((10, 10), None, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        self.assertEqual(ca.grid_size, (10, 10))
        self.assertEqual(ca.rule, None)
        self.assertEqual(ca.seed, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        self.assertListEqual(
            ca.grid.tolist(),
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
        """
        Tests the creation of a grid in the CellularAutomata class.

        The test checks if a new grid is correctly created with all zeros.

        Returns
        -------
        None
        """
        ca = CellularAutomata((10, 10), None, None)
        self.assertListEqual(
            ca.grid.tolist(),
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
