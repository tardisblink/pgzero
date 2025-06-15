import pgzrun
import math
import random
from pygame import Rect

# Definições de Tela
WIDTH = 800
HEIGHT = 480
TITLE = "Aliens VS Insects"
CREDITS = "Desenvolvido por Alberto Francisco - github.com/tardisblink"

# Estados do Jogo
STATE_MENU = "menu"
STATE_SELECTING = "selecting"
STATE_PAUSING = "pausing"
STATE_PLAYING = "playing"
STATE_EXIT = "exit"

# Valores padrão
game_state = STATE_MENU
sound_enabled = True
frame_counter = 0
mouse_pos = (0,0)
closing_countdown = 3
character = None

# Botões do menu principal
BUTTONS_MENU = [
    {"label": "Clique aqui para Iniciar o Jogo", "rect": Rect((WIDTH//2 - 200, 200), (400, 50)), "icon": "button-start", "action": "start"},
    {"label": "Sons/Música: ON", "rect": Rect((WIDTH//2 - 150, 290), (300, 45)), "icon": "audio-on", "action": "toggle_sound"},
    {"label": "Fechar o Jogo", "rect": Rect((WIDTH//2 - 150, 350), (300, 45)), "icon": "door", "action": "exit"},
]
hover_states_menu = [False] * len(BUTTONS_MENU)

BUTTONS_CHARACTERS = [
    {"label": "Blu", "rect": Rect((WIDTH - 760, HEIGHT // 2.6), (130, 100)), "icon": "alien-blue-badge", "action": "character_blue"},
    {"label": "Pin", "rect": Rect((WIDTH - 560, HEIGHT // 2.6), (130, 100)), "icon": "alien-pink-badge", "action": "character_pink"},
    {"label": "Bei", "rect": Rect((WIDTH - 360, HEIGHT // 2.6), (130, 100)), "icon": "alien-beige-badge", "action": "character_beige"},
    {"label": "Gim", "rect": Rect((WIDTH -160, HEIGHT // 2.6), (130, 100)), "icon": "alien-green-badge", "action": "character_green"},
]
hover_states_characters = [False] * len(BUTTONS_CHARACTERS)

def draw():
    global character
    
    if game_state == STATE_MENU:
        screen.clear()
        screen.draw.text(
            TITLE,
            center=(WIDTH // 2, HEIGHT // 5),
            fontsize=64,
            color="orange",
        )
        screen.draw.text(
            CREDITS,
            center=(WIDTH // 2, HEIGHT - 30),
            fontsize=20,
            color="white",
        )

        for i, button_menu_render in enumerate(BUTTONS_MENU):
            rect = button_menu_render["rect"]
            is_hover = rect.collidepoint(mouse_pos)
            button_collor = "darkorange" if is_hover else "orange"
            if is_hover and not hover_states_menu[i] and sound_enabled:
                sounds.hover.play()
            hover_states_menu[i] = is_hover
            screen.draw.filled_rect(rect, button_collor)
            
            label = button_menu_render["label"]
            icon_name = button_menu_render["icon"]
            if button_menu_render["action"] == "toggle_sound":
                if sound_enabled:
                    label = "Sons/Música: ON"
                    icon_name = "audio-on"
                else:
                    label = "Sons/Música: OFF"
                    icon_name = "audio-off"
            
            icon_actor = Actor(f"{icon_name}")
            icon_actor.topleft = (button_menu_render["rect"].left + 10, button_menu_render["rect"].centery - icon_actor.height // 2)
            icon_actor.draw()

            screen.draw.text(
                label,
                midleft=(button_menu_render["rect"].left + 70, button_menu_render["rect"].centery),
                fontsize=32,
                color="white"
            )
    
    elif game_state == STATE_SELECTING:

        screen.clear()
        screen.draw.text(
            "Selecione seu Personagem",
            center=(WIDTH // 2, HEIGHT // 4),
            fontsize=50,
            color="orange",
        )

        screen.draw.text(
            "Clique sobre o personagem para seleciona-lo",
            center=(WIDTH // 2, HEIGHT - 100),
            fontsize=30,
            color="white",
        )

        for i, button_characters_render in enumerate(BUTTONS_CHARACTERS):
            rect = button_characters_render["rect"]
            is_hover = rect.collidepoint(mouse_pos)
            button_collor = "darkorange" if is_hover else "orange"
            if is_hover and not hover_states_characters[i] and sound_enabled:
                sounds.hover.play()
            hover_states_characters[i] = is_hover
            screen.draw.filled_rect(rect, button_collor)
            
            label = button_characters_render["label"]
            icon_name = button_characters_render["icon"]
            
            icon_actor = Actor(f"{icon_name}")
            icon_actor.topleft = (button_characters_render["rect"].left + 5, button_characters_render["rect"].centery - icon_actor.height // 2)
            icon_actor.draw()

            screen.draw.text(
                label,
                midleft=(button_characters_render["rect"].left + 70, button_characters_render["rect"].centery),
                fontsize=32,
                color="white"
            )

    elif game_state == STATE_PLAYING and character != None:
        print(character)
        screen.clear()
        screen.draw.text(
            "Iniciando Jogo",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=50,
            color="orange",
        )

    elif game_state == STATE_EXIT:
        screen.clear()
        screen.draw.text(
            "Obrigado por jogar =D",
            center=(WIDTH // 2, HEIGHT // 3),
            fontsize=50,
            color="orange",
        )
        screen.draw.text(
            f"Fechando em {closing_countdown} ...",
            center=(WIDTH // 2, HEIGHT // 1.5),
            fontsize=30,
            color="white",
        )


def countdown_step():
    global closing_countdown
    closing_countdown -=1

    if closing_countdown > 0:
        clock.schedule(countdown_step, 1)
    else:
        exit()

def on_mouse_down(pos):
    global sound_enabled, game_state, character

    if game_state == STATE_MENU:
        for button_menu in BUTTONS_MENU:
            if button_menu["rect"].collidepoint(pos):
                if sound_enabled:
                    sounds.click.play()
                if button_menu["action"] == "toggle_sound":
                    sound_enabled = not sound_enabled
                elif button_menu["action"] == "start":
                    game_state = STATE_SELECTING
                elif button_menu["action"] == "exit":
                    game_state = STATE_EXIT
                    clock.schedule(countdown_step, 1)

    elif game_state == STATE_SELECTING and character is None:
        for button_character in BUTTONS_CHARACTERS:
            if button_character["rect"].collidepoint(pos):
                if sound_enabled:
                    sounds.click.play()
                if button_character["action"] == "character_blue":
                    game_state = STATE_PLAYING
                    character = "blue"
                elif button_character["action"] == "character_pink":
                    game_state = STATE_PLAYING
                    character = "pink"
                elif button_character["action"] == "character_beige":
                    game_state = STATE_PLAYING
                    character = "beige"
                elif button_character["action"] == "character_green":
                    game_state = STATE_PLAYING
                    character = "green"

def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos

pgzrun.go()