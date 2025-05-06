from browser import document, html, window, DOMEvent
import random

output_div = None
input_field = None
submit_button = None

current_input_callback = None
game_initialized = False
game_is_over = False

def web_print(text=""):
    global output_div
    if output_div is None: # Should not happen if initialization is correct
        print(f"DEBUG (output_div is None): {text}") # Fallback to console
        return
    text_to_print = str(text)
    escaped_text = text_to_print.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    output_div.innerHTML += escaped_text.replace('\n', '<br>') + "<br>"
    output_div.scrollTop = output_div.scrollHeight

def web_input_prompt(prompt_text, callback):
    global current_input_callback, input_field
    if prompt_text:
        web_print(prompt_text)
    current_input_callback = callback
    if input_field:
        input_field.focus()

def game_over_web(message=""):
    global game_is_over, input_field, submit_button
    if message:
        web_print(message)
    web_print("GAME OVER. Refresh the page to play again.")
    game_is_over = True
    if input_field: input_field.disabled = True
    if submit_button: submit_button.disabled = True

x_coord = 0
y_coord = 0
game_map_data = 0
gold = 0
health = 10
mana = 30
armor = 0
weaponcount = 0
firebook = 0
lightningbook = 0
enemyhealth = 0
enemyhealthstart = '3'
player_name_val = ""
player_class_val = ""
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


def handle_battle_action(fight_command_raw):
    global player_name_val, gold, y_coord, x_coord, health, weaponcount, armor
    global enemyhealth, enemyhealthstart, firebook, lightningbook, mana
    global battle_active, grid, battle_enemy_name_for_prompt

    if health <= 0:
        h_str = str(health)
        game_over_web('you have ' + h_str + ' health left YOU LOSE')
        battle_active = False
        return

    enemy_type_for_messages = battle_enemy_name_for_prompt
    enemy_hit_damage = 0
    enemy_punch_damage = 0
    
    if enemy_type_for_messages == "orc" or enemy_type_for_messages == "big orc":
        enemy_hit_damage = 20
        enemy_punch_damage = 10
    elif enemy_type_for_messages == "giant spider":
        enemy_hit_damage = 20 
        enemy_punch_damage = 10 
    elif enemy_type_for_messages == "zombie":
        enemy_hit_damage = 10
        enemy_punch_damage = 5

    fight_command = fight_command_raw.lower().strip() # Process here

    action_processed_by_spell_or_attack = False

    if fight_command == "blaze flame":
        action_processed_by_spell_or_attack = True
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
        action_processed_by_spell_or_attack = True
        if lightningbook >= 1 and mana >= 15:
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
        action_processed_by_spell_or_attack = True
        if weaponcount < 1:
            chance = random.randint(0, 2)
            if chance > 1:
                actual_damage = max(0, enemy_hit_damage - armor)
                health -= actual_damage
                if enemy_type_for_messages == "giant spider": web_print(player_name_val + ' got bit by the spider\n-' + str(actual_damage) + 'hp')
                elif enemy_type_for_messages == "zombie": web_print(player_name_val + ' got bit by the zombie\n-' + str(actual_damage) + 'hp')
                else: web_print(player_name_val + ' got hit by orc\n-' + str(actual_damage) + 'hp')
                if armor > 0 and actual_damage < enemy_hit_damage : web_print('armor protected ' + str(enemy_hit_damage - actual_damage) + ' hp')
            else:
                actual_damage_player = max(0, enemy_punch_damage - armor)
                health -= actual_damage_player
                enemyhealth -= 1
                web_print(f'{enemy_type_for_messages} punches {player_name_val} -{actual_damage_player}hp')
                if armor > 0 and actual_damage_player < enemy_punch_damage: web_print('armor protected ' + str(enemy_punch_damage - actual_damage_player) + ' hp')
                web_print(player_name_val + ' punches ' + enemy_type_for_messages + ' it takes 1 damage')
        else: 
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
            actual_damage = max(0, enemy_hit_damage - armor) 
            health -= actual_damage
            web_print(player_name_val + ' got hit while running -' + str(actual_damage) + 'hp')
            if armor > 0 and actual_damage < enemy_hit_damage: web_print('armor protected ' + str(enemy_hit_damage - actual_damage) + ' hp')
        else:
            web_print(player_name_val + ' escaped successfully')
        battle_active = False
        prompt_for_action()
        return

    # This handles the original "failed to decide" logic if none of the above matched
    if not action_processed_by_spell_or_attack and fight_command != "run": # if command wasn't spell, attack, or run
        actual_damage = max(0, enemy_hit_damage - armor) 
        health -= actual_damage
        web_print('failed to decide -' + str(actual_damage) + 'hp') # original message
        if armor > 0 and actual_damage < enemy_hit_damage:
            web_print('armor protected ' + str(enemy_hit_damage - actual_damage) + ' hp')

    if health <= 0:
        game_over_web('you have ' + str(health) + ' health left. YOU LOSE')
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
        prompt_for_action()
        return

    if battle_active:
        o_str = str(enemyhealth)
        web_print(f'the {enemy_type_for_messages} has {o_str}/{enemyhealthstart} health left')
        web_input_prompt(f"{player_name_val} encountered a {enemy_type_for_messages}:\nAttack\nRun", handle_battle_action)


def start_battle(enemy_name_prompt_arg, initial_hp):
    global battle_active, enemyhealth, enemyhealthstart, battle_enemy_name_for_prompt
    battle_active = True
    enemyhealth = initial_hp
    enemyhealthstart = str(initial_hp)
    battle_enemy_name_for_prompt = enemy_name_prompt_arg # Use the argument
    web_input_prompt(f"{player_name_val} encountered a {enemy_name_prompt_arg}:\nAttack\nRun", handle_battle_action)

def orcbattle_wrapper(): # Wrapper to ensure global battle_enemy_name_for_prompt is set correctly
    global battle_enemy_name_for_prompt, enemyhealthstart
    battle_enemy_name_for_prompt = "orc" # Set for the specific orc type
    if enemyhealthstart == '10': # This implies a big orc from original setup
        battle_enemy_name_for_prompt = "big orc"
    start_battle(battle_enemy_name_for_prompt, int(enemyhealthstart))

def spiderbattle_wrapper():
    global battle_enemy_name_for_prompt, enemyhealthstart
    battle_enemy_name_for_prompt = "giant spider"
    start_battle(battle_enemy_name_for_prompt, int(enemyhealthstart))

def zombiebattle_wrapper():
    global battle_enemy_name_for_prompt, enemyhealthstart
    battle_enemy_name_for_prompt = "zombie"
    start_battle(battle_enemy_name_for_prompt, int(enemyhealthstart))


def look_check(direction_text):
    target_x, target_y = x_coord, y_coord
    valid_look = True
    actual_direction_looked = direction_text

    if direction_text == 'north':
        if y_coord > 0: target_y -=1
        else: valid_look = False
    elif direction_text == 'south':
        if y_coord < len(grid) - 1: target_y +=1
        else: valid_look = False
    elif direction_text == 'west':
        if x_coord > 0: target_x -=1
        else: valid_look = False
    elif direction_text == 'east':
        if grid and x_coord < len(grid[0]) - 1 : target_x +=1 # Check grid not empty
        else: valid_look = False
    else: 
        actual_direction_looked = ""

    if not valid_look or (not grid) or not (0 <= target_y < len(grid)) or not (grid[target_y]) or not (0 <= target_x < len(grid[target_y])): # Added checks
        web_print("saw a brick wall " + actual_direction_looked)
        return

    tile_val = grid[target_y][target_x]
    description = "saw "
    if tile_val == 1: description += "a safe path"
    elif tile_val == 0: description += "a trap"
    elif tile_val == 2: description += "treasure" 
    elif tile_val == 3: description += "a orc" 
    elif tile_val == 9: description += "a big orc"
    elif tile_val == 4: description += "some pancakes"
    elif tile_val == 5: description += "a sword"
    elif tile_val == 6: description += "armor"
    elif tile_val == 7: description += "a brick wall"
    elif tile_val == 10: description += player_name_val + " saw a giant spider"
    elif tile_val == 8: description += player_name_val + " saw a zombie"
    elif tile_val == 11: description += "a chest"
    elif tile_val == 12: description += "a fire magic book"
    elif tile_val == 13: description += "a lightning magic book"
    elif tile_val == 14: description += player_name_val + " saw a map"
    else: description = "saw something unknown" # Changed from mysterious to unknown
    
    web_print(description + (" " + actual_direction_looked if actual_direction_looked else ""))


def explore(direction_command_raw):
    global player_name_val, gold, y_coord, x_coord, health, weaponcount, armor
    global enemyhealth, enemyhealthstart, firebook, lightningbook, mana, game_map_data, grid

    if game_is_over: return

    if mana < 30:
        mana += 1
        web_print('1 mana restored')

    original_x, original_y = x_coord, y_coord
    action_taken = False # Tracks if any recognized action happened
    moved = False        # Tracks if player position changed

    cmd = direction_command_raw.lower().strip()

    if cmd == '':
        action_taken = True
        chance = random.randint(0, 100)
        if chance > 90 and grid[y_coord][x_coord] == 1 :
             grid[y_coord][x_coord] = 10 
    elif cmd in ['go north', 'walk north', 'north', 'up', 'walk up', 'go up']:
        action_taken = True
        if y_coord > 0:
            if grid[y_coord - 1][x_coord] != 7: y_coord -= 1; moved = True
            else: web_print('hit a wall cant go this way')
        else: web_print('hit a wall cant go this way')
    elif cmd in ['go south', 'walk south', 'south', 'down', 'walk down', 'go down']:
        action_taken = True
        if y_coord < len(grid) - 1:
            if grid[y_coord + 1][x_coord] != 7: y_coord += 1; moved = True
            else: web_print('hit a wall cant go this way')
        else: web_print('hit a wall cant go this way')
    elif cmd in ['go west', 'walk west', 'west', 'left', 'walk left', 'go left']:
        action_taken = True
        if x_coord > 0:
            if grid[y_coord][x_coord - 1] != 7: x_coord -= 1; moved = True
            else: web_print('hit a wall cant go this way')
        else: web_print('hit a wall cant go this way')
    elif cmd in ['go east', 'walk east', 'east', 'right', 'walk right', 'go right']:
        action_taken = True
        if grid and x_coord < len(grid[0]) - 1: # Check grid not empty
            if grid[y_coord][x_coord + 1] != 7: x_coord += 1; moved = True
            else: web_print('hit a wall cant go this way')
        else: web_print('hit a wall cant go this way')
    elif cmd in ['look north', 'check north', 'look up', 'check up']: look_check('north'); action_taken = True
    elif cmd in ['look south', 'check south', 'look down', 'check down']: look_check('south'); action_taken = True
    elif cmd in ['look west', 'check west', 'look left']: look_check('west'); action_taken = True
    elif cmd in ['look east', 'check east', 'look right', 'check right']: look_check('east'); action_taken = True
    elif cmd in ['look', 'check']:
        web_print(player_name_val + ' looks around')
        look_check('north');look_check('south');look_check('west');look_check('east')
        action_taken = True
    elif cmd in ['check map', 'map']:
        action_taken = True
        if game_map_data < 1: web_print(player_name_val + ' does not have a map')
        else:
            for r_idx, i_row in enumerate(grid):
                row_display = []
                for c_idx, j_cell in enumerate(i_row):
                    if r_idx == y_coord and c_idx == x_coord: row_display.append('@')
                    elif j_cell == 7: row_display.append('0')
                    else: row_display.append('.')
                web_print(" ".join(row_display))
    elif cmd in ['check stats', 'stats']:
        action_taken = True
        w, h, a, g, m = str(weaponcount), str(health), str(armor), str(gold), str(mana) # Shorten for f-string
        web_print('_____________________________')
        web_print(f'Name: {player_name_val}\nClass: {player_class_val}\nHealth: {h}\nMana: {m}\nSwords: {w}\narmor: {a}\ngold: {g}')
        if armor > 0 and weaponcount > 0: web_print('\n \\    O\n _\\|  |  }\n   M_/|\\_|}\n      |  }\n     / \\ \n   _/   \\_')
        elif weaponcount > 0 : web_print('\n \\    O\n _\\|  |   \n   M_/|\\_| \n      |   \n     / \\ \n   _/   \\_')
        elif armor > 0 : web_print('\n      O\n      |  }\n    _/|\\_|}\n      |  }\n     / \\ \n   _/   \\_')
        else: web_print('\n      O\n      |   \n    _/|\\_| \n      |   \n     / \\ \n   _/   \\_')
        if firebook >= 1: web_print(r"""
                   __..._   _...__
              _..-"      `Y`      "-._
              \ Blaze     |           /
              \\  FLame   |          //
              \\\    3 mp |         ///
               \\\ _..---.|.---.._ ///
                \\`_..---.Y.---.._`//
                 '`               `'
                            """)
        if lightningbook >= 1: web_print(r"""
                   __..._   _...__
              _..-"      `Y`      "-._
              \ bolt      |           /
              \\  strike  |          //
              \\\   15 mp |         ///
               \\\ _..---.|.---.._ ///
                \\`_..---.Y.---.._`//
                 '`               `'
                                        """)
        web_print('_____________________________')
    elif cmd == 'check swords': action_taken = True; web_print('you have ' + str(weaponcount) + ' swords')
    elif cmd == 'check health': action_taken = True; web_print('you have ' + str(health) + ' hp')
    elif cmd == 'check mana': action_taken = True; web_print('you have ' + str(mana) + ' mana')
    elif cmd == 'check armor': action_taken = True; web_print('you have ' + str(armor) + ' armor')
    elif cmd == 'check gold': action_taken = True; web_print('you have ' + str(gold) + ' gold')
    elif cmd == 'help':
        action_taken = True
        web_print('go "direction"\nwalk "direction"\ncheck health\ncheck mana\ncheck swords\ncheck armor\ncheck gold\nlook "direction"\nlook\ncheck "direction"\ncheck\ncheck stats\nstats\ncheck map\nmap\n')
    
    
    # Process tile player is ON or MOVED TO
    # This should happen if player moved OR if an action (like '' for spider) modified current tile OR if it's the first turn on a tile after battle/chest
    # The 'action_taken' flag helps distinguish no-op unknown commands from actual actions.
    # If an unknown command was typed (action_taken is False), we still need to re-prompt.

    current_tile_interaction_processed = False
    if moved or (cmd == '' and grid[y_coord][x_coord] == 10) : # Process if moved OR spider appeared
        current_tile = grid[y_coord][x_coord]
        current_tile_interaction_processed = True # Will be set by interaction

        if current_tile == 1: web_print(player_name_val + ' encounters nothing') 
        elif current_tile == 0:
            damage_taken = max(0, 10 - armor); health -= damage_taken
            web_print(player_name_val + ' fell in a trap -' + str(damage_taken) + 'hp')
            if armor > 0: web_print('armor protected ' + str(min(10, armor)) + ' hp')
            grid[y_coord][x_coord] = 1
        elif current_tile == 4: web_print(player_name_val + ' found pancakes +10hp'); health += 10; grid[y_coord][x_coord] = 1
        elif current_tile == 5: weaponcount += 1; grid[y_coord][x_coord] = 1; web_print(player_name_val + ' picked up a sword')
        elif current_tile == 6: armor += 1; grid[y_coord][x_coord] = 1; web_print(player_name_val + ' found armor')
        elif current_tile == 12:
            web_print(player_name_val + ' found a fire magic book\nyou can now use blaze flame when fighting enemies'); firebook += 1
            web_print(r"""
                           __..._   _...__
                      _..-"      `Y`      "-._
                      \ Blaze     |           /
                      \\  Flame   |          //
                      \\\    3 mp |         ///
                       \\\ _..---.|.---.._ ///
                        \\`_..---.Y.---.._`//
                         '`               `'
                                    """); grid[y_coord][x_coord] = 1
        elif current_tile == 13:
            web_print(player_name_val + ' found a lightning magic book\nyou can now use bolt strike when fighting enemies'); lightningbook += 1
            web_print(r"""
                           __..._   _...__
                      _..-"      `Y`      "-._
                      \ Bolt      |           /
                      \\  Strike  |          //
                      \\\   15 mp |         ///
                       \\\ _..---.|.---.._ ///
                        \\`_..---.Y.---.._`//
                         '`               `'
                                    """); grid[y_coord][x_coord] = 1
        elif current_tile == 14: web_print(player_name_val + ' found a map'); game_map_data += 1; grid[y_coord][x_coord] = 1
        elif current_tile == 3: web_print('Found a orc'); enemyhealthstart = '3'; orcbattle_wrapper(); return
        elif current_tile == 9: web_print('Found a big orc'); enemyhealthstart = '10'; orcbattle_wrapper(); return
        elif current_tile == 10: web_print('Found a giant spider'); enemyhealthstart = '5'; spiderbattle_wrapper(); return
        elif current_tile == 8: web_print('Found a zombie'); enemyhealthstart = '7'; zombiebattle_wrapper(); return
        elif current_tile == 11:
            web_print(player_name_val + ' found a chest, do you want to open it?')
            web_input_prompt("", handle_chest_open); return
        elif current_tile == 2:
            g_str = str(gold); web_print('you found the exit and you recovered ' + g_str + ' gold')
            game_over_web(); return
        else: # Unhandled tile number but was processed
            current_tile_interaction_processed = False # It wasn't a known item/enemy

    if not action_taken and cmd != "": # An unknown command was entered
        web_print("Unknown command. Type 'help' for options.")

    if health <= 0 and not game_is_over:
        h_str = str(health); game_over_web('you have ' + h_str + ' health left YOU LOSE')
        return

    if not battle_active and not game_is_over:
        prompt_for_action()


def handle_chest_open(yesno_raw):
    global grid, y_coord, x_coord
    if yesno_raw.lower().strip() in ['yes', 'y', 'i do', 'open']:
        chest()
    else:
        web_print(player_name_val + ' does not open the chest')
    
    if not battle_active and not game_is_over:
        prompt_for_action()

setup_step = 0

def process_setup_input(text_input_raw):
    global setup_step, player_name_val, player_class_val, map_size_choice, weaponcount, armor, game_initialized
    text_input = text_input_raw.strip()

    if setup_step == 0:
        player_name_val = text_input
        if not player_name_val: player_name_val = "Adventurer"
        setup_step = 1
        web_input_prompt('Pick a class:\n1. rogue 2 swords\n2. warrior 1 sword 1 armor\n3. paladin 2 armor', process_setup_input)
    elif setup_step == 1:
        choice = text_input
        if choice == '1': player_class_val = 'rogue'; weaponcount += 2
        elif choice == '2': player_class_val = 'warrior'; weaponcount += 1; armor += 1
        elif choice == '3': player_class_val = 'paladin'; armor += 2
        else: player_class_val = choice ; web_print("Class not chosen from list, starting with no class bonuses.")
        setup_step = 2
        web_input_prompt('big, small or random size map: ', process_setup_input)
    elif setup_step == 2:
        map_size_choice = text_input.lower()
        if map_size_choice not in ['big', 'small', 'random']:
            if map_size_choice == 'test': map_size_choice = 'big'; web_print("Test map not implemented for web, defaulting to big.")
            else: map_size_choice = 'big'; web_print("Invalid map size, defaulting to big map.")
        
        setup_grid()
        display_intro_art()
        game_initialized = True
        prompt_for_action()

def prompt_for_action():
    if game_is_over: return
    web_input_prompt("", process_command_input)

def process_command_input(command_text_raw):
    global game_initialized
    if game_is_over: return

    if not game_initialized: # Should not happen if setup calls prompt_for_action only after init
        process_setup_input(command_text_raw) # Route to setup if somehow called early
    elif battle_active:
        handle_battle_action(command_text_raw)
    else:
        explore(command_text_raw)

def handle_submit_button_click(event: DOMEvent):
    global current_input_callback, input_field
    if game_is_over or not input_field: return

    command = input_field.value
    input_field.value = ""

    if current_input_callback:
        callback_to_run = current_input_callback
        current_input_callback = None 
        callback_to_run(command)
    else:
        process_command_input(command)


def initialize_game_interface():
    global output_div, input_field, submit_button

    # Check if elements exist before trying to use them or bind events
    if "output" not in document or "command_input" not in document or "submit_button" not in document:
        print("CRITICAL ERROR: One or more HTML elements for the game interface are missing.")
        print("Ensure index.html contains elements with id='output', id='command_input', and id='submit_button'.")
        # Python's print goes to browser console with Brython.
        # Fallback to window.alert if trying to inform user directly.
        try:
            window.alert("Error: Critical game interface elements missing in HTML. Check console (F12).")
        except: #pylint: disable=bare-except
            pass # If window.alert itself fails in some strange Brython context
        return False

    output_div = document["output"]
    input_field = document["command_input"]
    submit_button = document["submit_button"]

    try:
        submit_button.bind("click", handle_submit_button_click)
        # Allow Enter key in input field to submit command
        input_field.bind("keypress", lambda ev: handle_submit_button_click(ev) if ev.keyCode == 13 else None)
    except Exception as e:
        print(f"Error binding events: {e}")
        if output_div: # Try to display error on page if output_div was found
            output_div.innerHTML += f"<br>RUNTIME ERROR BINDING UI EVENTS: {e}<br>Check console (F12)."
        else: # Fallback if output_div itself is the problem
            try: window.alert(f"Error binding game events: {e}. Check console (F12).")
            except: pass
        return False
    
    return True

# Main execution start
if initialize_game_interface():
    web_input_prompt('enter your name: ', process_setup_input)
else:
    # If initialization failed, errors should have been printed to console or alerted.
    # A message to a potentially non-existent output_div might not be seen.
    print("Game initialization failed. Check browser console (F12) for detailed errors.")
