import pygame
from parameters import Comet, Dino
import redis
from decouple import config

redis_client = redis.Redis(
    host=config('HOST'),
    port=config('PORT'),
    password=config('PASSWORD')
)


class GameLogic:
    def __init__(self, dino_game):
        self.dino_game = dino_game

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.dino_game.running = False
            elif event.type == self.dino_game.comet_spawn_timer:
                self.dino_game.comet_list.append(Comet())
                pygame.time.set_timer(self.dino_game.comet_spawn_timer, self.dino_game.get_random_time())
        keys = pygame.key.get_pressed()
        self.dino_game.dino.handle_keys(keys)

    def update(self):
        self.dino_game.background_x -= 3
        if self.dino_game.background_x == -600:
            self.dino_game.background_x = 0
        self.dino_game.dino.update()
        for comet in self.dino_game.comet_list:
            comet.update()
            if self.dino_game.dino.is_colliding(comet):
                if self.dino_game.score > self.dino_game.max_score:
                    redis_client.set('max_score', self.dino_game.score)
                    self.dino_game.max_score = int(self.dino_game.score)
                print({'game_state': self.dino_game.gameplay, 'gameplay': self.dino_game.game_over,
                       'max_score': self.dino_game.max_score,
                       'score_overall': int(self.dino_game.score),
                       'dino_cls': self.dino_game, 'comet_list': self.dino_game.comet_list})
                self.dino_game.sounds.play_encounter_sound()
                pygame.time.delay(600)
                self.dino_game.game_over = True
