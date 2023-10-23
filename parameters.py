import pygame
import pygame.mixer


class Sounds:
    def __init__(self):
        pygame.mixer.init()
        self.start_music = pygame.mixer.Sound('sounds/undertale-shop.mp3')
        self.game_over_music = pygame.mixer.Sound('sounds/undertale-fallendown.mp3')
        self.encounter = pygame.mixer.Sound('sounds/undertale-save-game.mp3')

    def play_start_music(self):
        self.start_music.play()

    def stop_start_music(self):
        self.start_music.stop()

    def play_game_over_music(self):
        self.game_over_music.play()

    def stop_game_over_music(self):
        self.game_over_music.stop()

    def play_encounter_sound(self):
        self.encounter.play()


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
    pygame.mixer.init()

    def __init__(self):
        super().__init__(50, 210, 'images/dino_right/dino1.png', 52, 52)
        self.dino_walk = [
            pygame.transform.scale(pygame.image.load('images/dino_right/dino1.png').convert_alpha(), (52, 52)),
            pygame.transform.scale(pygame.image.load('images/dino_right/dino2.png').convert_alpha(), (52, 52)),
            pygame.transform.scale(pygame.image.load('images/dino_right/dino3.png').convert_alpha(), (52, 52)),
        ]
        self.__ani_dino = 0
        self.__is_jump = False
        self.__jump_count = 7
        self.__ani_speed = 10
        self.jump = pygame.mixer.Sound('sounds/jump_sound.wav')

    def handle_keys(self, keys):
        if not self.__is_jump:
            if keys[pygame.K_SPACE]:
                self.jump.play()
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
        self.image = self.dino_walk[self.__ani_dino // self.__ani_speed]

    def is_colliding(self, comet):
        return self.rect.colliderect(comet.rect)


class Comet(GameObject):
    def __init__(self):
        super().__init__(610, 225, 'images/comet.png', 32, 32)
        self.speed = 4

    def update(self):
        self.x -= self.speed
        self.rect.topleft = (self.x, self.y)
