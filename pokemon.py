# =========================================
# POKEMON: ECLIPSE OF THE VOID
# MASSIVE ASCII RPG - PART 1/4
# =========================================

import pygame
import random
import json
import os
import time

pygame.init()

# =========================================
# SCREEN SETTINGS
# =========================================

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokemon: Eclipse of the Void")

clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 24)
small_font = pygame.font.SysFont("consolas", 18)

# =========================================
# COLORS
# =========================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
GRAY = (120, 120, 120)

# =========================================
# ASCII ART
# =========================================

PIKACHU = ['''
`;-.          ___,
  `.`\_...._/`.-"`
    \        /      ,
    /()   () \    .' `-._
   |)  .    ()\  /   _.'
   \  -'-     ,; '. <
    ;.__     ,;|   > \
   / ,    / ,  |.-'.-'
  (_/    (_/ ,;|.<`
    \    ,     ;-`
     >   \    /
    (_,-'`> .'
         (_,'
''']

CHARMANDER = [
"   /\\\\",
"  / 🔥\\\\",
" | ^ ^ |",
" | --- |",
"  -----"
]

BULBASAUR = [
"   _____",
" / 🌱🌱 \\",
"| ◕ ◕ |",
"| --- |",
" -------"
]

SQUIRTLE = [
" ______",
"/ 💧💧\\\\",
"| ◕ ◕ |",
"| --- |",
" -------"
]

DRAGON = [
"      /\\\\",
" /\\___/\\\\",
"/ O O \\\\",
"/       \\\\",
"/__DRAGON_\\\\"
]

# =========================================
# MOVE CLASS
# =========================================

class Move:

    def __init__(self, name, power, move_type):

        self.name = name
        self.power = power
        self.move_type = move_type

# =========================================
# POKEMON CLASS
# =========================================

class Pokemon:

    def __init__(
        self,
        name,
        level,
        hp,
        attack,
        defense,
        speed,
        art
    ):

        self.name = name
        self.level = level
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.art = art
        self.exp = 0
        self.moves = []
        self.shiny = False

    def draw_ascii(self, x, y):

        for i, line in enumerate(self.art):

            text = small_font.render(line, True, WHITE)

            screen.blit(text, (x, y + i * 20))

    def is_alive(self):

        return self.hp > 0

    def attack_enemy(self, enemy, move):

        critical = random.randint(1, 100)

        damage = random.randint(
            self.attack + move.power - 5,
            self.attack + move.power + 5
        )

        damage -= enemy.defense // 2

        if damage < 1:
            damage = 1

        if critical <= 10:

            damage *= 2

            print("CRITICAL HIT!")

        enemy.hp -= damage

        if enemy.hp < 0:
            enemy.hp = 0

        print(f"{self.name} used {move.name}!")
        print(f"It dealt {damage} damage!")

    def gain_exp(self, amount):

        self.exp += amount

        print(f"{self.name} gained {amount} EXP!")

        if self.exp >= self.level * 30:

            self.level_up()

    def level_up(self):

        self.level += 1
        self.max_hp += 12
        self.attack += 4
        self.defense += 2
        self.speed += 1
        self.hp = self.max_hp
        self.exp = 0

        print("\n====================")
        print(f"{self.name} LEVELED UP!")
        print(f"LEVEL: {self.level}")
        print("====================")

# =========================================
# PLAYER CLASS
# =========================================

class Player:

    def __init__(self, name):

        self.name = name

        self.team = []

        self.inventory = {
            "Potion": 5,
            "Super Potion": 2,
            "Pokeball": 10,
            "Revive": 1
        }

        self.money = 1000
        self.badges = 0

        self.x = 100
        self.y = 100

    def draw(self):

        pygame.draw.rect(
            screen,
            BLUE,
            (self.x, self.y, 40, 40)
        )

    def move(self, keys):

        speed = 5

        if keys[pygame.K_LEFT]:
            self.x -= speed

        if keys[pygame.K_RIGHT]:
            self.x += speed

        if keys[pygame.K_UP]:
            self.y -= speed

        if keys[pygame.K_DOWN]:
            self.y += speed

# =========================================
# MOVES
# =========================================

thunderbolt = Move(
    "Thunderbolt",
    20,
    "Electric"
)

flamethrower = Move(
    "Flamethrower",
    22,
    "Fire"
)

water_gun = Move(
    "Water Gun",
    18,
    "Water"
)

leaf_blade = Move(
    "Leaf Blade",
    19,
    "Grass"
)

dragon_claw = Move(
    "Dragon Claw",
    30,
    "Dragon"
)

shadow_blast = Move(
    "Shadow Blast",
    35,
    "Dark"
)

# =========================================
# CREATE POKEMON
# =========================================

pikachu = Pokemon(
    "Pikachu",
    5,
    60,
    14,
    8,
    15,
    PIKACHU
)

pikachu.moves = [thunderbolt]

charmander = Pokemon(
    "Charmander",
    5,
    65,
    15,
    7,
    12,
    CHARMANDER
)

charmander.moves = [flamethrower]

bulbasaur = Pokemon(
    "Bulbasaur",
    5,
    70,
    13,
    10,
    10,
    BULBASAUR
)

bulbasaur.moves = [leaf_blade]

squirtle = Pokemon(
    "Squirtle",
    5,
    75,
    12,
    13,
    8,
    SQUIRTLE
)

squirtle.moves = [water_gun]

shadow_dragon = Pokemon(
    "Shadow Dragon",
    20,
    300,
    30,
    20,
    15,
    DRAGON
)

shadow_dragon.moves = [
    dragon_claw,
    shadow_blast
]

wild_pokemon = [
    pikachu,
    charmander,
    bulbasaur,
    squirtle
]

# =========================================
# STARTER SELECTION
# =========================================

def choose_starter(player):

    print("Choose your starter Pokemon:")
    print("1. Pikachu")
    print("2. Charmander")
    print("3. Bulbasaur")
    print("4. Squirtle")

    choice = input("Choose: ")

    if choice == "1":

        player.team.append(pikachu)

    elif choice == "2":

        player.team.append(charmander)

    elif choice == "3":

        player.team.append(bulbasaur)

    else:

        player.team.append(squirtle)

# =========================================
# SAVE SYSTEM
# =========================================

def save_game(player):

    data = {
        "name": player.name,
        "money": player.money,
        "badges": player.badges,
        "inventory": player.inventory
    }

    with open("save.json", "w") as file:

        json.dump(data, file)

    print("Game Saved!")

# =========================================
# LOAD SYSTEM
# =========================================

def load_game():

    if not os.path.exists("save.json"):

        return None

    with open("save.json", "r") as file:

        data = json.load(file)

    player = Player(data["name"])

    player.money = data["money"]
    player.badges = data["badges"]
    player.inventory = data["inventory"]

    return player

# =========================================
# DRAW TEXT
# =========================================

def draw_text(text, x, y, color=WHITE):

    img = font.render(text, True, color)

    screen.blit(img, (x, y))

# =========================================
# ATTACK ANIMATION
# =========================================

def attack_animation():

    for i in range(10):

        pygame.draw.circle(
            screen,
            YELLOW,
            (500, 300),
            i * 10
        )

        pygame.display.update()

        time.sleep(0.03)

# =========================================
# BATTLE SYSTEM
# =========================================

def battle(player, enemy):

    pokemon = player.team[0]

    running_battle = True

    while running_battle:

        screen.fill(BLACK)

        draw_text(
            f"{pokemon.name} HP: {pokemon.hp}/{pokemon.max_hp}",
            50,
            50
        )

        draw_text(
            f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}",
            650,
            50
        )

        pokemon.draw_ascii(50, 120)
        enemy.draw_ascii(650, 120)

        draw_text("1 - Attack", 50, 550)
        draw_text("2 - Potion", 50, 590)
        draw_text("3 - Catch", 50, 630)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:

                    move = pokemon.moves[0]

                    attack_animation()

                    pokemon.attack_enemy(enemy, move)

                    if enemy.is_alive():

                        enemy_move = random.choice(enemy.moves)

                        enemy.attack_enemy(
                            pokemon,
                            enemy_move
                        )

                if event.key == pygame.K_2:

                    if player.inventory["Potion"] > 0:

                        pokemon.hp += 30

                        if pokemon.hp > pokemon.max_hp:

                            pokemon.hp = pokemon.max_hp

                        player.inventory["Potion"] -= 1

                if event.key == pygame.K_3:

                    chance = random.randint(1, 100)

                    if chance <= 35:

                        print(f"You caught {enemy.name}!")

                        player.team.append(enemy)

                        return

                    else:

                        print("The Pokemon escaped!")

        if not pokemon.is_alive():

            print("Your Pokemon fainted!")

            running_battle = False

        if not enemy.is_alive():

            print(f"{enemy.name} defeated!")

            pokemon.gain_exp(50)

            running_battle = False

        clock.tick(60)

# =========================================
# END OF PART 1
# =========================================

# =========================================
# PART 2 OF 4
# OPEN WORLD + QUESTS + SHOPS + GYMS
# =========================================

# =========================================
# WORLD MAP
# =========================================

world_map = [
    "GGGGGGGGGGGGGGGGGGGG",
    "GTTTTGGGGGGMMMMMMGGG",
    "GGGGGGGGGGMMMMMMMMGG",
    "GGCCCCCGGGMMMMMMMMGG",
    "GGCCCCCGGGGGGGGGGGGG",
    "GGGGGGGGGGVVVVVVVGGG",
    "GGGGSSSSGGVVVVVVVGGG",
    "GGGGSSSSGGGGGGGGGGGG",
]

# G = Grass
# T = Town
# M = Mountain
# C = Cave
# V = Volcano
# S = Sea

TILE_SIZE = 48

# =========================================
# DRAW MAP
# =========================================

def draw_map():

    for row in range(len(world_map)):

        for col in range(len(world_map[row])):

            tile = world_map[row][col]

            x = col * TILE_SIZE
            y = row * TILE_SIZE

            if tile == "G":

                pygame.draw.rect(
                    screen,
                    GREEN,
                    (x, y, TILE_SIZE, TILE_SIZE)
                )

            elif tile == "T":

                pygame.draw.rect(
                    screen,
                    YELLOW,
                    (x, y, TILE_SIZE, TILE_SIZE)
                )

            elif tile == "M":

                pygame.draw.rect(
                    screen,
                    GRAY,
                    (x, y, TILE_SIZE, TILE_SIZE)
                )

            elif tile == "C":

                pygame.draw.rect(
                    screen,
                    BLACK,
                    (x, y, TILE_SIZE, TILE_SIZE)
                )

            elif tile == "V":

                pygame.draw.rect(
                    screen,
                    RED,
                    (x, y, TILE_SIZE, TILE_SIZE)
                )

            elif tile == "S":

                pygame.draw.rect(
                    screen,
                    BLUE,
                    (x, y, TILE_SIZE, TILE_SIZE)
                )

# =========================================
# QUEST SYSTEM
# =========================================

class Quest:

    def __init__(self, title, description, reward):

        self.title = title
        self.description = description
        self.reward = reward
        self.completed = False

    def complete(self, player):

        if not self.completed:

            self.completed = True

            player.money += self.reward

            print(f"Quest Complete: {self.title}")
            print(f"You earned ${self.reward}")

# =========================================
# QUEST LIST
# =========================================

quests = [

    Quest(
        "Forest Trouble",
        "Defeat 3 wild Pokemon in Brightleaf Forest.",
        300
    ),

    Quest(
        "Lost Pikachu",
        "Find the missing Pikachu near Thunder Mountain.",
        500
    ),

    Quest(
        "Shadow Invasion",
        "Defeat a Shadow League Grunt.",
        800
    )

]

# =========================================
# SHOP SYSTEM
# =========================================

shop_items = {

    "Potion": 100,
    "Super Potion": 300,
    "Pokeball": 200,
    "Revive": 700

}

def shop(player):

    shopping = True

    while shopping:

        print("\n===== POKEMON SHOP =====")
        print(f"Money: ${player.money}")

        for item, price in shop_items.items():

            print(f"{item} - ${price}")

        print("Type EXIT to leave")

        choice = input("Buy Item: ")

        if choice.upper() == "EXIT":

            shopping = False
            continue

        if choice in shop_items:

            price = shop_items[choice]

            if player.money >= price:

                player.money -= price

                if choice not in player.inventory:

                    player.inventory[choice] = 0

                player.inventory[choice] += 1

                print(f"You bought {choice}!")

            else:

                print("Not enough money!")

# =========================================
# HEALING CENTER
# =========================================

def pokemon_center(player):

    print("\nWelcome to the Pokemon Center!")

    for pokemon in player.team:

        pokemon.hp = pokemon.max_hp

    print("All Pokemon healed!")

# =========================================
# EVOLUTION SYSTEM
# =========================================

def evolve_pokemon(pokemon):

    if pokemon.name == "Charmander" and pokemon.level >= 16:

        print("Charmander is evolving!")

        pokemon.name = "Charmeleon"
        pokemon.max_hp += 30
        pokemon.attack += 10
        pokemon.defense += 5

    elif pokemon.name == "Squirtle" and pokemon.level >= 16:

        print("Squirtle is evolving!")

        pokemon.name = "Wartortle"
        pokemon.max_hp += 35
        pokemon.attack += 8
        pokemon.defense += 10

    elif pokemon.name == "Bulbasaur" and pokemon.level >= 16:

        print("Bulbasaur is evolving!")

        pokemon.name = "Ivysaur"
        pokemon.max_hp += 32
        pokemon.attack += 9
        pokemon.defense += 7

    elif pokemon.name == "Pikachu" and pokemon.level >= 20:

        print("Pikachu evolved into Raichu!")

        pokemon.name = "Raichu"
        pokemon.max_hp += 40
        pokemon.attack += 15
        pokemon.speed += 10

# =========================================
# RIVAL TRAINER
# =========================================

class Rival:

    def __init__(self, name):

        self.name = name
        self.team = []

rival = Rival("Kai")

rival_pokemon = Pokemon(
    "Eevee",
    7,
    80,
    14,
    10,
    14,
    BULBASAUR
)

rival_pokemon.moves = [leaf_blade]

rival.team.append(rival_pokemon)

# =========================================
# TRAINER BATTLE
# =========================================

def trainer_battle(player, rival):

    print(f"\n{rival.name} challenges you!")

    enemy = rival.team[0]

    battle(player, enemy)

# =========================================
# GYM LEADERS
# =========================================

class GymLeader:

    def __init__(self, name, pokemon, badge):

        self.name = name
        self.pokemon = pokemon
        self.badge = badge

fire_gym = GymLeader(

    "Blaze",

    Pokemon(
        "InfernoX",
        15,
        180,
        22,
        16,
        14,
        CHARMANDER
    ),

    "Flame Badge"
)

water_gym = GymLeader(

    "Aqua",

    Pokemon(
        "Wavefin",
        18,
        220,
        20,
        20,
        10,
        SQUIRTLE
    ),

    "Ocean Badge"
)

electric_gym = GymLeader(

    "Volt",

    Pokemon(
        "Zapstrike",
        20,
        240,
        28,
        16,
        22,
        PIKACHU
    ),

    "Thunder Badge"
)

# =========================================
# GYM BATTLE SYSTEM
# =========================================

def gym_battle(player, gym):

    print(f"\nGym Leader {gym.name} wants to battle!")

    gym.pokemon.moves = [
        thunderbolt,
        flamethrower,
        water_gun
    ]

    battle(player, gym.pokemon)

    if player.team[0].is_alive():

        print(f"You earned the {gym.badge}!")

        player.badges += 1

        player.money += 1000

# =========================================
# LEGENDARY POKEMON
# =========================================

eternava = Pokemon(
    "Eternava",
    50,
    500,
    45,
    40,
    35,
    DRAGON
)

eternava.moves = [
    dragon_claw,
    shadow_blast
]

thunderion = Pokemon(
    "Thunderion",
    45,
    450,
    40,
    35,
    45,
    PIKACHU
)

thunderion.moves = [
    thunderbolt
]

# =========================================
# RARE ENCOUNTERS
# =========================================

def rare_encounter(player):

    chance = random.randint(1, 100)

    if chance <= 5:

        print("A LEGENDARY POKEMON APPEARED!")

        battle(
            player,
            random.choice([eternava, thunderion])
        )

# =========================================
# INVENTORY DISPLAY
# =========================================

def show_inventory(player):

    print("\n===== INVENTORY =====")

    for item, amount in player.inventory.items():

        print(f"{item}: {amount}")

# =========================================
# TEAM DISPLAY
# =========================================

def show_team(player):

    print("\n===== TEAM =====")

    for pokemon in player.team:

        print(
            f"{pokemon.name} | "
            f"LVL {pokemon.level} | "
            f"HP {pokemon.hp}/{pokemon.max_hp}"
        )

# =========================================
# EXPLORE FUNCTION
# =========================================

def explore(player):

    encounter = random.randint(1, 100)

    if encounter <= 70:

        enemy = random.choice(wild_pokemon)

        enemy.hp = enemy.max_hp

        battle(player, enemy)

    else:

        rare_encounter(player)

# =========================================
# SHADOW LEAGUE STORY EVENT
# =========================================

def shadow_league_event():

    print("\n==========================")
    print("SHADOW LEAGUE ATTACK!")
    print("==========================")

    print("The sky suddenly turns dark...")
    print("Shadow soldiers invade the city!")
    print("Citizens run in fear.")
    print("A mysterious masked trainer appears.")

    time.sleep(2)

    print("\nOBSIDIAN:")
    print("\"You are too late, trainer.\"")
    print("\"Eternava will awaken soon.\"")

# =========================================
# END OF PART 2
# =========================================

# =========================================
# PART 3 OF 4
# ELITE FOUR + STORY MODE + OPEN WORLD LOOP
# =========================================

# =========================================
# ELITE FOUR
# =========================================

elite_four = []

elite1 = GymLeader(

    "Inferno Drake",

    Pokemon(
        "MagmaRex",
        40,
        420,
        40,
        30,
        25,
        CHARMANDER
    ),

    "Elite Fire Crest"
)

elite2 = GymLeader(

    "Luna Tide",

    Pokemon(
        "OceanLord",
        42,
        450,
        38,
        40,
        20,
        SQUIRTLE
    ),

    "Elite Water Crest"
)

elite3 = GymLeader(

    "Volt Titan",

    Pokemon(
        "ThunderBeast",
        44,
        470,
        45,
        28,
        45,
        PIKACHU
    ),

    "Elite Thunder Crest"
)

elite4 = GymLeader(

    "Eclipse Queen",

    Pokemon(
        "DarkPhoenix",
        48,
        520,
        50,
        35,
        40,
        DRAGON
    ),

    "Elite Shadow Crest"
)

elite_four.append(elite1)
elite_four.append(elite2)
elite_four.append(elite3)
elite_four.append(elite4)

# =========================================
# ELITE FOUR BATTLE SYSTEM
# =========================================

def elite_four_battle(player):

    print("\n======================")
    print("WELCOME TO THE ELITE FOUR")
    print("======================")

    for member in elite_four:

        print(f"\n{member.name} approaches!")

        member.pokemon.moves = [
            flamethrower,
            water_gun,
            thunderbolt,
            shadow_blast
        ]

        battle(player, member.pokemon)

        if not player.team[0].is_alive():

            print("You lost to the Elite Four!")
            return False

        print(f"{member.name} defeated!")

    print("\nYOU DEFEATED THE ELITE FOUR!")

    return True

# =========================================
# FINAL CHAMPION BATTLE
# =========================================

def champion_battle(player):

    print("\n======================")
    print("FINAL CHAMPION BATTLE")
    print("======================")

    shadow_dragon.hp = shadow_dragon.max_hp

    battle(player, shadow_dragon)

    if player.team[0].is_alive():

        print("\n======================")
        print("YOU ARE THE NEW CHAMPION!")
        print("======================")

        player.money += 10000

# =========================================
# STORY MODE
# =========================================

story_dialogue = [

    "Long ago, Eternava protected Eldoria.",
    "But darkness began spreading across the world.",
    "A mysterious trainer named Obsidian vanished.",
    "Years later, he returned with the Shadow League.",
    "Their goal: awaken Voidrake.",
    "The forbidden dragon of destruction."
]

def play_story():

    print("\n======================")
    print("POKEMON: ECLIPSE OF THE VOID")
    print("======================")

    for line in story_dialogue:

        print(line)

        time.sleep(2)

# =========================================
# CUTSCENE SYSTEM
# =========================================

def cutscene(title, lines):

    print("\n======================")
    print(title)
    print("======================")

    for line in lines:

        print(line)

        time.sleep(1.5)

# =========================================
# SHADOW GENERAL
# =========================================

shadow_general = Pokemon(
    "VoidHound",
    35,
    350,
    35,
    25,
    30,
    DRAGON
)

shadow_general.moves = [
    shadow_blast,
    dragon_claw
]

def shadow_general_battle(player):

    cutscene(
        "SHADOW GENERAL",
        [
            "A dark portal opens...",
            "Shadow General Nyx appears.",
            "\"You cannot stop Obsidian.\""
        ]
    )

    battle(player, shadow_general)

# =========================================
# DAY/NIGHT SYSTEM
# =========================================

game_time = 0

def update_day_night():

    global game_time

    game_time += 1

    if game_time >= 1000:

        game_time = 0

def draw_day_night():

    if game_time < 500:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(0)

    else:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((20, 20, 60))
        overlay.set_alpha(120)

    screen.blit(overlay, (0, 0))

# =========================================
# WEATHER SYSTEM
# =========================================

weather = "Clear"

def random_weather():

    global weather

    weather_options = [
        "Clear",
        "Rain",
        "Storm",
        "Fog"
    ]

    weather = random.choice(weather_options)

def draw_weather():

    if weather == "Rain":

        for i in range(100):

            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)

            pygame.draw.line(
                screen,
                BLUE,
                (x, y),
                (x + 2, y + 10),
                1
            )

    elif weather == "Storm":

        for i in range(150):

            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)

            pygame.draw.line(
                screen,
                WHITE,
                (x, y),
                (x + 2, y + 12),
                1
            )

# =========================================
# NPC SYSTEM
# =========================================

class NPC:

    def __init__(self, name, x, y, dialogue):

        self.name = name
        self.x = x
        self.y = y
        self.dialogue = dialogue

    def draw(self):

        pygame.draw.rect(
            screen,
            PURPLE,
            (self.x, self.y, 40, 40)
        )

    def talk(self):

        print(f"\n{self.name}:")
        print(self.dialogue)

npc_list = [

    NPC(
        "Professor Maple",
        300,
        200,
        "The Shadow League is growing stronger."
    ),

    NPC(
        "Old Fisherman",
        500,
        350,
        "I once saw Eternava in the ocean."
    ),

    NPC(
        "Young Trainer",
        700,
        450,
        "Gym Leaders are extremely powerful!"
    )
]

# =========================================
# NPC INTERACTION
# =========================================

def check_npc_interaction(player):

    for npc in npc_list:

        if abs(player.x - npc.x) < 50 and abs(player.y - npc.y) < 50:

            npc.talk()

# =========================================
# SOUND EFFECTS
# =========================================

def play_battle_sound():

    try:

        import winsound

        winsound.Beep(1000, 150)

    except:

        pass

def play_levelup_sound():

    try:

        import winsound

        winsound.Beep(1500, 300)

    except:

        pass

# =========================================
# OPEN WORLD GAME LOOP
# =========================================

def open_world(player):

    running = True

    random_weather()

    while running:

        screen.fill(BLACK)

        draw_map()

        draw_day_night()

        draw_weather()

        player.draw()

        for npc in npc_list:

            npc.draw()

        draw_text(
            f"Money: ${player.money}",
            20,
            20
        )

        draw_text(
            f"Badges: {player.badges}",
            20,
            60
        )

        draw_text(
            f"Weather: {weather}",
            20,
            100
        )

        pygame.display.update()

        keys = pygame.key.get_pressed()

        player.move(keys)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_e:

                    explore(player)

                if event.key == pygame.K_i:

                    show_inventory(player)

                if event.key == pygame.K_t:

                    show_team(player)

                if event.key == pygame.K_h:

                    pokemon_center(player)

                if event.key == pygame.K_q:

                    shadow_league_event()

                if event.key == pygame.K_r:

                    trainer_battle(player, rival)

                if event.key == pygame.K_1:

                    gym_battle(player, fire_gym)

                if event.key == pygame.K_2:

                    gym_battle(player, water_gym)

                if event.key == pygame.K_3:

                    gym_battle(player, electric_gym)

                if event.key == pygame.K_4:

                    elite_four_battle(player)

                if event.key == pygame.K_5:

                    champion_battle(player)

                if event.key == pygame.K_s:

                    save_game(player)

        check_npc_interaction(player)

        update_day_night()

        clock.tick(60)

# =========================================
# MAIN MENU
# =========================================

def main_menu():

    print("\n===============================================")
    print('''              _              
  _ __   ___ | | _____ _ __ ___   ___  _ __  
 | '_ \ / _ \| |/ / _ \ '_ ` _ \ / _ \| '_ \ 
 | |_) | (_) |   <  __/ | | | | | (_) | | | |
 | .__/ \___/|_|\_\___|_| |_| |_|\___/|_| |_|
 |_|                                         ''')
    print('                    RPG             ')
    print("===============================================")

    print("1. New Game")
    print("2. Load Game")

    choice = input("Choose: ")

    if choice == "1":

        name = input("Enter Trainer Name: ")

        player = Player(name)

        choose_starter(player)

        return player

    else:

        player = load_game()

        if player is None:

            print("No save found!")

            return main_menu()

        return player

# =========================================
# END OF PART 3
# =========================================

# =========================================
# PART 4 OF 4
# FINAL STORY + BOSSES + GAME START
# =========================================

# =========================================
# FINAL LEGENDARY BOSSES
# =========================================

voidrake = Pokemon(
    "Voidrake",
    70,
    900,
    70,
    55,
    45,
    DRAGON
)

voidrake.moves = [
    shadow_blast,
    dragon_claw,
    flamethrower,
    thunderbolt
]

eternava_final = Pokemon(
    "Eternava Prime",
    75,
    1000,
    75,
    60,
    50,
    DRAGON
)

eternava_final.moves = [
    dragon_claw,
    water_gun,
    thunderbolt,
    shadow_blast
]

# =========================================
# FINAL STORY ARC
# =========================================

def final_story():

    cutscene(
        "THE FINAL PROPHECY",
        [
            "Ancient ruins begin to shake...",
            "The sky cracks open with dark energy.",
            "Professor Maple discovers the truth.",
            "Obsidian was once a protector of Eldoria.",
            "But Voidrake corrupted his soul.",
            "Now the world faces destruction."
        ]
    )

# =========================================
# OBSIDIAN FINAL BATTLE
# =========================================

def obsidian_battle(player):

    cutscene(
        "OBSIDIAN APPEARS",
        [
            "\"You are strong, trainer.\"",
            "\"But strength alone cannot save this world.\"",
            "\"Voidrake will erase everything.\""
        ]
    )

    shadow_dragon.hp = shadow_dragon.max_hp

    battle(player, shadow_dragon)

# =========================================
# VOIDRAKE FINAL BATTLE
# =========================================

def voidrake_battle(player):

    cutscene(
        "VOIDRAKE AWAKENS",
        [
            "The ground begins collapsing.",
            "A gigantic dragon rises from darkness.",
            "Its roar shakes the entire world."
        ]
    )

    voidrake.hp = voidrake.max_hp

    battle(player, voidrake)

    if player.team[0].is_alive():

        print("\nVOIDRAKE HAS BEEN DEFEATED!")

# =========================================
# TRUE FINAL BATTLE
# =========================================

def eternava_battle(player):

    cutscene(
        "ETER NAVA PRIME",
        [
            "Light explodes across the sky.",
            "Eternava transforms into its true form.",
            "The final test has begun."
        ]
    )

    eternava_final.hp = eternava_final.max_hp

    battle(player, eternava_final)

    if player.team[0].is_alive():

        print("\nYOU MASTERED THE LEGENDARY POWER!")

# =========================================
# ENDING CUTSCENE
# =========================================

def ending_scene():

    cutscene(
        "THE END",
        [
            "Peace returns to Eldoria.",
            "Cities are rebuilt.",
            "Pokemon and humans celebrate together.",
            "You are remembered as the greatest trainer.",
            "But deep underground...",
            "Something still watches from the shadows..."
        ]
    )

# =========================================
# CREDITS
# =========================================

def credits():

    print("\n======================")
    print("POKEMON: ECLIPSE OF THE VOID")
    print("======================")

    credits_text = [

        "GAME DIRECTOR: YOU",
        "LEAD TRAINER: PLAYER",
        "PROFESSOR MAPLE",
        "OBSIDIAN",
        "VOIDRAKE",
        "ETER NAVA PRIME",
        "THANK YOU FOR PLAYING!"
    ]

    for line in credits_text:

        print(line)

        time.sleep(1)

# =========================================
# SIDE QUEST BOSSES
# =========================================

ice_titan = Pokemon(
    "Ice Titan",
    45,
    500,
    42,
    40,
    18,
    DRAGON
)

ice_titan.moves = [
    water_gun,
    shadow_blast
]

lava_beast = Pokemon(
    "Lava Beast",
    48,
    530,
    46,
    35,
    20,
    CHARMANDER
)

lava_beast.moves = [
    flamethrower,
    dragon_claw
]

storm_serpent = Pokemon(
    "Storm Serpent",
    50,
    600,
    50,
    38,
    42,
    PIKACHU
)

storm_serpent.moves = [
    thunderbolt,
    dragon_claw
]

# =========================================
# SIDE BOSS EVENTS
# =========================================

def side_boss_event(player):

    boss = random.choice([
        ice_titan,
        lava_beast,
        storm_serpent
    ])

    print(f"\nA wild boss {boss.name} appeared!")

    boss.hp = boss.max_hp

    battle(player, boss)

# =========================================
# ACHIEVEMENT SYSTEM
# =========================================

achievements = []

def unlock_achievement(name):

    if name not in achievements:

        achievements.append(name)

        print("\n======================")
        print(f"ACHIEVEMENT UNLOCKED: {name}")
        print("======================")

# =========================================
# PLAYER RANK SYSTEM
# =========================================

def player_rank(player):

    if player.badges >= 8:

        return "MASTER TRAINER"

    elif player.badges >= 5:

        return "ELITE TRAINER"

    elif player.badges >= 3:

        return "ADVANCED TRAINER"

    else:

        return "ROOKIE TRAINER"

# =========================================
# MAIN GAME START
# =========================================

def start_game():

    play_story()

    player = main_menu()

    print("\n======================")
    print("CONTROLS")
    print("======================")

    print("Arrow Keys = Move")
    print("E = Explore")
    print("I = Inventory")
    print("T = Team")
    print("H = Heal")
    print("Q = Story Event")
    print("R = Rival Battle")
    print("1 = Fire Gym")
    print("2 = Water Gym")
    print("3 = Electric Gym")
    print("4 = Elite Four")
    print("5 = Champion Battle")
    print("S = Save Game")

    open_world(player)

    if player.badges >= 3:

        unlock_achievement("Gym Conqueror")

    if len(player.team) >= 6:

        unlock_achievement("Pokemon Collector")

    print(f"\nTrainer Rank: {player_rank(player)}")

    final_story()

    obsidian_battle(player)

    if player.team[0].is_alive():

        voidrake_battle(player)

    if player.team[0].is_alive():

        eternava_battle(player)

    if player.team[0].is_alive():

        unlock_achievement("Savior of Eldoria")

        ending_scene()

        credits()

# =========================================
# GAME START
# =========================================

start_game()

# =========================================
# END OF GAME
# =========================================