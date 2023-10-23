# import pygame
# import random
# import redis
# from parameters import Sounds, Dino, Comet, GameObject
# redis_client = redis.Redis(
#   host='redis-17932.c1.asia-northeast1-1.gce.cloud.redislabs.com',
#   port=17932,
#   password='LnNrEZ27dbYGoDp56aGQSnwVjTcahQJR'
#   )
#
# COMET_SPAWN_TIMER = pygame.USEREVENT + 1
# SCREEN_WIDTH = 600
# SCREEN_HEIGHT = 360

#
# class DinoGame:
#     def __init__(self):
#         pygame.init()
#         pygame.mixer.init()
#         self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#         self.clock = pygame.time.Clock()
#         self.background = GameObject(0, 0, 'images/bg2.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)
#         self.background_x = 0
#         self.dino = Dino()
#         self.comet_list = []
#         self.comet_spawn_timer = COMET_SPAWN_TIMER
#         pygame.time.set_timer(self.comet_spawn_timer, self.get_random_time())
#         self.running = True
#         self.score = 0
#         self.font = pygame.font.Font('fonts/roboto.ttf', 25)
#         self.max_score = int((round(float(redis_client.get('max_score')), 0)))
#         self.gameplay = False
#         self.game_over = False
#         self.sounds = Sounds()
#
#     def get_random_time(self):
#         return random.randint(1000, 3000)
#
#     def run(self):
#         while self.running:
#             if not self.game_over:
#                 if not self.gameplay:
#                     self.show_start_screen()
#                     self.handle_start_events()
#                 else:
#                     self.score += 0.15
#                     self.handle_events()
#                     self.update()
#                     self.draw()
#                     self.clock.tick(60)
#             else:
#                 self.show_game_over_screen()
#                 self.handle_game_over_events()
#
#     def handle_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running = False
#             elif event.type == self.comet_spawn_timer:
#                 self.comet_list.append(Comet())
#                 pygame.time.set_timer(self.comet_spawn_timer, self.get_random_time())
#         keys = pygame.key.get_pressed()
#         self.dino.handle_keys(keys)
#
#     def update(self):
#         self.background_x -= 3
#         if self.background_x == -600:
#             self.background_x = 0
#         self.dino.update()
#         for comet in self.comet_list:
#             comet.update()
#             if self.dino.is_colliding(comet):
#                 if self.score > self.max_score:
#                     redis_client.set('max_score', self.score)
#                     self.max_score = int(self.score)
#                 print('Game over')
#                 self.sounds.play_encounter_sound()
#                 pygame.time.delay(600)
#                 self.game_over = True
#
#     def draw(self):
#         self.screen.blit(self.background.image, (self.background_x, 0))
#         self.screen.blit(self.background.image, (self.background_x + 600, 0))
#         self.screen.blit(self.font.render(f'Max score: {self.max_score}', True, 'White'), (30, 30))
#         self.screen.blit(self.font.render(f'Score: {int(self.score)}', True, 'White'), (440, 30))
#         self.dino.draw(self.screen)
#         for comet in self.comet_list:
#             comet.draw(self.screen)
#         pygame.display.update()
#
#     def show_start_screen(self):
#         self.screen.fill(('black'))
#         self.sounds.play_start_music()
#         font = pygame.font.Font('fonts/roboto.ttf', 15)
#         font2 = pygame.font.Font('fonts/roboto.ttf', 75)
#         text = font.render('Нажмите "SPACE", чтобы начать игру', True, 'white')
#         text2 = font2.render('DINO      GAME', True, 'green')
#         self.screen.blit(pygame.transform.scale(Dino().dino_walk[0], (120, 120)), (228, 70))
#         self.screen.blit(text, (155, 219))
#         self.screen.blit(text2, (47, 98))
#         pygame.display.flip()
#
#     def handle_start_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running = False
#             elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#                 self.sounds.stop_start_music()
#                 self.gameplay = True
#
#     def show_game_over_screen(self):
#         self.screen.fill('black')
#         self.sounds.play_game_over_music()
#         text = pygame.font.Font('fonts/roboto.ttf', 58)
#         text1 = pygame.font.Font('fonts/roboto.ttf', 21)
#         text2 = pygame.font.Font('fonts/roboto.ttf', 15)
#         self.screen.blit(text1.render(f'Max score: {self.max_score}', True, 'green'), (15, 15))
#         self.screen.blit(text1.render(f'Your score: {int(self.score)}', True, 'white'), (15, 55))
#         self.screen.blit(text.render('GAME OVER', True, 'red'), (135, 140))
#         self.screen.blit(text2.render('Press "R" to restart game', True, 'white'), (210, 210))
#         pygame.display.flip()
#
#     def handle_game_over_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running = False
#             elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
#                 self.game_over = False
#                 self.sounds.stop_game_over_music()
#                 self.reset_game()
#
#     def reset_game(self):
#         self.dino = Dino()
#         self.comet_list = []
#         self.comet_timer = pygame.USEREVENT + 1
#         pygame.time.set_timer(self.comet_timer, self.get_random_time())
#         self.score = 0
#
#
# if __name__ == "__main__":
#     game = DinoGame()
#     game.run()
#     pygame.quit()

import pygame
import random
import redis
from parameters import Sounds, Dino, Comet, GameObject

redis_client = redis.Redis(
    host='redis-17932.c1.asia-northeast1-1.gce.cloud.redislabs.com',
    port=17932,
    password='LnNrEZ27dbYGoDp56aGQSnwVjTcahQJR'
)

COMET_SPAWN_TIMER = pygame.USEREVENT + 1
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 360
FONT_L = 'fonts/roboto.ttf'


class GameRenderer:
    def __init__(self, screen, dino_game):
        self.screen = screen
        self.dino_game = dino_game

    def render(self):
        self.screen.blit(self.dino_game.background.image, (self.dino_game.background_x, 0))
        self.screen.blit(self.dino_game.background.image, (self.dino_game.background_x + 600, 0))
        self.screen.blit(self.dino_game.font.render(f'Max score: {self.dino_game.max_score}', True, 'White'), (30, 25))
        self.screen.blit(self.dino_game.font.render(f'Score: {int(self.dino_game.score)}', True, 'White'), (440, 25))
        self.dino_game.dino.draw(self.screen)
        for comet in self.dino_game.comet_list:
            comet.draw(self.screen)
        pygame.display.update()


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
                print('Game over')
                self.dino_game.sounds.play_encounter_sound()
                pygame.time.delay(600)
                self.dino_game.game_over = True


class DinoGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = GameObject(0, 0, 'images/bg2.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background_x = 0
        self.dino = Dino()
        self.comet_list = []
        self.comet_spawn_timer = COMET_SPAWN_TIMER
        pygame.time.set_timer(self.comet_spawn_timer, self.get_random_time())
        self.running = True
        self.score = 0
        self.font = pygame.font.Font('fonts/roboto.ttf', 25)
        self.max_score = int((round(float(redis_client.get('max_score')), 0)))
        self.gameplay = False
        self.game_over = False
        self.sounds = Sounds()
        self.game_renderer = GameRenderer(self.screen, self)
        self.game_logic = GameLogic(self)

    def get_random_time(self):
        return random.randint(800, 3000)

    def run(self):
        while self.running:
            if not self.game_over:
                if not self.gameplay:
                    self.show_start_screen()
                    self.handle_start_events()
                else:
                    self.score += 0.15
                    self.game_logic.handle_events()
                    self.game_logic.update()
                    self.game_renderer.render()
                    self.clock.tick(60)
            else:
                self.show_game_over_screen()
                self.handle_game_over_events()

    def handle_start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.sounds.stop_start_music()
                self.gameplay = True

    def show_start_screen(self):
        self.screen.fill('black')
        self.sounds.play_start_music()
        font = pygame.font.Font(FONT_L, 15)
        font2 = pygame.font.Font(FONT_L, 75)
        text = font.render('Нажмите "SPACE", чтобы начать игру', True, 'white')
        text2 = font2.render('DINO      GAME', True, 'green')
        self.screen.blit(pygame.transform.scale(Dino().dino_walk[0], (120, 120)), (228, 70))
        self.screen.blit(text, (155, 219))
        self.screen.blit(text2, (47, 98))
        pygame.display.flip()

    def show_game_over_screen(self):
        self.screen.fill('black')
        self.sounds.play_game_over_music()
        texts = {
            'title': pygame.font.Font(FONT_L, 58),
            'score': pygame.font.Font(FONT_L, 21),
            'restart': pygame.font.Font(FONT_L, 15)
        }

        self.screen.blit(texts['score'].render(f'Max score: {self.max_score}', True, 'green'), (15, 15))
        self.screen.blit(texts['score'].render(f'Your score: {int(self.score)}', True, 'white'), (15, 55))
        self.screen.blit(texts['title'].render('GAME OVER', True, 'red'), (135, 140))
        self.screen.blit(texts['restart'].render('Press "R" to restart game', True, 'white'), (210, 210))
        pygame.display.flip()

    def handle_game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.game_over = False
                self.sounds.stop_game_over_music()
                self.reset_game()

    def reset_game(self):
        self.dino = Dino()
        self.comet_list = []
        self.comet_spawn_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.comet_spawn_timer, self.get_random_time())
        self.score = 0


if __name__ == "__main__":
    game = DinoGame()
    game.run()
    pygame.quit()
