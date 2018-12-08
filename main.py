# Tom Baker
# Randy the Robot
# Main Program

import os
import pygame
import random

# Define some constants.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ENEMY_SPAWN_LIST = [[0, 250], [400, 0], [850, 250], [400, 550]]

# Define the game screen.
pygame.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"
SIZE = (900, 600)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Randy the Robot")
icon = pygame.image.load("icon.bmp")
pygame.display.set_icon(icon)
FONT = pygame.font.SysFont("Calibri", 30, True, False)

# Load bit maps.
background = pygame.image.load("background.bmp")
enemy_img = pygame.image.load("enemy.bmp")
reward_img = pygame.image.load("reward.bmp")
speed_boost_img = pygame.image.load("speed_boost.bmp")
gun_boost_img = pygame.image.load("gun_boost.bmp")
player_img_up = pygame.image.load("robot_up.bmp")
player_img_down = pygame.image.load("robot_down.bmp")
player_img_left = pygame.image.load("robot_left.bmp")
player_img_right = pygame.image.load("robot_right.bmp")
enemy_img.set_colorkey(WHITE)
reward_img.set_colorkey(WHITE)
speed_boost_img.set_colorkey(WHITE)
gun_boost_img.set_colorkey(WHITE)
player_img_up.set_colorkey(WHITE)
player_img_down.set_colorkey(WHITE)
player_img_left.set_colorkey(WHITE)
player_img_right.set_colorkey(WHITE)

# Define clock for screen refreshing.
CLOCK = pygame.time.Clock()


class Sprite(object):
    pass

    def __init__(self, x, y, up, down, left, right):  # x and y are integers, up/down/left/right are bool.
        self.x_coord = x
        self.y_coord = y
        self.move_up = up
        self.move_down = down
        self.move_left = left
        self.move_right = right
        self.speed = 1  # 2 or 3 is ideal.


class Upgrade(Sprite):
    def __init__(self, x, y, boost_type):
        super(Upgrade, self).__init__(x, y, False, False, False, False)
        self.image = [speed_boost_img, gun_boost_img][boost_type]


class Player(Sprite):
    def __init__(self):
        super(Player, self).__init__(450, 300, False, False, False, False)
        self.is_shooting = False
        self.is_boosted = False
        self.boost_type = ""
        self.bullet_list = []
        self.wait_time = 0
        self.bullet_speed = 5
        self.speed = 2

    def shoot(self, up, down, left, right):
        if self.wait_time <= 0:
            self.bullet_list.append(
                Sprite(self.x_coord + 20, self.y_coord + 20, up, down, left, right))
            self.wait_time = player_shoot_speed
        else:
            self.wait_time -= 1


def setup():
    global done, player, enemy_list, reward_list, upgrade_list, reward_timer, player_max_bullets, \
        player_shoot_speed, MAX_REWARD_COUNT, BOOST_TIME, MAX_ENEMY_COUNT, enemy_spawn_time
    done = False
    player = Player()
    enemy_spawn_time = 0
    reward_timer = 0
    player_shoot_speed = 10
    player_max_bullets = 5
    MAX_REWARD_COUNT = 20
    MAX_ENEMY_COUNT = 30
    BOOST_TIME = 400
    enemy_list = []
    reward_list = []
    upgrade_list = []
    main()


def main():
    global done, player, player_img, enemy_list, reward_list, upgrade_list, reward_timer, MAX_ENEMY_COUNT, \
        player_max_bullets, BOOST_TIME, player_shoot_speed, enemy_spawn_time
    score = 0
    lost = False
    player_img = player_img_down
    aim_left = False
    aim_right = False
    aim_up = False
    aim_down = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.move_up = False
                if event.key == pygame.K_s:
                    player.move_down = False
                if event.key == pygame.K_a:
                    player.move_left = False
                if event.key == pygame.K_d:
                    player.move_right = False
                if event.key == pygame.K_LEFT \
                        or event.key == pygame.K_RIGHT \
                        or event.key == pygame.K_UP \
                        or event.key == pygame.K_DOWN:
                    player.is_shooting = False
                    if event.key == pygame.K_LEFT:
                        aim_left = False
                    if event.key == pygame.K_RIGHT:
                        aim_right = False
                    if event.key == pygame.K_UP:
                        aim_up = False
                    if event.key == pygame.K_DOWN:
                        aim_down = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.move_up = True
                if event.key == pygame.K_s:
                    player.move_down = True
                if event.key == pygame.K_a:
                    player.move_left = True
                if event.key == pygame.K_d:
                    player.move_right = True
                if event.key == pygame.K_LEFT \
                        or event.key == pygame.K_RIGHT \
                        or event.key == pygame.K_UP \
                        or event.key == pygame.K_DOWN:
                    player.is_shooting = True
                    if event.key == pygame.K_LEFT:
                        aim_left = True
                    if event.key == pygame.K_RIGHT:
                        aim_right = True
                    if event.key == pygame.K_UP:
                        aim_up = True
                    if event.key == pygame.K_DOWN:
                        aim_down = True

        # Game Logic.
        if lost:
            player.move_up = False
            player.move_down = False
            player.move_left = False
            player.move_right = False
            player.is_shooting = False
            reward_timer = 0

        if player.is_boosted:
            reward_timer -= 1
            if reward_timer <= 0:
                player.is_boosted = False
                if player.boost_type == gun_boost_img:
                    player_shoot_speed = 10
                    player_max_bullets = 5
                elif player.boost_type == speed_boost_img:
                    player.speed = 2

        # # Update player location.
        if player.move_left:
            player.x_coord -= player.speed
            if player.x_coord < 0:
                player.x_coord = 0
            player_img = player_img_left
        elif player.move_right:
            player.x_coord += player.speed
            if player.x_coord > 850:
                player.x_coord = 850
            player_img = player_img_right

        if player.move_up:
            player.y_coord -= player.speed
            if player.y_coord < 0:
                player.y_coord = 0
            player_img = player_img_up
        elif player.move_down:
            player.y_coord += player.speed
            if player.y_coord > 550:
                player.y_coord = 550
            player_img = player_img_down

        # # Update enemy location.
        if enemy_spawn_time <= 0 and len(enemy_list) < MAX_ENEMY_COUNT:
            enemy_spawn_time = 200 - (score * 2)
            if enemy_spawn_time < 50:
                enemy_spawn_time = 50
            for num in range(0, 2):     # perform 2 loops.
                spawn = random.randint(0, len(ENEMY_SPAWN_LIST) - 1)
                enemy_list.append(
                    Sprite(ENEMY_SPAWN_LIST[spawn][0], ENEMY_SPAWN_LIST[spawn][1], False, False, False, False))
        else:
            enemy_spawn_time -= 1
        for enemy in enemy_list:
            if enemy.x_coord < player.x_coord:
                enemy.x_coord += enemy.speed
            elif enemy.x_coord > player.x_coord:
                enemy.x_coord -= enemy.speed
            if enemy.y_coord < player.y_coord:
                enemy.y_coord += enemy.speed
            elif enemy.y_coord > player.y_coord:
                enemy.y_coord -= enemy.speed

        # # Update player bullet locations.
        if player.is_shooting and len(player.bullet_list) < player_max_bullets:
            player.shoot(aim_up, aim_down, aim_left, aim_right)

        if len(player.bullet_list) > 0:
            for bullet in player.bullet_list:
                if bullet.move_up:
                    bullet.y_coord -= player.bullet_speed
                    if bullet.y_coord <= 0:
                        player.bullet_list.remove(bullet)
                if bullet.move_down:
                    bullet.y_coord += player.bullet_speed
                    if bullet.y_coord >= 600:
                        player.bullet_list.remove(bullet)
                if bullet.move_left:
                    bullet.x_coord -= player.bullet_speed
                    if bullet.x_coord <= 0:
                        player.bullet_list.remove(bullet)
                if bullet.move_right:
                    bullet.x_coord += player.bullet_speed
                    if bullet.x_coord >= 900:
                        player.bullet_list.remove(bullet)

        # # Check for collisions.
        for bullet in player.bullet_list:
            for enemy in enemy_list:
                if (bullet.x_coord + 2 >= enemy.x_coord) and (bullet.x_coord + 8 <= enemy.x_coord + 50) \
                        and (bullet.y_coord + 2 >= enemy.y_coord) and (bullet.y_coord + 8 <= enemy.y_coord + 50):
                    player.bullet_list.remove(bullet)
                    if len(reward_list) < MAX_REWARD_COUNT:
                        r = random.randint(0, 10)   # reward on 0, banana on 4 or more, nothing between 1 and 3.
                        if r >= 4:
                            reward_list.append(Sprite(enemy.x_coord, enemy.y_coord, False, False, False, False))
                        elif r == 0:
                            upgrade_list.append(Upgrade(enemy.x_coord, enemy.y_coord, random.randint(0, 1)))
                    enemy_list.remove(enemy)
                    score += 1
                    break

        for enemy in enemy_list:
            if (player.x_coord - 20 <= enemy.x_coord) and (player.x_coord + 70 >= enemy.x_coord + 50) \
                    and (player.y_coord - 20 <= enemy.y_coord) and (player.y_coord + 70 >= enemy.y_coord + 50):
                lost = True
                break

        for reward in reward_list:
            if (player.x_coord - 20 <= reward.x_coord) and (player.x_coord + 70 >= reward.x_coord + 50) \
                    and (player.y_coord - 20 <= reward.y_coord) and (player.y_coord + 70 >= reward.y_coord + 50):
                score += 5
                reward_list.remove(reward)

        for boost in upgrade_list:
            if not player.is_boosted \
                    and (player.x_coord - 20 <= boost.x_coord) \
                    and (player.x_coord + 70 >= boost.x_coord + 50) \
                    and (player.y_coord - 20 <= boost.y_coord) \
                    and (player.y_coord + 70 >= boost.y_coord + 50):
                player.is_boosted = True
                player.boost_type = boost.image
                reward_timer = BOOST_TIME
                if boost.image == gun_boost_img:
                    player_shoot_speed = 5
                    player_max_bullets = 15
                elif boost.image == speed_boost_img:
                    player.speed = 5
                upgrade_list.remove(boost)

        # Drawing Code.
        # # BMP drawing code.
        screen.fill(WHITE)
        screen.blit(background, [0, 0])
        for reward in reward_list:
            screen.blit(reward_img, [reward.x_coord, reward.y_coord])
        screen.blit(player_img, [player.x_coord, player.y_coord])
        for enemy in enemy_list:
            screen.blit(enemy_img, [enemy.x_coord, enemy.y_coord])
        for upgrade in upgrade_list:
            screen.blit(upgrade.image, [upgrade.x_coord, upgrade.y_coord])

        # # Player bullet drawing code.
        for bullet in player.bullet_list:
            pygame.draw.ellipse(screen, RED, [bullet.x_coord, bullet.y_coord, 10, 10], 5)

        # # Draw Score.
        if lost:
            lost_display = FONT.render("YOU DIED", True, RED)
            screen.blit(lost_display, [375, 200])
        score_display = FONT.render("Score: " + str(score), True, BLACK)
        screen.blit(score_display, [30, 30])

        # # Draw reward timer.
        if player.is_boosted:
            boost_display = FONT.render("Upgrade countdown: " + str(reward_timer), True, BLACK)
            screen.blit(boost_display, [250, 30])
        # Update the screen.
        pygame.display.flip()
        CLOCK.tick(60)

    pygame.quit()


# Game Starts here.
setup()
