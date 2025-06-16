# Importação das bibliotecas permitidas
import pgzrun
import math
import random

# Importação de constantes e botões
from elements import *

# Estados e variáveis do jogo
game_state = STATE_MENU
sound_enabled = False
music_playing = False
frame_counter = 0
mouse_pos = (0, 0)
closing_countdown = 3
character = None
paused = False
game_over = False
you_win = False
hover_states_menu = [False] * len(BUTTONS_MENU)
hover_states_characters = [False] * len(BUTTONS_CHARACTERS)

# Flags de movimento contínuo
moving_left = False
moving_right = False

# Classes principais
class Player:
    def __init__(self, name):
        self.name = name
        self.actor = Actor(f"alien_{name}_stand", (100, HEIGHT - 80))
        self.vy = 0
        self.on_ground = False
        self.facing_right = True
        self.hearts = 3
        self.state = "stand" 
        self.idle_counter = 0
        self.last_x = self.actor.x 

    def update(self):
        self.vy += GRAVITY
        self.actor.y += self.vy
        if self.actor.y >= HEIGHT - 80:
            self.actor.y = HEIGHT - 80
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

        moving = abs(self.actor.x - self.last_x) > 0.5 

        if self.state == "duck":
            self.actor.image = f"alien_{self.name}_duck"
        elif not self.on_ground:
            self.actor.image = f"alien_{self.name}_jump"
        elif moving:
            frame = 1 if (self.actor.x // 10) % 2 == 0 else 2
            self.actor.image = f"alien_{self.name}_walk{frame}"
        else:
            self.idle_counter += 1
            frame = (self.idle_counter // 15) % 3
            if frame == 0:
                self.actor.image = f"alien_{self.name}_stand"
            elif frame == 1:
                self.actor.image = f"alien_{self.name}_swim1"
            else:
                self.actor.image = f"alien_{self.name}_swim2"

        self.last_x = self.actor.x

    def draw(self):
        self.actor.flip_x = not self.facing_right
        self.actor.angle = 0
        self.actor.draw()


class Enemy:
    def __init__(self, name, pos):
        self.name = name
        self.actor = Actor(name, pos)
        self.dead = False
        self.timer = 0
        self.vx = 2

    def update(self):
        if self.dead:
            return

        self.timer += 1

        frame = 1 + (self.timer // 20) % 2 

        if self.name == "bat":
            self.actor.y += math.sin(self.timer / 10) * 2
            self.actor.image = f"bat_fly{frame}"

        elif self.name == "spider":
            self.actor.image = f"spider_walk{frame}"

        self.actor.x -= self.vx

    def draw(self):
        if not self.dead:
            self.actor.draw()


# Background
background_map = GAME_BACKGROUND

def draw_background():
    for row_index, row in enumerate(background_map):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE + TILE_SIZE // 2
            y = row_index * TILE_SIZE + TILE_SIZE // 2
            Actor(tile, (x, y)).draw()


# Inicialização dos elementos do jogo
player = None
fireballs = []
enemies = [
    Enemy("bat", (600, HEIGHT - 150)),
    Enemy("bat", (500, HEIGHT - 200)),
    Enemy("bat", (300, HEIGHT - 200)),
    Enemy("bat", (1000, HEIGHT - 150)),
    Enemy("spider", (800, HEIGHT - 60)),
    Enemy("spider", (400, HEIGHT - 60)),
    Enemy("spider", (1200, HEIGHT - 60)),
    Enemy("spider", (2200, HEIGHT - 60)),
]

flag = Actor("flag_green_a", (750, HEIGHT - 80))
flag_timer = 0
btn_pause = Actor("pause", (40, 40))
btn_home = Actor("home", (100, 40))

def draw_hearts():
    for i in range(3):
        img = "hud_heart" if player.hearts > i else "hud_heart_empty"
        screen.blit(img, (WIDTH - (i + 1) * 70, 10))

def draw():
    global character, paused, you_win, game_over
    screen.clear()

    if game_state == STATE_MENU:
        paused = False
        game_over = False
        you_win = False
        screen.draw.text(TITLE, center=(WIDTH // 2, HEIGHT // 5), fontsize=64, color="orange")
        screen.draw.text(CREDITS, center=(WIDTH // 2, HEIGHT - 30), fontsize=20, color="white")
        for i, btn in enumerate(BUTTONS_MENU):
            rect = btn["rect"]
            hovered = rect.collidepoint(mouse_pos)
            if hovered and not hover_states_menu[i] and sound_enabled:
                sounds.hover.play()
            hover_states_menu[i] = hovered
            screen.draw.filled_rect(rect, "darkorange" if hovered else "orange")
            icon = Actor("audio-on" if sound_enabled and btn["action"] == "toggle_sound" else btn["icon"])
            icon.topleft = (rect.left + 10, rect.centery - icon.height // 2)
            icon.draw()
            label = btn["label"]
            if btn["action"] == "toggle_sound":
                label = "Sons/Música: ON" if sound_enabled else "Sons/Música: OFF"
            screen.draw.text(label, midleft=(rect.left + 70, rect.centery), fontsize=32, color="white")

    elif game_state == STATE_SELECTING:
        screen.draw.text("Selecione seu Personagem", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color="orange")
        screen.draw.text("Clique sobre o personagem para selecioná-lo", center=(WIDTH // 2, HEIGHT - 100), fontsize=30, color="white")
        for i, btn in enumerate(BUTTONS_CHARACTERS):
            rect = btn["rect"]
            hovered = rect.collidepoint(mouse_pos)
            if hovered and not hover_states_characters[i] and sound_enabled:
                sounds.hover.play()
            hover_states_characters[i] = hovered
            screen.draw.filled_rect(rect, "darkorange" if hovered else "orange")
            icon = Actor(btn["icon"])
            icon.topleft = (rect.left + 5, rect.centery - icon.height // 2)
            icon.draw()
            screen.draw.text(btn["label"], midleft=(rect.left + 70, rect.centery), fontsize=32, color="white")

    elif game_state == STATE_PLAYING and player:
        draw_background()
        flag.draw()
        for e in enemies:
            e.draw()
        for f in fireballs:
            f.draw()
        player.draw()
        draw_hearts()
        btn_pause.draw()
        btn_home.draw()
        screen.draw.text("ESPAÇO: Atirar bolas de fogo\nSETA CIMA: Pula\nSETA BAIXO: Abaixa\nSETA DIREITA: Anda para frente\nSETA ESQUERDA: Anda para trás", center=(WIDTH // 2, HEIGHT - 400), fontsize=30, color="black")

        if paused and (not game_over and not you_win):
            screen.draw.text("JOGO PAUSADO", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="black")
        if game_over:
            paused = True
            screen.draw.text("VOCÊ PERDEU =(", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")
        if you_win:
            paused = True
            screen.draw.text("VOCÊ GANHOU =)", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="green")

    elif game_state == STATE_EXIT:
        screen.draw.text("Obrigado por jogar =D", center=(WIDTH // 2, HEIGHT // 3), fontsize=50, color="orange")
        screen.draw.text(f"Fechando em {closing_countdown} ...", center=(WIDTH // 2, HEIGHT // 1.5), fontsize=30, color="white")

def update():
    global flag_timer, game_over, you_win, paused
    if game_state != STATE_PLAYING or paused or not player:
        return

    if moving_right:
        player.actor.x += 5
        player.facing_right = True
    elif moving_left:
        player.actor.x -= 5
        player.facing_right = False

    flag_timer += 1
    flag.image = "flag_green_a" if flag_timer % 60 < 30 else "flag_green_b"
    player.update()

    for e in enemies:
        e.update()
        if not e.dead and player.actor.colliderect(e.actor):
            player.hearts -= 1
            sounds.impact.play()
            e.dead = True
            if player.hearts <= 0:
                game_over = True
                print("GAME OVER")

    for f in fireballs[:]:
        f.x += f.vx
        for e in enemies:
            if not e.dead and f.colliderect(e.actor):
                e.dead = True
                fireballs.remove(f)
                sounds.impact.play()
                break
        if f.x < 0 or f.x > WIDTH:
            fireballs.remove(f)

    if player.actor.colliderect(flag):
        you_win = True
        sounds.impact.play()

def on_key_down(key):
    global moving_left, moving_right
    if game_state != STATE_PLAYING or not player:
        return

    if key == keys.RIGHT:
        moving_right = True
        sounds.impact.play()
    elif key == keys.LEFT:
        moving_left = True
        sounds.impact.play()
    elif key == keys.UP and player.on_ground:
        player.vy = JUMP_STRENGTH
        sounds.impact.play()
    elif key == keys.DOWN:
        player.state = "duck"
    elif key == keys.SPACE:
        offset = 30 if player.facing_right else -30
        fire = Actor("fireball", (player.actor.x + offset, player.actor.y))
        fire.vx = 5 if player.facing_right else -5
        fireballs.append(fire)
        sounds.impact.play()

def on_key_up(key):
    global moving_left, moving_right
    if player and key == keys.DOWN:
        player.state = "stand"
    if key == keys.RIGHT:
        moving_right = False
    elif key == keys.LEFT:
        moving_left = False

def on_mouse_down(pos):
    global sound_enabled, game_state, character, player, paused
    if game_state == STATE_MENU:
        for btn in BUTTONS_MENU:
            if btn["rect"].collidepoint(pos):
                if sound_enabled:
                    sounds.click.play()
                    play_music()
                if btn["action"] == "toggle_sound":
                    sound_enabled = not sound_enabled
                    play_music() if sound_enabled else stop_music()
                elif btn["action"] == "start":
                    game_state = STATE_SELECTING
                elif btn["action"] == "exit":
                    game_state = STATE_EXIT
                    clock.schedule(countdown_step, 1)

    elif game_state == STATE_SELECTING and not character:
        for btn in BUTTONS_CHARACTERS:
            if btn["rect"].collidepoint(pos):
                if sound_enabled:
                    sounds.click.play()
                character = btn["action"].split("_")[1]
                game_state = STATE_PLAYING
                player = Player(character)

    elif game_state == STATE_PLAYING:
        if btn_pause.collidepoint(pos):
            paused = not paused
        elif btn_home.collidepoint(pos):
            game_state = STATE_MENU
            character = None
            player = None
            fireballs.clear()
            for e in enemies:
                e.dead = False
                e.actor.x = random.randint(600, 800)

def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos

def play_music():
    global music_playing
    if not music_playing:
        sounds.music.play(loops=-1)
        music_playing = True

def stop_music():
    global music_playing
    sounds.music.stop()
    music_playing = False

def countdown_step():
    global closing_countdown
    closing_countdown -= 1
    if closing_countdown > 0:
        clock.schedule(countdown_step, 1)
    else:
        exit()

pgzrun.go()
