""" # scout() - fullRecognize()

gameMap = [[None for col in range(6)] for row in range(6)] # empty matrix of size 6x6

#Array com os valores reais do mapa
realValuesMap = [[10,9,8,7,6,5],
                [9,8,7,6,5,4],
                [8,7,6,5,4,3],
                [7,6,5,4,3,2],
                [6,5,4,3,2,1],
                [5,4,3,2,1,0]]

#Array com os valores heuristicos do mapa
heurValueMap = [[30,6,6,6,6,30],
                [4,2,2,2,2,4],
                [4,2,3,3,2,4],
                [4,2,3,3,2,4],
                [4,2,2,2,2,4],
                [30,6,6,6,6,0]]

# used values to calculate real/heur
# values during gameplay
bulletValue = -10
pieceValue = -15
checkedHouseValue = 1
ZombieValue = 40
danger1Value = 1
danger2Value = 2
danger3Value = 3
danger4Value = 4

#Valores heuristicos da tres cores de reconhecimento
#Valores da primeira cor
smellValues = {
    'Green': 0, # there is no danger
    'Yellow': danger1Value,
    'Red': danger2Value,
    'Blue': danger3Value,
    'Brown': danger4Value
}
#Valores da segunda cor
zombieValues = {
    'Green': 0, # there is no zombie
    'Yellow': ZombieValue, # 2 squares of distance
    'Red': ZombieValue, # 1 square of distance
}
#Valores da terceira cor
pieceValues = {
    'Green': 0, # there are no pieces
    'Yellow': pieceValue,
    'Red': bulletValue
}

self.lastTurnSmell = 0


#Lista da accoes que o robo deve fazer por turno dependendo do cheiro na sua casa no ultimo turno
def listActions():
    if self.lastTurnSmell == 0:
        search()
        self.fullRecognition()
    else:
        colorArray = self.fullRecognition()
        zombiesDirections = whereZombie()
        if zombiesDirections[0] != [] or zombiesDirections[1] != []: # are there zombies nearby?
            attack(zombiesDirections)
        search(colorArray)

#Attaque do robo. Se ele tiver a bala ele dispara, senao ele da o ataque de machete
def attack(zombiesDirections):
    if zombiesDirections[0] != []: # attack a zombie nearby
        setDirection(zombiesDirections[0][0]) # attack first zombie in the array
    else:
        setDirection(zombiesDirections[1][0]) # attack second zombie in the array
    if hasBullet == True:
        shoot()
    else:
        punch()


def whereZombie(itemsAround=0):
    #Esta funcao recebe o array de items da funcao reconhecimento

    # returns the position of nearby zombies (if they exist)

    directions = {
        0: 'North',
        1: 'East',
        2: 'South',
        3: 'West'
    }

    arrayZombiesDirections = [[],[]]

    # first list inside the array corresponds to yellow
    # second list inside the array corresponds to red

    for i in range(4):
        direction = directions[i]
        zombieColor = itemsAround[direction][1]
        if zombieColor == 'Yellow':
            arrayZombiesDirections[0].append(direction)
        elif zombieColor == 'Red':
            arrayZombiesDirections[1].append(direction)
    
    return arrayZombiesDirections

#Funcao que calcula o cheiro na sua casa usando o cheiro de casas adjacentes
def saveSmell(colorsValues):
    #colorsValues[0]-->SmellNorth
    #colorsValues[1]-->SmellEast
    #colorsValues[2]-->SmellSouth
    #colorsValues[3]-->SmellWest

    if ((colorsValues[0] >= 2 and colorsValues[1] >= 2) or
        (colorsValues[1] >= 2 and colorsValues[2] >= 2) or
        (colorsValues[2] >= 2 and colorsValues[3] >= 2) or
        (colorsValues[3] >= 2 and colorsValues[0] >= 2)):
        return 2    #Aqui o valor nao interessa, o importante e que nao seja 0
    else:
        return 0

#Devolve um array com os valores heuristicos correspondentes
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

    self.lastTurnSmell = saveSmell(colorsValues)
    
    return addValues

#Adiciona os valores heuristicos dos items as casas adjacentes e calcula a casa com menor valor
def bestNextHouse(itemsAround=None):
    addValues = addItemsToValues(itemsAround)

    north = realValuesMap[self.posX][self.posY-1] + heurValueMap[self.posX][self.posY-1]+addValues[0]
    east = realValuesMap[self.posX+1][self.posY] + heurValueMap[self.posX+1][self.posY]+addValues[1]
    south = realValuesMap[self.posX][self.posY+1] + heurValueMap[self.posX][self.posY+1]+addValues[2]
    west = realValuesMap[self.posX-1][self.posY] + heurValueMap[self.posXentX-1][self.posY]+addValues[3]

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

#Calcula a casa para onde deve se movimentar usando a heuristica e movesse para la
def search(colorArray=None):
    targetHouse = bestNextHouse(colorArray) #Inserir nesta funçao o array das cores
    self.goDirection(targetHouse) """