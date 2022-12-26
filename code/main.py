import pygame
import sys
from settings import *
from player import Player
from monster import Coffin, Cactus
from allsprites import AllSprites
from sprite import Sprite, Bullet
from pytmx.util_pygame import load_pygame


class Game:
    def __init__(self):
        pygame.init()
        # Initial setup
        self.display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Western shooter')
        self.clock = pygame.time.Clock()
        self.bullet_surf = pygame.image.load('../graphics/other/particle.png').convert_alpha()

        # Groups
        self.all_groups = AllSprites()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()

        self.setup()

        # Music, sounds
        self.shoot_sound = pygame.mixer.Sound('../sound/bullet.wav')
        self.shoot_sound.set_volume(0.2)
        self.bg_music = pygame.mixer.Sound('../sound/music.mp3')
        self.bg_music.set_volume(0.5)
        self.bg_music.play(loops=-1)

        # Messages
        font = pygame.font.Font(None, 50)
        self.lose_text_surf = font.render('You have lost the game! Press space to restart.', True, 'gold')
        self.lose_text_rect = self.lose_text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.win_text_surf = font.render('You have won the game! Press space to restart.', True, 'gold')
        self.win_text_rect = self.win_text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.win = False

    def create_bullet(self, pos, direction):
        Bullet(pos, direction, self.bullet_surf, [self.all_groups, self.bullets])
        self.shoot_sound.play()

    def bullet_collision(self):

        # Bullet obstacle collision
        for obstacle in self.obstacles.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullets, True, pygame.sprite.collide_mask)

        # Bullet monster collision
        for bullet in self.bullets.sprites():
            sprites = pygame.sprite.spritecollide(bullet, self.monsters, False, pygame.sprite.collide_mask)
            if sprites:
                bullet.kill()
                for sprite in sprites:
                    sprite.damage()

        # Bullet player collision
        if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
            self.player.damage()

    def cleanup(self):
        for sprite in self.all_groups.sprites():
            sprite.kill()
        for sprite in self.obstacles.sprites():
            sprite.kill()
        for sprite in self.monsters.sprites():
            sprite.kill()

    def setup(self):
        tmx_map = load_pygame('../data/map.tmx')

        # Drawing tiles
        for x, y, surf in tmx_map.get_layer_by_name('fence').tiles():
            Sprite((x * 64, y * 64), surf, [self.all_groups, self.obstacles])

        # Drawing objects
        for obj in tmx_map.get_layer_by_name('objects'):
            Sprite((obj.x, obj.y), obj.image, [self.all_groups, self.obstacles])

        # Drawing entities
        for obj in tmx_map.get_layer_by_name('entities'):
            if obj.name == 'Player':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_groups,
                    path=PATHS['player'],
                    collision_sprites=self.obstacles,
                    create_bullet=self.create_bullet
                )

            if obj.name == 'Coffin':
                Coffin(
                    pos=(obj.x, obj.y),
                    groups=[self.all_groups, self.monsters],
                    path=PATHS['coffin'],
                    collision_sprites=self.obstacles,
                    player=self.player
                )

            if obj.name == 'Cactus':
                Cactus(
                    pos=(obj.x, obj.y),
                    groups=[self.all_groups, self.monsters],
                    path=PATHS['cactus'],
                    collision_sprites=self.obstacles,
                    player=self.player,
                    create_bullet=self.create_bullet
                )

    def run(self):
        # Game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not self.player.game_active:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.win = False
                        self.cleanup()
                        self.setup()

            if self.player.game_active:

                # Delta time
                dt = self.clock.tick() / 1000

                # Update groups
                self.all_groups.update(dt)
                self.bullet_collision()

                # Draw groups
                # self.display_surf.fill('black')
                self.all_groups.customize_draw(self.player)
                if len(self.monsters) == 0:
                    self.player.game_active = False
                    self.win = True
            else:
                if self.win:
                    self.display_surf.fill('black')
                    self.display_surf.blit(self.win_text_surf, self.win_text_rect)
                else:
                    self.display_surf.fill('black')
                    self.display_surf.blit(self.lose_text_surf, self.lose_text_rect)

            # pygame.display.update()
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
