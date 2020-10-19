import sys


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Dimension:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.area = x * y
        self.id = id


class Pallet:
    def __init__(self,  dimension, position):
        self.dimension = dimension
        self.position = position
        self.startX = position.x
        self.endX = position.x + dimension.x
        self.startY = position.y
        self.endY = position.y + dimension.y


def sortArea(val: Dimension):
    return val.area


def readInput():
    storeParameters = input()
    slicedParams = storeParameters.split('\t')
    storeDimensions = Dimension(int(slicedParams[1]), int(slicedParams[0]), 0)
    pillars = int(input().split()[0])
    pallets = int(input().split()[0])
    pillarArray = []
    for x in range(storeDimensions.x):
        row = []
        for y in range(storeDimensions.y):
            row.append(0)
        pillarArray.append(row)
    for i in range(pillars):
        inputArray = input().split('\t')
        pillarArray[int(inputArray[0])][int(inputArray[1])] = 1
    palletDimensions = []
    for i in range(pallets):
        inputArray = input().split('\t')
        palletDimensions.append(Dimension(
            int(inputArray[1]), int(inputArray[0]), i+1))
    palletDimensions.sort(key=sortArea, reverse=True)
    output = []
    for x in range(storeDimensions.x):
        row = []
        for y in range(storeDimensions.y):
            row.append(0)
        output.append(row)
    return storeDimensions, pillarArray, palletDimensions, output


def checkBorders(pallet: Pallet, storeDim: Dimension):
    if(pallet.position.x+pallet.dimension.x > storeDim.x) or (pallet.position.y+pallet.dimension.y > storeDim.y):
        return False
    return True


def checkPillars(pallet: Pallet, pillars: int):
    palletStartX = pallet.position.x
    palletEndX = pallet.position.x + pallet.dimension.x
    palletStartY = pallet.position.y
    palletEndY = pallet.position.y + pallet.dimension.y
    for x in range(palletStartX + 1, palletEndX):
        for y in range(palletStartY + 1, palletEndY):
            if(pillars[x][y] != 0):
                return False
    return True


def checkPallets(pallet: Pallet, output: int):
    pStartX = pallet.position.x
    pEndX = pallet.position.x + pallet.dimension.x
    pStartY = pallet.position.y
    pEndY = pallet.position.y + pallet.dimension.y
    for x in range(pStartX, pEndX):
        for y in range(pStartY, pEndY):
            if(output[x][y] != 0):
                return False
    return True


def addToArray(pallet: Pallet, output: int):
    pStartX = pallet.position.x
    pEndX = pallet.position.x + pallet.dimension.x
    pStartY = pallet.position.y
    pEndY = pallet.position.y + pallet.dimension.y
    id = pallet.dimension.id
    for x in range(pStartX, pEndX):
        for y in range(pStartY, pEndY):
            output[x][y] = id
    return output


def removeFromArray(pallet: Pallet, output: int):
    pStartX = pallet.position.x
    pEndX = pallet.position.x + pallet.dimension.x
    pStartY = pallet.position.y
    pEndY = pallet.position.y + pallet.dimension.y
    id = pallet.dimension.id
    for x in range(pStartX, pEndX):
        for y in range(pStartY, pEndY):
            output[x][y] = 0
    return output


def place(palletDims: Dimension, pillarPositions: int, output: int, storeDimensions: Dimension, i: int):
    for x in range(storeDimensions.x):
        for y in range(storeDimensions.y):
            if(output[x][y] == 0):
                pos = Position(x, y)
                pallet = Pallet(palletDims[i], pos)
                if(checkBorders(pallet, storeDimensions) and checkPillars(pallet, pillarPositions) and checkPallets(pallet, output)):
                    output = addToArray(pallet, output)
                    if(i == len(palletDims) - 1):
                        output = addToArray(pallet, output)
                        return True
                    if(place(palletDims, pillarPositions, output, storeDimensions, i + 1)):
                        return True
                    output = removeFromArray(pallet, output)
                rotatedPallet = Pallet(
                    Dimension(pallet.dimension.y, pallet.dimension.x, pallet.dimension.id), pos)
                if(checkBorders(rotatedPallet, storeDimensions) and checkPillars(rotatedPallet, pillarPositions) and checkPallets(rotatedPallet, output)):
                    output = addToArray(rotatedPallet, output)
                    if(i == len(palletDims) - 1):
                        output = addToArray(rotatedPallet, output)
                        return True
                    if(place(palletDims, pillarPositions, output, storeDimensions, i + 1)):
                        return True
                    output = removeFromArray(rotatedPallet, output)
    return False


def printOutput(output: int):
    for row in output:
        string = ""
        index = 0
        for z in row:
            string += str(z)
            if(len(row)-1 != index):
                string += "\t"
            index += 1
        print(string)


def main():
    if(len(sys.argv) > 1 and sys.argv[1] == 'FILE'):
        fd = open('input.txt', 'r')
        sys.stdin = fd

    storeDimensions, pillarArray, palletDimensions, output = readInput()

    if(len(palletDimensions) > 0):
        place(palletDimensions, pillarArray, output, storeDimensions, 0)

    printOutput(output)


main()
