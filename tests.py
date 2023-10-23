from parameters import Dino
from game import DinoGame
import unittest


class TestDino(unittest.TestCase):
    def setUp(self):
        self.dino = DinoGame()

    def test_scores(self):
        self.assertEqual(self.dino.max_score, 103)


if __name__ == '__main__':
    unittest.main()

