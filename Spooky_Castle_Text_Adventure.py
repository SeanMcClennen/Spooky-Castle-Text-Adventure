from browser import document, html, window, DOMEvent
import random

output_div = document["output"]
input_field = document["command_input"]
submit_button = document["submit_button"]

current_input_callback = None
game_initialized = False
game_is_over = False

def web_print(text=""):
    global output_div
    text_to_print = str(text)
    escaped_text = text_to_print.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    output_div.innerHTML += escaped_text.replace('\n', '<br>') + "<br>"
    output_div.scrollTop = output_div.scrollHeight

def web_input_prompt(prompt_text, callback):
    global current_input_callback
    if prompt_text: # Only print the prompt if it's not empty
        web_print(prompt_text)
    current_input_callback = callback
    input_field.focus()

def game_over_web(message=""):
    global game_is_over
    if message:
        web_print(message)
    # web_print("<strong>GAME OVER. Refresh the page to play again.</strong>") # Original didn't have this strong tag
    web_print("GAME OVER. Refresh the page to play again.")
    game_is_over = True
    input_field.disabled = True
    submit_button.disabled = True

x_coord = 0
y_coord = 0
game_map_data = 0 # Renamed from 'map'
gold = 0
health = 10
mana = 30
armor = 0
weaponcount = 0
firebook = 0
lightningbook = 0
enemyhealth = 0
enemyhealthstart = '3'
player_name_val = "" # Renamed from 'name'
player_class_val = "" # Renamed from 'clas'
map_size_choice = ""
grid = []

#    0 = trap
#    1 = nothing
#    2 = endgame
#    3 = orc
#    4 = pancakes
#    5 = sword
#    6 = armor
#    7 = wall
#    8 = zombie
#    9 = big orc
#    10 = giant spider
#    11 = chest
#    12 = fire magic book
#    13 = lightning magic book
#    14 = map

def remove_extra_twos_from_grid(current_grid):
    two_count = 0
    for row in current_grid:
        two_count += row.count(2)

    if two_count > 1:
        for i in range(len(current_grid)):
            for j in range(len(current_grid[i])):
                if current_grid[i][j] == 2:
                    current_grid[i][j] = random.randint(0, 15)
                    while current_grid[i][j] == 2:
                        current_grid[i][j] = random.randint(0,15)
                    two_count -= 1
                    if two_count == 1:
                        break
            if two_count == 1:
                break
    has_two = any(2 in row for row in current_grid)
    if not has_two and current_grid:
        rows = len(current_grid)
        cols = len(current_grid[0]) if rows > 0 else 0
        if rows > 0 and cols > 0:
            if rows > 1 or cols > 1:
                rx, ry = random.randint(0, cols-1), random.randint(0, rows-1)
                while rx == x_coord and ry == y_coord:
                    rx, ry = random.randint(0, cols-1), random.randint(0, rows-1)
                current_grid[ry][rx] = 2
            else:
                 current_grid[random.randint(0,rows-1)][random.randint(0,cols-1)] = 2


def setup_grid():
    global grid, x_coord, y_coord, map_size_choice
    if map_size_choice == 'random':
        o = random.randint(5, 30)
        p = random.randint(5, 30)
        grid = [[random.randint(0, 15) for _ in range(o)] for _ in range(p)]
        x_coord = random.randint(0, o - 1)
        y_coord = random.randint(0, p - 1)
        has_two = any(2 in row for row in grid)
        if not has_two and p > 0 and o > 0 :
            grid[random.randint(0, p-1)][random.randint(0, o-1)] = 2
        remove_extra_twos_from_grid(grid)
    elif map_size_choice == 'big':
        grid = [[1, 1, 0, 12, 11, 9, 7, 1, 1, 1, 0, 8, 1, 13, 11, 8, 6, 0, 1, 11],
                [11, 4, 5, 6, 14, 0, 7, 1, 0, 11, 1, 10, 1, 1, 3, 1, 1, 8, 1, 1],
                [6, 1, 1, 13, 8, 9, 7, 1, 3, 1, 1, 4, 6, 5, 0, 1, 4, 1, 1, 1],
                [1, 11, 1, 3, 1, 11, 7, 1, 1, 11, 1, 13, 1, 10, 11, 1, 1, 1, 8, 1],
                [5, 9, 1, 7, 7, 7, 7, 7, 0, 1, 1, 1, 4, 9, 1, 0, 1, 1, 12, 1],
                [1, 10, 0, 7, 1, 4, 12, 7, 1, 3, 1, 8, 1, 8, 6, 1, 3, 1, 13, 1],
                [1, 1, 1, 7, 5, 1, 6, 7, 1, 1, 0, 11, 10, 1, 12, 1, 0, 1, 1, 1],
                [7, 3, 7, 7, 3, 3, 3, 7, 7, 7, 7, 7, 7, 3, 7, 7, 7, 7, 7, 7],
                [0, 1, 4, 7, 11, 8, 0, 1, 5, 1, 6, 3, 13, 1, 1, 5, 1, 1, 1, 1],
                [4, 6, 3, 7, 1, 9, 3, 1, 11, 1, 0, 5, 1, 11, 1, 8, 4, 3, 1, 1],
                [7, 3, 7, 7, 7, 7, 7, 3, 7, 7, 3, 7, 7, 7, 3, 7, 7, 7, 7, 7],
                [12, 1, 7, 1, 13, 0, 8, 4, 1, 0, 4, 11, 1, 1, 0, 1, 11, 9, 0, 1],
                [3, 11, 8, 4, 0, 1, 1, 6, 1, 1, 1, 6, 1, 0, 1, 1, 6, 1, 1, 1],
                [1, 0, 7, 5, 11, 0, 1, 1, 8, 0, 10, 1, 12, 0, 1, 8, 1, 0, 1, 1],
                [10, 1, 7, 7, 7, 7, 7, 3, 7, 7, 7, 7, 7, 7, 7, 3, 7, 7, 7, 7],
                [0, 1, 7, 1, 0, 1, 1, 3, 1, 0, 9, 1, 7, 1, 0, 1, 6, 1, 0, 1],
                [7, 3, 7, 1, 8, 4, 6, 8, 1, 1, 4, 6, 7, 1, 11, 3, 0, 8, 3, 11],
                [0, 1, 9, 12, 1, 0, 1, 11, 5, 1, 8, 1, 3, 13, 1, 1, 3, 1, 1, 1],
                [1, 11, 1, 6, 1, 1, 3, 1, 1, 3, 10, 1, 7, 1, 0, 1, 4, 1, 9, 9],
                [11, 5, 8, 13, 1, 0, 1, 1, 6, 11, 12, 1, 7, 11, 1, 3, 13, 1, 9, 2]]
        x_coord = random.randint(0, 19)
        y_coord = random.randint(0, 19)
    elif map_size_choice == 'small':
        grid = [[7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                [7, 1, 3, 10, 4, 1, 5, 1, 6, 7],
                [7, 1, 7, 1, 7, 1, 7, 1, 7, 7],
                [7, 8, 7, 9, 1, 10, 1, 11, 1, 7],
                [7, 1, 7, 7, 7, 7, 7, 1, 7, 7],
                [7, 12, 7, 13, 1, 14, 1, 0, 1, 7],
                [7, 1, 7, 7, 7, 1, 7, 7, 7, 7],
                [7, 1, 8, 1, 9, 1, 8, 10, 1, 7],
                [7, 10, 1, 8, 1, 9, 1, 1, 2, 7],
                [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]]
        x_coord = random.randint(0, 9)
        y_coord = random.randint(0, 9)
    else:
        web_print("Invalid map size, defaulting to big.")
        map_size_choice = 'big'
        setup_grid()
        return

    if grid and 0 <= y_coord < len(grid) and 0 <= x_coord < len(grid[0]) and grid[y_coord][x_coord] == 7:
        found_start = False
        for r_idx, row_val in enumerate(grid):
            for c_idx, cell_val in enumerate(row_val):
                if cell_val != 7:
                    y_coord, x_coord = r_idx, c_idx
                    found_start = True
                    break
            if found_start:
                break
        if not found_start:
            web_print("Warning: Could not find a non-wall starting position!")


def display_intro_art():
    web_print(r"""
                             -|             |-
         -|                  [-_-_-_-_-_-_-_-]                  |-
         [-_-_-_-_-]          |             |          [-_-_-_-_-]
          | o   o |           [  0   0   0  ]           | o   o |
           |     |    -|       |           |       |-    |     |
           |     |_-___-___-___-|         |-___-___-___-_|     |
           |  o  ]              [    0    ]              [  o  |
           |     ]   o   o   o  [ _______ ]  o   o   o   [     | ----__________
_____----- |     ]              [ ||||||| ]              [     |
           |     ]              [ ||||||| ]              [     |
       _-_-|_____]--------------[_|||||||_]--------------[_____|-_-_
      ( (__________------------_____________-------------_________) )
                """)
    web_print('You are an explorer in search of gold. You enter the ominous looking castle and the door locks behind you. ')
    web_print('Now you must decide what to do....\n\n\nenter help for options')

battle_active = False
battle_enemy_name_for_prompt = ""

def chest():
    global player_name_val, gold, y_coord, x_coord, health, weaponcount, armor
    global firebook, lightningbook, mana, game_map_data, grid

    chance = random.randint(0, 6)
    if chance == 6:
        web_print(player_name_val + ' found a map')
        game_map_data += 1
    elif chance == 4:
        web_print(player_name_val + ' found a fire magic book in the chest\nyou can now use blaze flame when fighting enemies')
        firebook += 1
        web_print(r"""
                           __..._   _...__
                      _..-"      `Y`      "-._
                      \ Blaze     |           /
                      \\  Flame   |          //
                      \\\    3 mp |         ///
                       \\\ _..---.|.---.._ ///
                        \\`_..---.Y.---.._`//
                         '`               `'
                                    """)
    elif chance == 5:
        web_print(player_name_val + ' found a lightning magic book in the chest\nyou can now use bolt strike when fighting enemies')
        lightningbook += 1
        web_print(r"""
                           __..._   _...__
                      _..-"      `Y`      "-._
                      \ Bolt      |           /
                      \\  Strike  |          //
                      \\\   15 mp |         ///
                       \\\ _..---.|.---.._ ///
                        \\`_..---.Y.---.._`//
                         '`               `'
                                    """)
    elif chance == 0:
        damage_taken = max(0, 10 - armor)
        health -= damage_taken
        web_print(player_name_val + ' the chest was a trap -' + str(damage_taken) + 'hp')
        if armor > 0:
            web_print('armor protected ' + str(min(10, armor)) + ' hp')
    elif chance == 1:
        web_print(player_name_val + ' found pancakes in the chest +10hp')
        health += 10
    elif chance == 2:
        weaponcount += 1
        web_print(player_name_val + ' found a sword in the chest')
    elif chance == 3:
        armor += 1
        web_print(player_name_val + ' found armor in the chest')
    
    grid[y_coord][x_coord] = 1


def handle_battle_action(fight_command):
    global player_name_val, gold, y_coord, x_coord, health, weaponcount, armor
    global enemyhealth, enemyhealthstart, firebook, lightningbook, mana
    global battle_active, grid, battle_enemy_name_for_prompt

    if health <= 0:
        h_str = str(health)
        # web_print('you have ' + h_str + ' health left YOU LOSE') # From original, but more specific message below
        game_over_web('you have ' + h_str + ' health left YOU LOSE')
        battle_active = False
        return

    enemy_type_for_messages = battle_enemy_name_for_prompt
    enemy_hit_damage = 0
    enemy_punch_damage = 0
    flee_damage_mult = 1

    # Determine enemy stats based on type (simplified from original repeated blocks)
    if enemy_type_for_messages == "orc" or enemy_type_for_messages == "big orc": # big orc uses orc stats for damage
        enemy_hit_damage = 20
        enemy_punch_damage = 10
    elif enemy_type_for_messages == "giant spider":
        enemy_hit_damage = 20 # Original used 20
        enemy_punch_damage = 10 # Original used 10
    elif enemy_type_for_messages == "zombie":
        enemy_hit_damage = 10
        enemy_punch_damage = 5

    original_fight_command = fight_command # Keep a copy for "failed to decide" check
    fight_command = fight_command.lower().strip()

    if fight_command == "blaze flame":
        if firebook >= 1 and mana >=3:
            enemyhealth -= 3
            web_print(player_name_val + ' uses fire magic to burn ' + enemy_type_for_messages + ' it takes 3 damage\n')
            mana -= 3
            m_str = str(mana)
            web_print('remaining mana ' + m_str + '/30')
        elif firebook < 1:
            web_print(player_name_val + ' does not know fire magic')
        elif mana < 3:
            web_print(player_name_val + ' does not have enough mana for Blaze Flame (needs 3).')
    elif fight_command == "bolt strike":
        if lightningbook >= 1 and mana >= 15: # Original check was >10, cost was 15
            enemyhealth -= 10
            web_print(player_name_val + ' uses lightning magic to electrocute ' + enemy_type_for_messages + ' it takes 10 damage\n')
            mana -= 15
            m_str = str(mana)
            web_print('remaining mana ' + m_str + '/30')
        elif lightningbook < 1:
            web_print(player_name_val + ' does not know lightning magic')
        elif mana < 15:
            web_print(player_name_val + ' does not have enough mana for Bolt Strike (needs 15).')

    elif fight_command == "attack":
        if weaponcount < 1:
            chance = random.randint(0, 2)
            if chance > 1:
                actual_damage = max(0, enemy_hit_damage - armor)
                health -= actual_damage
                if enemy_type_for_messages == "giant spider":
                     web_print(player_name_val + ' got bit by the spider\n-' + str(actual_damage) + 'hp')
                elif enemy_type_for_messages == "zombie":
                     web_print(player_name_val + ' got bit by the zombie\n-' + str(actual_damage) + 'hp')
                else: # orc
                     web_print(player_name_val + ' got hit by orc\n-' + str(actual_damage) + 'hp')
            else:
                actual_damage_player = max(0, enemy_punch_damage - armor)
                health -= actual_damage_player
                enemyhealth -= 1
                web_print(f'{enemy_type_for_messages} punches {player_name_val} -{actual_damage_player}hp')
                if armor > 0 and actual_damage_player < enemy_punch_damage:
                    web_print('armor protected ' + str(enemy_punch_damage - actual_damage_player) + ' hp')
                web_print(player_name_val + ' punches ' + enemy_type_for_messages + ' it takes 1 damage')
            if armor > 0 and chance > 1 and actual_damage < enemy_hit_damage:
                 web_print('armor protected ' + str(enemy_hit_damage - actual_damage) + ' hp')

        else: # weaponcount >= 1
            chance = random.randint(0, 2)
            if chance == 0:
                weaponcount -= 1
                enemyhealth -= 2
                web_print(player_name_val + ' used a sword it breaks and the ' + enemy_type_for_messages + ' takes 2 damage ')
            else:
                enemyhealth -= 2
                web_print(player_name_val + ' used a sword the ' + enemy_type_for_messages + ' takes 2 damage ')
    elif fight_command == "run":
        chance = random.randint(0, 2)
        if chance > 1:
            actual_damage = max(0, enemy_hit_damage - armor) # Using enemy_hit_damage as base for flee hit
            health -= actual_damage
            web_print(player_name_val + ' got hit while running -' + str(actual_damage) + 'hp')
            if armor > 0 and actual_damage < enemy_hit_damage:
                web_print('armor protected ' + str(enemy_hit_damage - actual_damage) + ' hp')
        else:
            web_print(player_name_val + ' escaped successfully')
        battle_active = False
        prompt_for_action()
        return

    # Original logic for "failed to decide" - checking if command was not any of the valid ones
    # This is tricky because "attack" and "run" are valid. We need to check original_fight_command if it wasn't processed.
    # If a command was processed (e.g., blaze flame, bolt strike, attack, run), this block should be skipped.
    # A simpler way: if after all specific checks, no damage was dealt by player and it wasn't 'run'.
    # For now, assume any other text means player fumbled.
    elif original_fight_command.lower().strip() not in ["attack", "run", "blaze flame", "bolt strike"]:
        actual_damage = max(0, enemy_hit_damage - armor) # Using orc's hit damage as default for fumble
        health -= actual_damage
        web_print('failed to decide -' + str(actual_damage) + 'hp')
        if armor > 0 and actual_damage < enemy_hit_damage:
            web_print('armor protected ' + str(enemy_hit_damage - actual_damage) + ' hp')


    if health <= 0: # Check health again after player's action might have caused retaliation
        game_over_web('You have ' + str(health) + ' health left. YOU LOSE')
        battle_active = False
        return

    if enemyhealth <= 0:
        grid[y_coord][x_coord] = 1
        battle_active = False
        if enemy_type_for_messages == "orc" or enemy_type_for_messages == "big orc":
            web_print(f'the {enemy_type_for_messages} died +10 gold')
            gold += 10
        elif enemy_type_for_messages == "giant spider":
            web_print('the giant spider died +10 gold')
            gold += 10
        elif enemy_type_for_messages == "zombie":
            web_print('the zombie died +5 gold')
            gold += 5
            # Original zombie had a chance to not be removed from grid (grid[y][x]=1)
            # based on `fire == 0` (if blaze flame was used). Simplified for now.
            # To restore: need to track if blaze flame was used this combat.
        prompt_for_action()
        return

    if battle_active:
        o_str = str(enemyhealth)
        web_print(f'the {enemy_type_for_messages} has {o_str}/{enemyhealthstart} health left')
        #
