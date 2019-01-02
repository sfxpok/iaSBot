
gameMap = [[None for col in range(6)] for row in range(6)] # empty matrix of size 6x6

realValuesMap = [[10,9,8,7,6,5],
                [9,8,7,6,5,4],
                [8,7,6,5,4,3],
                [7,6,5,4,3,2],
                [6,5,4,3,2,1],
                [5,4,3,2,1,0]]

heurValueMap = [[30,6,6,6,6,30],
                [4,2,2,2,2,4],
                [4,2,3,3,2,4],
                [4,2,3,3,2,4],
                [4,2,2,2,2,4],
                [30,6,6,6,6,0]]

bulletValue = -10
pieceValue = -15
checkedHouseValue = 1
ZombieValue = 20
danger1Value = 1
danger2Value = 2
danger3Value = 3
danger4Value = 4


def listActions():
    if perigo == 0:
        search()
        scout()
    if perigo == 1:
        search()
        scout()
        if nextToZombie():
            attack(zombie_position) 
    if perigo == 2:
        scout()
        if nextToZombie():
            attack(zombie_position)
            search()
    if perigo == 3:
        scout()
        attack(zombie_position)
        search()
    if perigo == 4:
        scout()
        attack(zombie_position)
        search()

def attack(zombie_position):
    setDirection(zombie_position)
    if bullet:
        shoot()
    else:
        punch()

def nextToZombie():
    return (existZombie(curentX+1,currentY+1) or
        existZombie(curentX+1,currentY-1) or
        existZombie(curentX-1,currentY+1) or
        existZombie(curentX-1,currentY-1))

def existZombie(targetX, targetY):
    

def addItemsToValues(itemsAround=None):
    # bulletValue = -10
    # pieceValue = -15
    # checkedHouseValue = 1 Acrescentar depois de movimento
    # ZombieValue = 40
    # danger1Value = 1
    # danger2Value = 2
    # danger3Value = 3
    # danger4Value = 4

    #Colors:
    #Cheiro: Vermelho, Amarelo, Azul, Castanho
    #Zombie: Vermelho, Castanho
    #Peça: Azul, Verde

    if itemsAround == None:
        return [0,0,0]

    smellValues = {
        'White': 0,
        'Red': 1,
        'Yellow': 2,
        'Blue': 3,
        'Brown': 4
    }
    zombieValues = {
        'White': 0,
        'Red': 40,
        'Brown': 40,
    }
    pieceValues = {
        'White': 0,
        'Blue': -15,
        'Green': -10
    }

    counter = 1
    addValues = []

    for direction in itemsAround:
        for color in direction:
            colorsValues = []
            if counter == 1:
                colorsValues.append(smellValues[color])
            elif counter == 2:
                colorsValues.append(zombieValues[color])
            elif counter == 3:
                colorsValues.append(pieceValues[color])
        counter += 1
        addValues.append(colorsValues)
    
    return addValues
    

def nextHouse(itemsAround=None):
    addValues = addItemsToValues(itemsAround)

    north = realValuesMap[currentX][currentY-1] + heurValueMap[currentX][currentY-1]+addValues[0]
    east = realValuesMap[currentX+1][currentY] + heurValueMap[currentX+1][currentY]+addValues[1]
    south = realValuesMap[currentX][currentY+1] + heurValueMap[currentX][currentY+1]+addValues[2]
    west = realValuesMap[currentX-1][currentY] + heurValueMap[currentX-1][currentY]+addValues[3]

    min = north
    targetHouse = 'North'

    if min > east:
        min = east
        targetHouse = 'East'
    if min > south:
        min = south
        targetHouse = 'South'
    if min > west:
        min = west
        targetHouse = 'West'
    return targetHouse

def search():
    targetHouse = nextHouse() #Inserir nesta funçao o array das cores
    move(targetHouse)