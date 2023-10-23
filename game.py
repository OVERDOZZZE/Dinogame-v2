import pygame
import random
import redis
redis_client = redis.Redis(
  host='redis-17932.c1.asia-northeast1-1.gce.cloud.redislabs.com',
  port=17932,
  password='LnNrEZ27dbYGoDp56aGQSnwVjTcahQJR'
  )


class GameObject:
    def __init__(self, x, y, image_path, width, height):
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (width, height))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Dino(GameObject):
    def __init__(self):
        super().__init__(50, 210, 'images/dino_right/dino1.png', 52, 52)
        self.__dino_walk = [
            pygame.transform.scale(pygame.image.load('images/dino_right/dino1.png').convert_alpha(), (52, 52)),
            pygame.transform.scale(pygame.image.load('images/dino_right/dino2.png').convert_alpha(), (52, 52)),
            pygame.transform.scale(pygame.image.load('images/dino_right/dino3.png').convert_alpha(), (52, 52)),
        ]
        self.__ani_dino = 0
        self.__is_jump = False
        self.__jump_count = 7
        self.__ani_speed = 10

    # def get_ani_dino(self):
    #     return self.__ani_dino

    # def set_ani_dino(self, value):
    #     self.__ani_dino = value

    def handle_keys(self, keys):
        if not self.__is_jump:
            if keys[pygame.K_SPACE]:
                self.__is_jump = True

    def update(self):
        if self.__is_jump:
            if self.__jump_count >= -7:
                if self.__jump_count > 0:
                    self.y -= (self.__jump_count ** 2) / 2.3
                else:
                    self.y += (self.__jump_count ** 2) / 2.3
                self.__jump_count -= 0.5
            else:
                self.__is_jump = False
                self.__jump_count = 7

        if self.__ani_dino == 2 * self.__ani_speed:
            self.__ani_dino = 0
        else:
            self.__ani_dino += 1
        self.rect.topleft = (self.x, self.y)
        self.image = self.__dino_walk[self.__ani_dino // self.__ani_speed]

    def is_colliding(self, comet):
        return self.rect.colliderect(comet.rect)


class Comet(GameObject):
    def __init__(self):
        super().__init__(610, 225, 'images/comet.png', 32, 32)
        self.speed = 4

    def update(self):
        self.x -= self.speed
        self.rect.topleft = (self.x, self.y)


class DinoGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 360))
        self.clock = pygame.time.Clock()
        self.background = GameObject(0, 0, 'images/bg2.jpg', 600, 360)
        self.background_x = 0
        self.dino = Dino()
        self.comet_list = []
        self.comet_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.comet_timer, self.get_random_time())
        self.running = True
        self.score = 0
        self.font = pygame.font.Font('fonts/roboto.ttf', 25)
        self.max_score = int((round(float(redis_client.get('max_score')), 0)))
        self.gameplay = False
        self.game_over = False

    def get_random_time(self):
        return random.randint(1000, 3000)

    def run(self):
        while self.running:
            if not self.game_over:
                if not self.gameplay:
                    self.show_start_screen()
                    self.handle_start_events()
                else:
                    self.score += 0.15
                    self.handle_events()
                    self.update()
                    self.draw()
                    self.clock.tick(60)
            else:
                self.show_game_over_screen()
                self.handle_game_over_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.comet_timer:
                self.comet_list.append(Comet())
                pygame.time.set_timer(self.comet_timer, self.get_random_time())
        keys = pygame.key.get_pressed()
        self.dino.handle_keys(keys)

    def update(self):
        self.background_x -= 3
        if self.background_x == -600:
            self.background_x = 0
        self.dino.update()
        for comet in self.comet_list:
            comet.update()
            if self.dino.is_colliding(comet):
                if self.score > self.max_score:
                    redis_client.set('max_score', self.score)
                    self.max_score = int(self.score)
                print('Game over')
                pygame.time.delay(200)
                self.game_over = True

    def draw(self):
        self.screen.blit(self.background.image, (self.background_x, 0))
        self.screen.blit(self.background.image, (self.background_x + 600, 0))
        self.screen.blit(self.font.render(f'Max score: {self.max_score}', True, 'White'), (30, 30))
        self.screen.blit(self.font.render(f'Score: {int(self.score)}', True, 'White'), (420, 30))
        self.dino.draw(self.screen)
        for comet in self.comet_list:
            comet.draw(self.screen)
        pygame.display.update()

    def show_start_screen(self):
        self.screen.fill(('black'))
        font = pygame.font.Font('fonts/roboto.ttf', 26)
        text = font.render('Нажмите "SPACE" чтобы начать игру', True, 'white')
        self.screen.blit(text, (75, 150))
        pygame.display.flip()

    def handle_start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.gameplay = True

    def show_game_over_screen(self):
        self.screen.fill('black')
        text = pygame.font.Font('fonts/roboto.ttf', 58)
        text1 = pygame.font.Font('fonts/roboto.ttf', 21)
        text2 = pygame.font.Font('fonts/roboto.ttf', 15)
        self.screen.blit(text1.render(f'Max score: {self.max_score}', True, 'green'), (15, 15))
        self.screen.blit(text1.render(f'Your score: {int(self.score)}', True, 'white'), (15, 55))
        self.screen.blit(text.render('GAME OVER', True, 'red'), (135, 140))
        self.screen.blit(text2.render('Press "R" to restart game', True, 'white'), (210, 210))
        pygame.display.flip()

    def handle_game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.game_over = False
                self.reset_game()

    def reset_game(self):
        self.dino = Dino()
        self.comet_list = []
        self.comet_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.comet_timer, self.get_random_time())
        self.score = 0


if __name__ == "__main__":
    game = DinoGame()
    game.run()
    pygame.quit()
