import pygame
import unittest
from game import DinoGame
import pydirectinput as pdi
from game import redis_client
import time


class Set_Up(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.mixer.init()
    
    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.dino_game = DinoGame()
        self.dino_game.run()


class TestDinoGameAfterStart(Set_Up, unittest.TestCase):
    def test_gameplay(self):
        self.dino_game.stop_game()
        self.assertTrue(self.dino_game.gameplay)
        
    def test_comet_list(self):
        self.assertTrue(self.dino_game.comet_list)
    
    def test_values(self):
        self.assertFalse(self.dino_game.game_over)
        self.assertIsNotNone(self.dino_game.comet_list)
    
   

class TestDinoGameBeforeStart(Set_Up, unittest.TestCase):
    def setUp(self):
        self.dino_game = DinoGame()

    def test_gameplay(self):
        self.assertFalse(self.dino_game.gameplay)
    
    def test_init_score(self):
        self.assertEqual(self.dino_game.score, 0)

    def test_max_score(self):
        self.assertEqual(int(float(redis_client.get('max_score'))), self.dino_game.max_score)

    def test_1(self):
        with self.assertRaises(ValueError):
            self.dino_game.run()

               

if __name__ == "__main__":
    unittest.main()
