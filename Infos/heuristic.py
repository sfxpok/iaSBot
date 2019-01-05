# search() - pesquisa?
# scout() - reconhecimento das zonas à volta do chappie

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
ZombieValue = 40
danger1Value = 1
danger2Value = 2
danger3Value = 3
danger4Value = 4

smellValues = {
    'Green': 0, # there is no danger
    'Yellow': danger1Value,
    'Red': danger2Value,
    'Blue': danger3Value,
    'Brown': danger4Value
}
zombieValues = {
    'Green': 0, # there is no zombie
    'Yellow': ZombieValue,
    'Red': ZombieValue,
}
pieceValues = {
    'Green': 0, # there are no pieces
    'Yellow': pieceValue,
    'Red': bulletValue
}

lastTurnSmell = 0

def listActions():
    if lastTurnSmell == 0:
        search()
        scout()
    else:
        scout()
        zombiesDirections = whereZombie()
        if zombiesDirections[0] != [] or zombiesDirections[1] != []:
            attack(zombiesDirections)
        search()

def attack(zombiesDirections):
    if zombiesDirections[0] != []:
        setDirection(zombiesDirections[0][0])
    else:
        setDirection(zombiesDirections[1])
    if hasBullet == True:
        shoot()
    else:
        punch()


def whereZombie(itemsAround=0):
    #Esta funcao recebe o array de items da funcao reconhecimento

    directions = {
        0: 'North',
        1: 'East',
        2: 'South',
        3: 'West'
    }

    arrayZombiesDirections = [[],[]]

    for i in range(4):
        direction = directions[i]
        zombieColor = itemsAround[direction][1]
        if zombieColor == 'Yellow':
            arrayZombiesDirections[0].append(direction)
        elif zombieColor == 'Red':
            arrayZombiesDirections[1].append(direction)
    
    return arrayZombiesDirections

def saveSmell(colorsValues):
    #colorsValues[0]-->SmellNorth
    #colorsValues[1]-->SmellEast
    #colorsValues[2]-->SmellSouth
    #colorsValues[3]-->SmellWest

def addItemsToValues(itemsAround=None):

    if itemsAround == None:
        return [0,0,0]

    counter = 1
    addValues = []
    colorsValues = []

    for direction in itemsAround:
        for color in direction:
            directionValue = 0
            if counter == 1:
                colorValue = smellValues[color]
                directionValue += colorValue
                colorsValues.append(colorValue)
            elif counter == 2:
                directionValue += zombieValues[color]
            elif counter == 3:
                directionValue += zombieValues[color]
        counter += 1
        addValues.append(directionValue)

    lastTurnSmell = saveSmell(colorsValues)
    
    return addValues
    
def bestNextHouse(itemsAround=None):
    addValues = addItemsToValues(itemsAround)

    north = realValuesMap[currentX][currentY-1] + heurValueMap[currentX][currentY-1]+addValues[0]
    east = realValuesMap[currentX+1][currentY] + heurValueMap[currentX+1][currentY]+addValues[1]
    south = realValuesMap[currentX][currentY+1] + heurValueMap[currentX][currentY+1]+addValues[2]
    west = realValuesMap[currentX-1][currentY] + heurValueMap[currentX-1][currentY]+addValues[3]

    min = north # min is the shortest path
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
    targetHouse = bestNextHouse() #Inserir nesta funçao o array das cores
    move(targetHouse)