import random
import sys

x = random.randint(0, 9)
y = random.randint(0, 9)

map = 0
gold = 0
health = 100
mana = 30
armor = 0
weaponcount = 0
firebook = 0
lightningbook = 0
enemyhealth = 0
enemyhealthstart = '3'
name = input('enter your name: ')
clas = input('Pick a class:\n1. rogue 2 swords\n2. warrior 1 sword 1 armor\n3. paladin 2 armor\n')
size = input('big, small or random size map: ')
if clas == '1':
    clas = 'rogue'
    weaponcount += 2
if clas == '2':
    clas = 'warrior'
    weaponcount += 1
    armor += 1
if clas == '3':
    clas = 'paladin'
    armor += 2

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

if size == 'random':
    o = random.randint(5, 30)
    p = random.randint(5, 30)
    grid = [[random.randint(0, 15) for j in range(o)] for i in range(p)]


    def remove_extra_twos(grid):
        two_count = 0
        for row in grid:
            two_count += row.count(2)

        if two_count > 1:
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] == 2:
                        grid[i][j] = random.randint(0, 15)
                        two_count -= 1
                        if two_count == 1:
                            break
                if two_count == 1:
                    break


    grid[random.randint(0, 9)][random.randint(0, 9)] = 2
    remove_extra_twos(grid)



else:

    if size == 'big':
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

    elif size == 'small':
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
    else:
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

if size == 'test':
    x = 0
    y = 0
    grid = [[8, 14, 11, 11, 11, 11, 11, 10, 2],
            [1, 3, 4, 5, 6, 7, 8]]

print(r"""\
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

print('You are an explorer in search of gold. You enter the ominous looking castle and the door locks behind you. '
      'Now you must decide what to do....\n\n\nenter help for options')


def chest():
    global name
    global gold
    global y
    global x
    global health
    global weaponcount
    global armor
    global enemyhealth
    global enemyhealthstart
    global firebook
    global lightningbook
    global mana
    global map
    chance = random.randint(0, 6)
    if chance == 6:
        print(name + ' found a map')
        map += 1
    grid[y][x] = 1
    if chance == 4:
        print(name + ' found a fire magic book in the chest\nyou can now use blaze flame when fighting enemies')
        firebook += 1
        print(r"""\
                           __..._   _...__
                      _..-"      `Y`      "-._
                      \ Blaze     |           /
                      \\  Flame   |          //
                      \\\    3 mp |         ///
                       \\\ _..---.|.---.._ ///
                        \\`_..---.Y.---.._`//
                         '`               `'
                                    """)
        grid[y][x] = 1
    if chance == 5:
        print(name + ' found a lightning magic book in the chest\nyou can now use bolt strike when fighting enemies')
        lightningbook += 1
        print(r"""\
                           __..._   _...__
                      _..-"      `Y`      "-._
                      \ Bolt      |           /
                      \\  Strike  |          //
                      \\\   15 mp |         ///
                       \\\ _..---.|.---.._ ///
                        \\`_..---.Y.---.._`//
                         '`               `'
                                    """)
        grid[y][x] = 1
    if chance == 0:
        health -= (10 - armor)
        print(name + ' the chest was a trap -' + str(10 - armor) + 'hp')
        armors = str(armor)
        if armor > 0:
            print('armor protected ' + armors + ' hp')
        grid[y][x] = 1
    if chance == 1:
        print(name + ' found pancakes in the chest +10hp')
        health += 10
        grid[y][x] = 1
    if chance == 2:
        weaponcount += 1
        grid[y][x] = 1
        print(name + ' found a sword in the chest')
    if chance == 3:
        armor += 1
        grid[y][x] = 1
        print(name + ' found armor in the chest')


def orcbattle():
    global name
    global gold
    global y
    global x
    global health
    global weaponcount
    global armor
    global enemyhealth
    global enemyhealthstart
    global firebook
    global lightningbook
    global mana
    if health <= 0:
        h = str(health)
        print('you have ' + h + ' health left YOU LOSE')
        sys.exit(0)
    fight = input(name + ' encountered an orc: \nattack\nrun\n')
    if fight == "blaze flame" and firebook >= 1 and mana > 2:
        enemyhealth -= 3
        print(name + ' uses fire magic to burn orc it takes 3 damage\n')
        mana -= 3
        m = str(mana)
        print('remaining mana ' + m + '/30')
    if fight == "blaze flame" and firebook < 1:
        print(name + ' does not know fire magic')
    if fight == "bolt strike" and lightningbook >= 1 and mana > 10:
        enemyhealth -= 10
        print(name + ' uses lightning magic to electrocute orc it takes 10 damage\n')
        mana -= 15
        m = str(mana)
        print('remaining mana ' + m + '/30')
    if fight == "bolt strike" and lightningbook < 1:
        print(name + ' does not know lightning magic')
    if fight == "attack" and weaponcount < 1:
        chance = random.randint(0, 2)
        if chance > 1:
            health -= (20 - armor)
            armors = str(armor)
            if armor > 0:
                print('armor protected ' + armors + ' hp')
            print(name + ' got hit by orc\n-' + str(20 - armor) + 'hp')

        else:
            health -= (10 - armor)
            enemyhealth -= 1
            print('orc punches ' + name + ' -' + str(10 - armor) + 'hp')
            armors = str(armor)
            if armor > 0:
                print('armor protected ' + armors + ' hp')
            print(name + ' punches orc it takes 1 damage')
    if fight == 'attack' and weaponcount >= 1:
        chance = random.randint(0, 2)
        if chance == 0:
            weaponcount -= 1
            enemyhealth -= 2
            print(name + ' used a sword it breaks and the orc takes 2 damage ')
        else:
            enemyhealth -= 2
            print(name + ' used a sword the orc takes 2 damage ')
    if fight != 'attack' and fight != 'run' and fight != 'blaze flame' and fight != "bolt strike":
        health -= (20 - armor)
        print('failed to decide -' + str(20 - armor) + 'hp')
        armors = str(armor)
        if armor > 0:
            print('armor protected ' + armors + ' hp')

    if fight == 'run':
        chance = random.randint(0, 2)
        if chance > 1:
            health -= (20 - armor)
            print(name + ' got hit while running -' + str(20 - armor) + 'hp')
            armors = str(armor)
            if armor > 0:
                print('armor protected ' + armors + ' hp')
        else:
            print(name + ' escaped successfully')
    if enemyhealth <= 0 and fight != 'run':
        if enemyhealth <= 0:
            grid[y][x] = 1
            print('the orc died +10 gold')
            gold += 10
    if enemyhealth > 0 and fight != 'run':
        o = str(enemyhealth)
        print('the orc has ' + o + '/' + enemyhealthstart + ' health left')
        orcbattle()

    else:
        explore()


def spiderbattle():
    global name
    global gold
    global y
    global x
    global health
    global weaponcount
    global armor
    global enemyhealth
    global enemyhealthstart
    global firebook
    global lightningbook
    global mana
    if health <= 0:
        h = str(health)
        print('you have ' + h + ' health left YOU LOSE')
        sys.exit(0)
    fight = input(name + ' encountered a giant spider: \nattack\nrun\n')
    if fight == "blaze flame" and firebook >= 1:
        enemyhealth -= 3
        print(name + ' uses fire magic to burn the spider it takes 3 damage\n')
        mana -= 3
        m = str(mana)
        print('remaining mana ' + m + '/30')
    if fight == "blaze flame" and firebook < 1:
        print(name + ' does not know fire magic')
    if fight == "bolt strike" and lightningbook >= 1 and mana > 10:
        enemyhealth -= 10
        print(name + ' uses lightning magic to electrocute the spider it takes 10 damage\n')
        mana -= 15
        m = str(mana)
        print('remaining mana ' + m + '/30')
    if fight == "bolt strike" and lightningbook < 1:
        print(name + ' does not know lightning magic')
    if fight == "attack" and weaponcount < 1:
        chance = random.randint(0, 2)
        if chance > 1:
            health -= (20 - armor)
            armors = str(armor)
            if armor > 0:
                print('armor protected ' + armors + ' hp')
            print(name + ' got bit by the spider\n-' + str(20 - armor) + 'hp')
        else:
            health -= (10 - armor)
            enemyhealth -= 1
            print('spider bites ' + name + ' -' + str(10 - armor) + 'hp')
            armors = str(armor)
            if armor > 0:
                print('armor protected ' + armors + ' hp')
            print(name + ' punches spider it takes 1 damage')
    if fight == 'attack' and weaponcount >= 1:
        chance = random.randint(0, 2)
        if chance == 0:
            weaponcount -= 1
            enemyhealth -= 2
            print(name + ' used a sword it breaks and the spider takes 2 damage ')
        else:
            enemyhealth -= 2
            print(name + ' used a sword the spider takes 2 damage ')
    if fight != 'attack' and fight != 'run' and fight != 'blaze flame' and fight != "bolt strike":
        health -= (20 - armor)
        print('failed to decide -' + str(20 - armor) + 'hp')
        armors = str(armor)
        if armor > 0:
            print('armor protected ' + armors + ' hp')

    if fight == 'run':
        chance = random.randint(0, 2)
        if chance > 1:
            health -= (20 - armor)
            print(name + ' got hit while running -' + str(20 - armor) + 'hp')
            armors = str(armor)
            if armor > 0:
                print('armor protected ' + armors + ' hp')
        else:
            print(name + ' escaped successfully')
    if enemyhealth <= 0 and fight != 'run':
        if enemyhealth <= 0:
            grid[y][x] = 1
            print('the spider died +10 gold')
            gold += 10

    if enemyhealth > 0 and fight != 'run':
        o = str(enemyhealth)
        print('the spider has ' + o + '/' + enemyhealthstart + ' health left')
        spiderbattle()

    else:
        explore()


def zombiebattle():
    global name
    global gold
    global y
    global x
    global health
    global weaponcount
    global armor
    global enemyhealth
    global enemyhealthstart
    global firebook
    global lightningbook
    global mana
    if health <= 0:
        h = str(health)
        print('you have ' + h + ' health left YOU LOSE')
        sys.exit(0)
    fight = input(name + ' encountered a zombie: \nattack\nrun\n')
    fire = 1
    if fight == "blaze flame" and firebook >= 1:
        fire = 0
        enemyhealth -= 3
        print(name + ' uses fire magic to burn zombie it takes 3 damage and cannot regenerate\n')
        mana -= 3
        m = str(mana)
        print('remaining mana ' + m + '/30')
    if fight == "blaze flame" and firebook < 1:
        print(name + ' does not know fire magic')
    if fight == "bolt strike" and lightningbook >= 1 and mana > 10:
        enemyhealth -= 10
        print(name + ' uses lightning magic to electrocute zombie it takes 10 damage\n')
        mana -= 15
        m = str(mana)
        print('remaining mana ' + m + '/30')
    if fight == "bolt strike" and lightningbook < 1:
        print(name + ' does not know lightning magic')
    if fight == "attack" and weaponcount < 1:
        chance = random.randint(0, 2)
        if chance > 1:
            health -= (10 - armor)
            armors = str(armor)
            if armor > 0:
                print('armor protected ' + armors + ' hp')
            print(name + ' got bit by the zombie\n-' + str(10 - armor) + 'hp')

        else:
            health -= (5 - armor)
            enemyhealth -= 1
            print('zombie bites ' + name + ' -' + str(5 - armor) + 'hp')
            armors = str(armor)
            if armor > 0:
                print('armor protected ' + armors + ' hp')
            print(name + ' punches zombie it takes 1 damage')
    if fight == 'attack' and weaponcount >= 1:
        chance = random.randint(0, 2)
        if chance == 0:
            weaponcount -= 1
            enemyhealth -= 2
            print(name + ' used a sword it breaks and the zombie takes 2 damage ')
        else:
            enemyhealth -= 2
            print(name + ' used a sword the zombie takes 2 damage ')
    if fight != 'attack' and fight != 'run' and fight != 'blaze flame' and fight != "bolt strike":
        health -= (10 - armor)
        print('failed to decide -' + str(10 - armor) + 'hp')
        armors = str(armor)
        if armor > 0:
            print('armor protected ' + armors + ' hp')

    if fight == 'run':
        chance = random.randint(0, 2)
        if chance > 1:
            health -= (10 - armor)
            print(name + ' got hit while running -' + str(10 - armor) + 'hp')
            armors = str(armor)
            if armor > 0:
                print('armor protected ' + armors + ' hp')
        else:
            print(name + ' escaped successfully')
    if enemyhealth <= 0 and fight != 'run':
        if enemyhealth <= 0:
            chance = random.randint(0, 100)
            if chance > 50:
                grid[y][x] = 1
            if fire == 0:
                grid[y][x] = 1
            print('the zombie died +5 gold')
            gold += 5

    if enemyhealth > 0 and fight != 'run':
        o = str(enemyhealth)
        print('the zombie has ' + o + '/' + enemyhealthstart + ' health left')
        zombiebattle()

    else:
        explore()


def lookcheck(direction):
    if grid[y][x] == 1:
        print("saw a safe path " + direction)
    if grid[y][x] == 0:
        print("saw a trap " + direction)
    if grid[y][x] == 2:
        print("saw treasure " + direction)
    if grid[y][x] == 3:
        print("saw a orc " + direction)
    if grid[y][x] == 9:
        print("saw a big orc " + direction)
    if grid[y][x] == 4:
        print("saw some pancakes " + direction)
    if grid[y][x] == 5:
        print("saw a sword " + direction)
    if grid[y][x] == 6:
        print("saw armor " + direction)
    if grid[y][x] == 7:
        print("saw a brick wall " + direction)
    if grid[y][x] == 10:
        print(name + " saw a giant spider " + direction)
    if grid[y][x] == 8:
        print(name + " saw a zombie " + direction)
    if grid[y][x] == 14:
        print(name + " saw a map " + direction)


def explore():
    global name
    global gold
    global y
    global x
    global health
    global weaponcount
    global armor
    global enemyhealth
    global enemyhealthstart
    global firebook
    global lightningbook
    global mana
    global map

    if mana < 30:
        mana += 1
        print('1 mana restored')

    direction = input('enter a action: ')
    direction = direction.lower()
    if direction == '':
        chance = random.randint(0, 100)
        if chance > 90:
            grid[y][x] = 10
    if direction == 'look north' or direction == 'check north' or direction == 'look up' or direction == 'check up':
        if y > 0:
            y -= 1
            lookcheck('')
            y += 1
        else:
            print('saw a brick wall')
    if direction == 'look south' or direction == 'check south' or direction == 'look down' or direction == 'check down':
        if y < len(grid) - 1:
            y += 1
            lookcheck('')
            y -= 1
        else:
            print('saw a brick wall')
    if direction == 'look west' or direction == 'check west' or direction == 'look left' or direction == 'check right':
        if x > 0:
            x -= 1
            lookcheck('')
            x += 1
        else:
            print('saw a brick wall')
    if direction == 'look east' or direction == 'check east' or direction == 'look right' or direction == 'check right':
        if x < len(grid[y]) - 1:
            x += 1
            lookcheck('')
            x -= 1
        else:
            print('saw a brick wall')
    if direction == 'look' or direction == 'check':
        print(name + ' looks around')
        if y > 0:
            y -= 1
            lookcheck('north')
            y += 1
        else:
            print('saw a brick wall north')
        if y < len(grid) - 1:
            y += 1
            lookcheck('south')
            y -= 1
        else:
            print('saw a brick wall south')
        if x > 0:
            x -= 1
            lookcheck('west')
            x += 1
        else:
            print('saw a brick wall west')
        if x < len(grid[y]) - 1:
            x += 1
            lookcheck('east')
            x -= 1
        else:
            print('saw a brick wall east')
    if direction == 'go north' or direction == 'walk north' or direction == 'north' or direction == 'up' or direction == 'walk up' or direction == 'go up':
        if y > 0:
            y -= 1
            if grid[y][x] == 7:
                print('hit a wall cant go this way')
                y += 1
        else:
            print('hit a wall cant go this way')
    if direction == 'go south' or direction == 'walk south' or direction == 'south' or direction == 'down' or direction == 'walk down' or direction == 'go down':
        if y < len(grid) - 1:
            y += 1
            if grid[y][x] == 7:
                print('hit a wall cant go this way')
                y -= 1
        else:
            print('hit a wall cant go this way')
    if direction == 'go west' or direction == 'walk west' or direction == 'west' or direction == 'left' or direction == 'walk left' or direction == 'go left':
        if x > 0:
            x -= 1
            if grid[y][x] == 7:
                print('hit a wall cant go this way')
                x += 1
        else:
            print('hit a wall cant go this way')
    if direction == 'go east' or direction == 'walk east' or direction == 'east' or direction == 'right' or direction == 'walk right' or direction == 'go right':
        if x < len(grid[y]) - 1:
            x += 1
            if grid[y][x] == 7:
                print('hit a wall cant go this way')
                x -= 1
        else:
            print('hit a wall cant go this way')
    if direction == 'check map' or direction == 'map' and map < 1:
        print(name + ' does not have a map')
    if direction == 'check map' or direction == 'map' and map > 0:
        for i in grid:
            for j in i:
                if j == 7:
                    print('0', end=" ")
                else:
                    print('.', end=" ")
            print()
    if direction == 'check stats' or direction == 'stats':
        w = str(weaponcount)
        h = str(health)
        a = str(armor)
        g = str(gold)
        m = str(mana)
        print('_____________________________')
        print(
            'Name: ' + name + '\nClass: ' + clas + '\nHealth: ' + h + '\nMana: ' + m + '\nSwords: ' + w + '\narmor: ' + a + '\ngold: ' + g)
        if armor > 0 and weaponcount > 0:
            print('\n \    O\n _\|  |  }\n   M_/|\_|}\n      |  }\n     / \ ' + '\n   _/   \_')
        if armor == 0 and weaponcount > 0:
            print('\n \    O\n _\|  |   \n   M_/|\_| \n      |   \n     / \ ' + '\n   _/   \_')
        if armor > 0 and weaponcount == 0:
            print('\n      O\n      |  }\n    _/|\_|}\n      |  }\n     / \ ' + '\n   _/   \_')
        if armor == 0 and weaponcount == 0:
            print('\n      O\n      |   \n    _/|\_| \n      |   \n     / \ ' + '\n   _/   \_')
        if firebook >= 1:
            print(r"""\
                   __..._   _...__
              _..-"      `Y`      "-._
              \ Blaze     |           /
              \\  FLame   |          //
              \\\    3 mp |         ///
               \\\ _..---.|.---.._ ///
                \\`_..---.Y.---.._`//
                 '`               `'
                            """)
        if lightningbook >= 1:
            print(r"""\
                   __..._   _...__
              _..-"      `Y`      "-._
              \ bolt      |           /
              \\  strike  |          //
              \\\   15 mp |         ///
               \\\ _..---.|.---.._ ///
                \\`_..---.Y.---.._`//
                 '`               `'
                                        """)
        print('_____________________________')
    if direction == 'check swords':
        w = str(weaponcount)
        print('you have ' + w + ' swords')
    if direction == 'check health':
        h = str(health)
        print('you have ' + h + ' hp')
    if direction == 'check mana':
        m = str(mana)
        print('you have ' + m + ' mana')
    if direction == 'check armor':
        a = str(armor)
        print('you have ' + a + ' armor')
    if direction == 'check gold':
        g = str(gold)
        print('you have ' + g + ' gold')
    if direction == 'help':
        print(
            'go "direction"\nwalk "direction"\ncheck health\ncheck mana\ncheck swords\ncheck armor\ncheck gold\nlook "direction"\nlook\ncheck "direction"\ncheck\ncheck stats\nstats\ncheck map\nmap\n')
    if grid[y][x] == 12:
        print(name + ' found a fire magic book\nyou can now use blaze flame when fighting enemies')
        firebook += 1
        print(r"""\
                           __..._   _...__
                      _..-"      `Y`      "-._
                      \ Blaze     |           /
                      \\  Flame   |          //
                      \\\    3 mp |         ///
                       \\\ _..---.|.---.._ ///
                        \\`_..---.Y.---.._`//
                         '`               `'
                                    """)
        grid[y][x] = 1
    if grid[y][x] == 13:
        print(name + ' found a lightning magic book\nyou can now use bolt strike when fighting enemies')
        lightningbook += 1
        print(r"""\
                           __..._   _...__
                      _..-"      `Y`      "-._
                      \ Bolt      |           /
                      \\  Strike  |          //
                      \\\   15 mp |         ///
                       \\\ _..---.|.---.._ ///
                        \\`_..---.Y.---.._`//
                         '`               `'
                                    """)
        grid[y][x] = 1
    if grid[y][x] == 1:
        print(name + ' encounters nothing')
    if grid[y][x] == 0:
        health -= (10 - armor)
        print(name + ' fell in a trap -' + str(10 - armor) + 'hp')
        armors = str(armor)
        if armor > 0:
            print('armor protected ' + armors + ' hp')
        grid[y][x] = 1
    if grid[y][x] == 4:
        print(name + ' found pancakes +10hp')
        health += 10
        grid[y][x] = 1
    if grid[y][x] == 5:
        weaponcount += 1
        grid[y][x] = 1
        print(name + ' picked up a sword')
    if grid[y][x] == 6:
        armor += 1
        grid[y][x] = 1
        print(name + ' found armor')
    if grid[y][x] == 3:
        print('Found a orc')
        enemyhealth = 3
        enemyhealthstart = '3'
        orcbattle()
    if grid[y][x] == 9:
        print('Found a big orc')
        enemyhealth = 10
        enemyhealthstart = '10'
        orcbattle()
    if grid[y][x] == 10:
        print('Found a giant spider')
        enemyhealth = 5
        enemyhealthstart = '5'
        spiderbattle()
    if grid[y][x] == 8:
        print('Found a zombie')
        enemyhealth = 7
        enemyhealthstart = '7'
        zombiebattle()
    if grid[y][x] == 11:
        print(name + ' found a chest, do you want to open it?')
        yesno = input()
        if yesno == 'yes' or 'y' or 'I do' or 'open':
            chest()
        else:
            print(name + ' does not open the chest')
    if grid[y][x] == 14:
        print(name + ' found a map')
        map += 1
        grid[y][x] = 1
    return 0


def advent():
    global gold
    global health
    while grid[y][x] != 2:
        explore()
        if health <= 0:
            h = str(health)
            print('you have ' + h + ' health left YOU LOSE')
            break
    if grid == 2:
        g = str(gold)
        print('you found the exit and you recovered ' + g + ' gold')
    pass


advent()
