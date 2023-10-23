from parameters import Dino
from game import DinoGame, redis_client
import unittest


class TestDino(unittest.TestCase):
    def setUp(self):
        self.dino = DinoGame()

    def test_scores(self):
        self.assertEqual(self.dino.max_score, int(float(redis_client.get('max_score'))))


if __name__ == '__main__':
    unittest.main()

