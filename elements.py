from pygame import Rect

# Definições de Tela
WIDTH = 800
HEIGHT = 480
TILE_SIZE = 250
TITLE = "Aliens VS Insects"
CREDITS = "Desenvolvido por Alberto Francisco - github.com/tardisblink"

# Estados do Jogo
STATE_MENU = "menu"
STATE_SELECTING = "selecting"
STATE_PAUSING = "pausing"
STATE_PLAYING = "playing"
STATE_EXIT = "exit"

# Pergonagens
CHARACTER_BLUE = "blu"
CHARACTER_PINK = "pin"
CHARACTER_BEIGE = "bei"
CHARACTER_GREEN = "gim"

# Jogabilidade
GRAVITY = 0.5
JUMP_STRENGTH = -20


# Botões do menu principal
BUTTONS_MENU = [
    {"label": "Clique aqui para Iniciar o Jogo", "rect": Rect((WIDTH//2 - 200, 200), (400, 50)), "icon": "button-start", "action": "start"},
    {"label": "Sons/Música: OFF", "rect": Rect((WIDTH//2 - 150, 290), (300, 45)), "icon": "audio-off", "action": "toggle_sound"},
    {"label": "Fechar o Jogo", "rect": Rect((WIDTH//2 - 150, 350), (300, 45)), "icon": "door", "action": "exit"},
]
# Botões da selecção de personagens
BUTTONS_CHARACTERS = [
    {"label": CHARACTER_BLUE.capitalize(), "rect": Rect((WIDTH - 760, HEIGHT // 2.6), (130, 100)), "icon": "alien-blu-badge", "action": f"select_{CHARACTER_BLUE}"},
    {"label": CHARACTER_PINK.capitalize(), "rect": Rect((WIDTH - 560, HEIGHT // 2.6), (130, 100)), "icon": "alien-pin-badge", "action": f"select_{CHARACTER_PINK}"},
    {"label": CHARACTER_BEIGE.capitalize(), "rect": Rect((WIDTH - 360, HEIGHT // 2.6), (130, 100)), "icon": "alien-bei-badge", "action": f"select_{CHARACTER_BEIGE}"},
    {"label": CHARACTER_GREEN.capitalize(), "rect": Rect((WIDTH -160, HEIGHT // 2.6), (130, 100)), "icon": "alien-gim-badge", "action": f"select_{CHARACTER_GREEN}"},
]
# Botões do Jogo

GAME_BACKGROUND = [
    ["bg_cloud"]   * 4,
    ["bg_area"] * 4,
    ["bg_dirt"] * 4,
]


