from browser import document, html, window, DOMEvent
import random
# sys module is not fully available/applicable in Brython in the same way for sys.exit
# We'll handle game over differently.

# --- Globals to manage game state and I/O ---
output_div = document["output"]
input_field = document["command_input"]
submit_button = document["submit_button"]

current_input_callback = None
game_initialized = False
game_is_over = False

# --- Web I/O Functions ---
def web_print(text=""):
    global output_div
    # Convert any non-string to string
    text_to_print = str(text)
    # Replace newlines with <br> for HTML display
    # And handle potential HTML in text by escaping (simplistic version)
    escaped_text = text_to_print.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    output_div.innerHTML += escaped_text.replace('\n', '<br>') + "<br>"
    output_div.scrollTop = output_div.scrollHeight # Auto-scroll

def web_input_prompt(prompt_text, callback):
    global current_input_callback
    web_print(f'<span class="prompt">{prompt_text}</span>')
    current_input_callback = callback
    input_field.focus()

def game_over_web(message=""):
    global game_is_over
    if message:
        web_print(message)
    web_print("<strong>GAME OVER. Refresh the page to play again.</strong>")
    game_is_over = True
    input_field.disabled = True
    submit_button.disabled = True


# --- Original Game Code (with modifications) ---
x_coord = 0 # Renamed from 'x' to avoid conflict if Brython uses 'x'
y_coord = 0 # Renamed from 'y'

game_map = 0 # Renamed from 'map' as it's a built-in
gold = 0
health = 10
mana = 30
armor = 0
weaponcount = 0
firebook = 0
lightningbook = 0
enemyhealth = 0
enemyhealthstart = '3'
player_name = "" # Renamed from 'name'
player_class = "" # Renamed from 'clas'
map_size_choice = ""
grid = []


def remove_extra_twos_from_grid(current_grid): # Renamed 'grid' param
    two_count = 0
    for row in current_grid:
        two_count += row.count(2)

    if two_count > 1:
        for i in range(len(current_grid)):
            for j in range(len(current_grid[i])):
                if current_grid[i][j] == 2:
                    current_grid[i][j] = random.randint(0, 15) # Ensure not 2 again if possible
                    while current_grid[i][j] == 2: # re-roll if it's 2 again
                        current_grid[i][j] = random.randint(0,15)
                    two_count -= 1
                    if two_count == 1:
                        break
            if two_count == 1:
                break
    # Ensure at least one '2' exists if it was removed
    has_two = any(2 in row for row in current_grid)
    if not has_two and current_grid:
        rows = len(current_grid)
        cols = len(current_grid[0]) if rows > 0 else 0
        if rows > 0 and cols > 0:
             # Try to place it not on the starting spot, if possible and map is larger
            if rows > 1 or cols > 1:
                rx, ry = random.randint(0, cols-1), random.randint(0, rows-1)
                while rx == x_coord and ry == y_coord: # Avoid player start
                    rx, ry = random.randint(0, cols-1), random.randint(0, rows-1)
                current_grid[ry][rx] = 2
            else: # Tiny map, just place it
                 current_grid[random.randint(0,rows-1)][random.randint(0,cols-1)] = 2


def setup_grid():
    global grid, x_coord, y_coord, map_size_choice
    if map_size_choice == 'random':
        o = random.randint(5, 30)
        p = random.randint(5, 30)
        grid = [[random.randint(0, 15) for _ in range(o)] for _ in range(p)]
        # Place player randomly, ensuring it's within new grid bounds
        x_coord = random.randint(0, o - 1)
        y_coord = random.randint(0, p - 1)

        # Ensure there's an endgame '2', but only one.
        # First, make sure '2' is definitely present
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
        x_coord = random.randint(0, 19) # Default was 0,9. Random for big map.
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
        x_coord = random.randint(0, 9) # Default was 0,9. Random for small map
        y_coord = random.randint(0, 9)
    else: # Default to big if invalid choice (or handle as error)
        web_print("Invalid map size, defaulting to big.")
        map_size_choice = 'big' # ensure it's set for next logic
        setup_grid() # Recurse to set up big map
        return

    # Ensure player starts on a walkable tile (not 7=wall) if possible
    # This is a simple check; more complex logic might be needed for sparse maps
    if grid and 0 <= y_coord < len(grid) and 0 <= x_coord < len(grid[0]) and grid[y_coord][x_coord] == 7:
        # Try to find a non-wall spot
        found_start = False
        for r_idx, row_val in enumerate(grid):
            for c_idx, cell_val in enumerate(row_val):
                if cell_val != 7:
                    y_coord, x_coord = r_idx, c_idx
                    found_start = True
                    break
            if found_start:
                break
        if not found_start: # Should not happen with current maps but good for safety
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
    web_print('Now you must decide what to do....\n\n\nType "help" for options')

# --- Define game logic functions (chest, orcbattle, etc.) ---
# These will use web_print and might need adjustment for web_input_prompt if they have nested inputs

battle_active = False
battle_enemy_func = None
battle_enemy_name_for_prompt = ""

def chest():
    global player_name, gold, y_coord, x_coord, health, weaponcount, armor
    global firebook, lightningbook, mana, game_map, grid

    chance = random.randint(0, 6)
    if chance == 6:
        web_print(player_name + ' found a map')
        game_map += 1
    # grid[y_coord][x_coord] = 1 # This should happen after interaction
    elif chance == 4:
        web_print(player_name + ' found a fire magic book in the chest\nyou can now use blaze flame when fighting enemies')
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
        web_print(player_name + ' found a lightning magic book in the chest\nyou can now use bolt strike when fighting enemies')
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
        damage_taken = max(0, 10 - armor) # Ensure damage isn't negative
        health -= damage_taken
        web_print(player_name + ' the chest was a trap -' + str(damage_taken) + 'hp')
        if armor > 0:
            web_print('armor protected ' + str(min(10, armor)) + ' hp') # Show how much armor absorbed from this hit
    elif chance == 1:
        web_print(player_name + ' found pancakes in the chest +10hp')
        health += 10
    elif chance == 2:
        weaponcount += 1
        web_print(player_name + ' found a sword in the chest')
    elif chance == 3:
        armor += 1
        web_print(player_name + ' found armor in the chest')
    
    grid[y_coord][x_coord] = 1 # Mark chest as looted


def handle_battle_action(fight_command):
    global player_name, gold, y_coord, x_coord, health, weaponcount, armor
    global enemyhealth, enemyhealthstart, firebook, lightningbook, mana
    global battle_active, battle_enemy_func, grid, battle_enemy_name_for_prompt

    if health <= 0:
        h_str = str(health)
        web_print('You have ' + h_str + ' health left. YOU LOSE')
        game_over_web()
        battle_active = False
        return

    enemy_type_for_messages = battle_enemy_name_for_prompt # e.g., "orc", "spider", "zombie"
    enemy_hit_damage = 0
    enemy_punch_damage = 0
    flee_damage_mult = 1 # default, orcs might hit harder when fleeing etc.

    if enemy_type_for_messages == "orc":
        enemy_hit_damage = 20
        enemy_punch_damage = 10
    elif enemy_type_for_messages == "giant spider":
        enemy_hit_damage = 20 # Assuming same as orc from original code
        enemy_punch_damage = 10
    elif enemy_type_for_messages == "zombie":
        enemy_hit_damage = 10
        enemy_punch_damage = 5
        # Zombies might not hit harder on flee, could adjust flee_damage_mult

    # Player action
    if fight_command == "blaze flame":
        if firebook >= 1 and mana >= 3:
            mana -= 3
            damage_dealt = 3
            if enemy_type_for_messages == "zombie":
                # Assuming fire stops zombie regen, handled implicitly by not adding health back
                web_print(player_name + ' uses fire magic to burn ' + enemy_type_for_messages + '. It takes ' + str(damage_dealt) + ' damage and cannot regenerate.')
            else:
                web_print(player_name + ' uses fire magic to burn ' + enemy_type_for_messages + '. It takes ' + str(damage_dealt) + ' damage.')
            enemyhealth -= damage_dealt
            m_str = str(mana)
            web_print('Remaining mana ' + m_str + '/30')
        elif firebook < 1:
            web_print(player_name + ' does not know fire magic.')
        elif mana < 3:
            web_print(player_name + ' does not have enough mana for Blaze Flame (needs 3).')

    elif fight_command == "bolt strike":
        if lightningbook >= 1 and mana >= 15: # Original code said 10, then 15 for mana cost
            mana -= 15
            damage_dealt = 10
            enemyhealth -= damage_dealt
            web_print(player_name + ' uses lightning magic to electrocute ' + enemy_type_for_messages + '. It takes ' + str(damage_dealt) + ' damage.')
            m_str = str(mana)
            web_print('Remaining mana ' + m_str + '/30')
        elif lightningbook < 1:
            web_print(player_name + ' does not know lightning magic.')
        elif mana < 15:
             web_print(player_name + ' does not have enough mana for Bolt Strike (needs 15).')


    elif fight_command == "attack":
        if weaponcount < 1: # Bare hands
            chance = random.randint(0, 2)
            if chance > 1: # Enemy hits hard
                damage_taken = max(0, enemy_hit_damage - armor)
                health -= damage_taken
                web_print(f'{enemy_type_for_messages.capitalize()} hits {player_name} hard! -{damage_taken}hp')
            else: # Exchange blows
                damage_taken = max(0, enemy_punch_damage - armor)
                health -= damage_taken
                enemyhealth -= 1 # Player punches for 1 damage
                web_print(f'{enemy_type_for_messages.capitalize()} hits {player_name} -{damage_taken}hp')
                web_print(f'{player_name} punches {enemy_type_for_messages}, it takes 1 damage.')
            if armor > 0 and damage_taken < (enemy_hit_damage if chance > 1 else enemy_punch_damage) : # if armor absorbed anything
                web_print(f'Your armor absorbed { (enemy_hit_damage if chance > 1 else enemy_punch_damage) - damage_taken } damage.')
        else: # Has weapon
            chance = random.randint(0, 2)
            damage_dealt = 2
            if chance == 0: # Weapon breaks
                weaponcount -= 1
                web_print(player_name + ' used a sword, it breaks! The ' + enemy_type_for_messages + ' takes ' + str(damage_dealt) + ' damage.')
            else:
                web_print(player_name + ' used a sword. The ' + enemy_type_for_messages + ' takes ' + str(damage_dealt) + ' damage.')
            enemyhealth -= damage_dealt

    elif fight_command == "run":
        chance = random.randint(0, 2)
        if chance > 1: # Got hit while running
            damage_taken = max(0, int(enemy_hit_damage * flee_damage_mult) - armor) # Potentially different damage on flee
            health -= damage_taken
            web_print(player_name + ' got hit while running -' + str(damage_taken) + 'hp')
            if armor > 0 and damage_taken < int(enemy_hit_damage * flee_damage_mult) :
                web_print(f'Your armor absorbed {int(enemy_hit_damage * flee_damage_mult) - damage_taken} damage.')
        else:
            web_print(player_name + ' escaped successfully!')
        battle_active = False # Exited battle
        # Player stays in the same spot if they ran, original code implies this.
        # No need to call explore() here, main loop will ask for next command.
        prompt_for_action()
        return # Skip enemy turn and further checks this round

    else: # Invalid command
        damage_taken = max(0, enemy_hit_damage - armor) # Default to hard hit for fumbling
        health -= damage_taken
        web_print(f'Failed to decide! {enemy_type_for_messages.capitalize()} hits you. -{damage_taken}hp')
        if armor > 0 and damage_taken < enemy_hit_damage:
             web_print(f'Your armor absorbed {enemy_hit_damage - damage_taken} damage.')


    # Check if player died from their action or enemy counter
    if health <= 0:
        web_print(f'You have been slain by the {enemy_type_for_messages}!')
        game_over_web()
        battle_active = False
        return

    # Enemy defeated?
    if enemyhealth <= 0:
        grid[y_coord][x_coord] = 1 # Mark enemy as defeated
        battle_active = False
        if enemy_type_for_messages == "orc":
            web_print('The orc died! +10 gold')
            gold += 10
        elif enemy_type_for_messages == "giant spider":
            web_print('The giant spider died! +10 gold') # Original used orc's gold amount
            gold += 10
        elif enemy_type_for_messages == "zombie":
             web_print('The zombie died! +5 gold')
             gold += 5
             # Original had chance for zombie to not be cleared from grid,
             # simplified here to always clear. Re-add if important.
        prompt_for_action() # Back to exploration
        return

    # If battle continues (enemy not dead, player not fled, player not dead)
    if battle_active: # Redundant check, but good for clarity
        # Enemy attacks (if player didn't run or die, and enemy not dead)
        # This part was implicit in original as it would loop back. Here it's one turn.
        # For simplicity, the enemy's attack is part of the player's "failed to decide" or "bare hands" logic above.
        # If we want a distinct enemy turn after player acts, more logic here.
        # For now, the prompt for next battle action handles the loop.

        o_str = str(enemyhealth)
        web_print(f'The {enemy_type_for_messages} has {o_str}/{enemyhealthstart} health left.')
        web_input_prompt(f"{player_name} vs {enemy_type_for_messages}: attack, blaze flame, bolt strike, run?", handle_battle_action)


def start_battle(enemy_name_prompt, initial_hp, original_battle_func):
    global battle_active, enemyhealth, enemyhealthstart, battle_enemy_func, battle_enemy_name_for_prompt
    battle_active = True
    enemyhealth = initial_hp
    enemyhealthstart = str(initial_hp)
    battle_enemy_func = original_battle_func # Not used currently, but good for future ref
    battle_enemy_name_for_prompt = enemy_name_prompt
    web_print(f"{player_name} encountered a {enemy_name_prompt}:")
    web_input_prompt(f"What will {player_name} do? (attack, blaze flame, bolt strike, run)", handle_battle_action)


# Original battle functions are now just initiators
def orcbattle():
    start_battle("orc", int(enemyhealthstart), orcbattle) # enemyhealthstart would be set before calling

def bigorcbattle(): # Assuming 'big orc' is still an orc mechanically but with more HP
    start_battle("big orc", int(enemyhealthstart), bigorcbattle)

def spiderbattle():
    start_battle("giant spider", int(enemyhealthstart), spiderbattle)

def zombiebattle():
    start_battle("zombie", int(enemyhealthstart), zombiebattle)


def look_check(direction_text): # Renamed direction
    # Temporarily move to check, then move back.
    # This assumes look_check is only called when a move is possible OR if checking current tile (direction_text empty)
    # For simplicity with web_print, we'll just print what's there.
    # A more complex version would store temp_x, temp_y
    
    target_x, target_y = x_coord, y_coord
    valid_look = True

    if "north" in direction_text:
        if y_coord > 0: target_y -=1
        else: valid_look = False
    elif "south" in direction_text:
        if y_coord < len(grid) - 1: target_y +=1
        else: valid_look = False
    elif "west" in direction_text:
        if x_coord > 0: target_x -=1
        else: valid_look = False
    elif "east" in direction_text:
        if x_coord < len(grid[0]) - 1 : target_x +=1 # Assuming grid[0] exists
        else: valid_look = False
    # else: it's looking at the current spot if direction_text is empty, or "look around"

    if not valid_look or (not grid) or not (0 <= target_y < len(grid)) or not (0 <= target_x < len(grid[0])):
        web_print("Saw a brick wall " + direction_text if direction_text else "Can't see anything there.")
        return

    tile_val = grid[target_y][target_x]
    description = "Saw "
    if tile_val == 1: description += "a safe path"
    elif tile_val == 0: description += "a trap"
    elif tile_val == 2: description += "treasure (the exit!)"
    elif tile_val == 3: description += "an orc"
    elif tile_val == 9: description += "a big orc"
    elif tile_val == 4: description += "some pancakes"
    elif tile_val == 5: description += "a sword"
    elif tile_val == 6: description += "armor"
    elif tile_val == 7: description += "a brick wall"
    elif tile_val == 10: description += "a giant spider"
    elif tile_val == 8: description += "a zombie"
    elif tile_val == 11: description += "a chest"
    elif tile_val == 12: description += "a fire magic book"
    elif tile_val == 13: description += "a lightning magic book"
    elif tile_val == 14: description += "a map"
    else: description += "something mysterious"
    
    web_print(description + (" " + direction_text if direction_text else ""))


def explore(direction_command): # Renamed from 'direction'
    global player_name, gold, y_coord, x_coord, health, weaponcount, armor
    global enemyhealth, enemyhealthstart, firebook, lightningbook, mana, game_map, grid

    if game_is_over: return

    if mana < 30:
        mana += 1
        web_print('(1 mana restored)')

    original_x, original_y = x_coord, y_coord # Store current position

    action_taken = False
    if direction_command == '': # From original code, chance to spawn spider if "" is entered
        chance = random.randint(0, 100)
        if chance > 90 and grid[y_coord][x_coord] == 1: # Only on empty space
            web_print("A giant spider suddenly drops from the ceiling!")
            grid[y_coord][x_coord] = 10 # Change current tile to spider
            # Fall through to tile interaction check
        else:
            web_print("You wait a moment.")
            action_taken = True # Considered an action of waiting

    # Movement
    elif direction_command in ['go north', 'walk north', 'north', 'up', 'walk up', 'go up']:
        if y_coord > 0:
            if grid[y_coord - 1][x_coord] != 7: y_coord -= 1; action_taken = True
            else: web_print('Hit a wall. Cant go north.')
        else: web_print('Hit the edge of the map. Cant go north.')
    elif direction_command in ['go south', 'walk south', 'south', 'down', 'walk down', 'go down']:
        if y_coord < len(grid) - 1:
            if grid[y_coord + 1][x_coord] != 7: y_coord += 1; action_taken = True
            else: web_print('Hit a wall. Cant go south.')
        else: web_print('Hit the edge of the map. Cant go south.')
    elif direction_command in ['go west', 'walk west', 'west', 'left', 'walk left', 'go left']:
        if x_coord > 0:
            if grid[y_coord][x_coord - 1] != 7: x_coord -= 1; action_taken = True
            else: web_print('Hit a wall. Cant go west.')
        else: web_print('Hit the edge of the map. Cant go west.')
    elif direction_command in ['go east', 'walk east', 'east', 'right', 'walk right', 'go right']:
        if x_coord < len(grid[0]) - 1: # Assuming grid[0] exists if grid does
            if grid[y_coord][x_coord + 1] != 7: x_coord += 1; action_taken = True
            else: web_print('Hit a wall. Cant go east.')
        else: web_print('Hit the edge of the map. Cant go east.')
    
    # Look commands
    elif direction_command in ['look north', 'check north', 'look up', 'check up']:
        look_check('north'); action_taken = True
    elif direction_command in ['look south', 'check south', 'look down', 'check down']:
        look_check('south'); action_taken = True
    elif direction_command in ['look west', 'check west', 'look left', 'check left']: # 'check right' was a typo
        look_check('west'); action_taken = True
    elif direction_command in ['look east', 'check east', 'look right', 'check right']: # 'check right'
        look_check('east'); action_taken = True
    elif direction_command in ['look', 'check']:
        web_print(player_name + ' looks around.')
        look_check('north')
        look_check('south')
        look_check('west')
        look_check('east')
        action_taken = True
        
    # Other commands
    elif direction_command in ['check map', 'map']:
        if game_map < 1:
            web_print(player_name + ' does not have a map.')
        else:
            map_display = "--- MAP ---<br>"
            for r_idx, row in enumerate(grid):
                row_str = []
                for c_idx, cell in enumerate(row):
                    if r_idx == y_coord and c_idx == x_coord:
                        row_str.append("@") # Player position
                    elif cell == 7: # Wall
                        row_str.append("#")
                    elif cell == 2 and game_map > 1 : # Endgame, requires more map items to reveal?
                        row_str.append("X") # Reveal exit if good map
                    else: # Other tiles
                        row_str.append(".")
                map_display += " ".join(row_str) + "<br>"
            map_display += "-----------<br>@: You, #: Wall, X: Exit (if known)"
            web_print(map_display)
        action_taken = True

    elif direction_command in ['check stats', 'stats']:
        w_str = str(weaponcount)
        h_str = str(health)
        a_str = str(armor)
        g_str = str(gold)
        m_str = str(mana)
        web_print('_____________________________')
        web_print(f'Name: {player_name}\nClass: {player_class}\nHealth: {h_str}\nMana: {m_str}\nSwords: {w_str}\nArmor: {a_str}\nGold: {g_str}')
        # Simplified ASCII art for web, or remove if too messy
        if armor > 0 and weaponcount > 0: web_print(r' \ O /<br>--|--<br> / \ ')
        elif weaponcount > 0: web_print(r' \ O /<br>  |  <br> / \ ')
        elif armor > 0: web_print(r'   O  <br>--(+)--<br>  / \ ')
        else: web_print(r'  O  <br>  |  <br> / \ ')

        if firebook >= 1: web_print("Has Fire Magic Book (blaze flame)")
        if lightningbook >= 1: web_print("Has Lightning Magic Book (bolt strike)")
        web_print('_____________________________')
        action_taken = True
        
    elif direction_command == 'help':
        web_print("Available commands:")
        web_print("- go [north, south, east, west] (or just direction e.g. 'north')")
        web_print("- look [north, south, east, west] (or just 'look')")
        web_print("- stats")
        web_print("- map (if you have one)")
        web_print("- open chest (if you are on a chest tile and prompted)")
        web_print("During battle: attack, blaze flame, bolt strike, run")
        action_taken = True

    else:
        if not action_taken: # If no specific command matched and wasn't a move attempt that failed at boundary
            web_print("Unknown command. Type 'help' for options.")
            # No change in position if command is unknown

    # Check for tile interaction AFTER movement or action
    if action_taken and (original_x != x_coord or original_y != y_coord): # Player moved
        web_print(f"Moved to ({x_coord}, {y_coord})")
    
    # Tile interaction logic
    current_tile = grid[y_coord][x_coord]
    # web_print(f"DEBUG: On tile {current_tile} at ({x_coord},{y_coord})") # For debugging

    if current_tile == 1: # Nothing
        if action_taken and (original_x != x_coord or original_y != y_coord): # only print if moved to empty
             web_print(player_name + ' encounters nothing here.')
    elif current_tile == 0: # Trap
        damage_taken = max(0, 10 - armor)
        health -= damage_taken
        web_print(player_name + ' fell in a trap! -' + str(damage_taken) + 'hp')
        if armor > 0:
            web_print('Armor protected ' + str(min(10, armor)) + ' hp.')
        grid[y_coord][x_coord] = 1 # Trap sprung, becomes normal floor
    elif current_tile == 4: # Pancakes
        web_print(player_name + ' found pancakes! +10hp')
        health += 10
        grid[y_coord][x_coord] = 1
    elif current_tile == 5: # Sword
        weaponcount += 1
        web_print(player_name + ' picked up a sword.')
        grid[y_coord][x_coord] = 1
    elif current_tile == 6: # Armor
        armor += 1
        web_print(player_name + ' found armor.')
        grid[y_coord][x_coord] = 1
    elif current_tile == 12: # Fire magic book
        web_print(player_name + ' found a fire magic book!\nYou can now use "blaze flame" (3mp) in combat.')
        firebook += 1
        grid[y_coord][x_coord] = 1
    elif current_tile == 13: # Lightning magic book
        web_print(player_name + ' found a lightning magic book!\nYou can now use "bolt strike" (15mp) in combat.')
        lightningbook += 1
        grid[y_coord][x_coord] = 1
    elif current_tile == 14: # Map
        web_print(player_name + ' found a map!')
        game_map += 1
        grid[y_coord][x_coord] = 1
        
    # Enemies and Chest - these initiate new input prompts
    elif current_tile == 3: # Orc
        enemyhealthstart = '3' # Set before calling battle
        orcbattle() # This will set battle_active and prompt for input
        return # Battle handles its own input loop
    elif current_tile == 9: # Big Orc
        enemyhealthstart = '10'
        bigorcbattle()
        return
    elif current_tile == 10: # Giant Spider
        enemyhealthstart = '5'
        spiderbattle()
        return
    elif current_tile == 8: # Zombie
        enemyhealthstart = '7'
        zombiebattle()
        return
    elif current_tile == 11: # Chest
        web_input_prompt(player_name + ' found a chest. Do you want to open it? (yes/no)', handle_chest_open)
        return # Wait for chest input

    elif current_tile == 2: # Endgame
        g_str = str(gold)
        web_print(f'Congratulations, {player_name}! You found the exit and recovered {g_str} gold!')
        game_over_web()
        return

    # Check health after all actions
    if health <= 0 and not game_is_over:
        h_str = str(health)
        web_print(f'You have {h_str} health left. YOU LOSE')
        game_over_web()
        return

    # If not in battle and game not over, prompt for next exploration action
    if not battle_active and not game_is_over:
        prompt_for_action()

def handle_chest_open(yesno):
    global grid, y_coord, x_coord
    # Corrected logic for 'yesno'
    if yesno.lower() in ['yes', 'y', 'i do', 'open', 'ok']:
        chest() # chest() now modifies grid[y][x]
    else:
        web_print(player_name + ' does not open the chest.')
        # grid[y_coord][x_coord] remains 11 (chest) if not opened.
        # Or, you might want it to become 1 (empty) if they choose not to open it and can't re-open.
        # For now, it remains a chest.
    
    # After handling chest, go back to exploration prompt
    if not battle_active and not game_is_over:
        prompt_for_action()


# --- Game Setup and Main Loop Control ---
setup_step = 0

def process_setup_input(text_input):
    global setup_step, player_name, player_class, map_size_choice, weaponcount, armor, game_initialized

    if setup_step == 0:
        player_name = text_input.strip()
        if not player_name: player_name = "Adventurer" # Default name
        web_print(f"Welcome, {player_name}!")
        setup_step = 1
        web_input_prompt('Pick a class:\n1. Rogue (2 swords)\n2. Warrior (1 sword, 1 armor)\n3. Paladin (2 armor)', process_setup_input)
    elif setup_step == 1:
        choice = text_input.strip()
        if choice == '1':
            player_class = 'Rogue'
            weaponcount += 2
        elif choice == '2':
            player_class = 'Warrior'
            weaponcount += 1
            armor += 1
        elif choice == '3':
            player_class = 'Paladin'
            armor += 2
        else:
            web_print("Invalid class choice. Defaulting to Warrior.")
            player_class = 'Warrior'
            weaponcount += 1
            armor += 1
        web_print(f"You are a {player_class}.")
        setup_step = 2
        web_input_prompt('Choose map size: big, small, or random', process_setup_input)
    elif setup_step == 2:
        map_size_choice = text_input.strip().lower()
        if map_size_choice not in ['big', 'small', 'random']:
            web_print("Invalid map size. Defaulting to random.")
            map_size_choice = 'random'
        web_print(f"Map size: {map_size_choice}.")
        
        setup_grid() # Setup the grid based on choices
        display_intro_art()
        game_initialized = True
        prompt_for_action() # Start the game exploration

def prompt_for_action():
    if game_is_over: return
    web_input_prompt("What do you do next?", process_command_input)

def process_command_input(command_text):
    global game_initialized
    if game_is_over: return

    if not game_initialized:
        process_setup_input(command_text)
    elif battle_active: # Should be handled by battle_input_prompt, but as a fallback
        handle_battle_action(command_text.lower().strip())
    else:
        explore(command_text.lower().strip())


# Brython entry point / event handling
def handle_submit_button_click(event: DOMEvent):
    global current_input_callback
    if game_is_over: return

    command = input_field.value
    # web_print(f"<span style='color:gray'>>>> {command}</span>") # Echo command if desired
    input_field.value = "" # Clear input field

    if current_input_callback:
        # Temp store and clear callback in case the callback itself sets a new one
        callback_to_run = current_input_callback
        current_input_callback = None 
        callback_to_run(command)
    else:
        # This case should ideally not be reached if input logic is tight
        # but if it is, assume it's a general game command.
        process_command_input(command)


submit_button.bind("click", handle_submit_button_click)
input_field.bind("keypress", lambda ev: handle_submit_button_click(ev) if ev.keyCode == 13 else None)


# Start the game setup
web_input_prompt('Enter your name:', process_setup_input)
