import pygame
import random
import redis
from parameters import Sounds, Dino, Comet, GameObject
from decouple import config
from game_logic import GameLogic


redis_client = redis.Redis(
    host=config('HOST'),
    port=config('PORT'),
    password=config('PASSWORD')
)

COMET_SPAWN_TIMER = pygame.USEREVENT + 1
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 360
FONT_L = 'fonts/roboto.ttf'
pygame.display.set_caption('DinoGame')
pygame.display.set_icon(pygame.image.load('images/comet.png'))


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
        self.running = False
        self.score = 0
        self.font = pygame.font.Font('fonts/roboto.ttf', 25)
        self.max_score = int((round(float(redis_client.get('max_score')), 0)))
        self.gameplay = False
        self.game_over = False
        self.sounds = Sounds()
        self.game_renderer = GameRenderer(self.screen, self)
        self.game_logic = GameLogic(self)
        self.achievement_sound = pygame.mixer.Sound('sounds/8-bit-achievement-epic-stock-media-1-00-00.mp3')

    @staticmethod
    def get_random_time():
        return random.randint(800, 3000)

    def run(self):
        val = 50
        self.running = True
        while self.running:
            if not self.game_over:
                if not self.gameplay:
                    self.show_start_screen()
                    self.handle_start_events()
                else:
                    self.score += 0.15

                    if int(self.score) == val:
                        self.achievement_sound.play()
                        val += 50
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
            elif event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE:
                raise ValueError('Incorrect keyword!')

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

    def stop_game(self):
        self.running = False
        pygame.quit()


if __name__ == "__main__":
    game = DinoGame()
    game.run()
    pygame.quit()
