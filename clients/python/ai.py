"""
This is the file that should be used to code your AI.
"""
import random
import math
from planar import Vec2, Ray

from game.models import *


def checkVirusCollision(game, cell, target):

    size = cell.radius

    dir = target - cell.position

    if dir.is_null:
        return False

    r = Ray(cell.position, dir)

    for v in game.viruses:

        if v.radius * 1.1 >= cell.radius:
            continue

        d = r.distance_to(v.position)

        if v.radius + cell.radius < distance:
            return True

    return False

def getDangerousEnemies(game, cell, target):
    allEnemyCells = []
    for e in game.enemies:
        allEnemyCells = allEnemyCells+e.cells

    return [ec.position for ec in allEnemyCells if ec.radius >= (cell.radius*1.1) ]


def enemyComingthrough(cell, enemyCell):

    if cell.position.distance_to(enemyCell.position) > 250:
        return False

    dir = enemyCell.target - enemyCell.position

    if dir.is_null:
        return False

    r = Ray(enemyCell.position, dir)

    d = r.distance_to(cell.position)

    if enemyCell.radius > d + cell.radius:
        return True

    return False


def closestRessource(game, cell, targets, nbOfEnemies):

    result = None
    min = 99999999999;
    index = 9999999;

    for i in range(len(targets)):
        distance = cell.position.distance_to(targets[i])

        if i == nbOfEnemies and index < 10000 and cell.position.distance_to(result) < 100:
            if cell.mass >= 200:
                cell.burst()
            break

        if distance < min: # and not checkVirusCollision(game, cell, targets[i]):

            if i < nbOfEnemies and result != None and cell.position.distance_to(result) < 250:
                dir = result - cell.position
                if not dir.is_null:
                    r = Ray(cell.position, dir)
                    d = r.distance_to(targets[i])
                    if d + cell.radius < 75:
                        pass


            min = distance
            result = targets[i]
            index = i





    return result

def findVictims(cell, enemies):

    allEnemyCells = []
    for e in enemies:
        allEnemyCells = allEnemyCells+e.cells

    return [ec.position for ec in allEnemyCells if (ec.radius*1.1) <= cell.radius ]

def getSplitValue(game):
    allEnemyCells = []
    for e in game.enemies:
        allEnemyCells = allEnemyCells+e.cells
    allEnemyCells.sort(key=lambda x: x.radius)

    return 350

    #return allEnemyCells[len(allEnemyCells) -1 ].mass * 2

    #return allEnemyCells[math.floor(len(allEnemyCells)*0.8)].mass*2 # x2 because the cells after the split should be at the 75ht percentile

class AI:
    def __init__(self):
        pass

    def step(self, game: Game):
        """
        Given the state of the 'game', decide what your cells ('game.me.cells')
        should do.

        :param game: Game object
        """

        print("Tick #{}".format(game.time_left))

        splitValue = getSplitValue(game)
        print (getSplitValue(game))

        for cell in game.me.cells:

            if game.time_left < 6:
                cell.trade(99999)




            if cell.mass >= splitValue:
                if len(game.me.cells) < 10:
                    cell.split()
                #else:
                    #cell.trade(cell.mass - 100)
            else:
                distance = cell.position.distance_to(cell.target)
                possibleVictims = findVictims(cell, game.enemies)

                if (cell.mass <= 100):
                    target = closestRessource(game, cell, possibleVictims + game.resources.allResources, len(possibleVictims))
                else:
                    #cell.burst()
                    target = closestRessource(game, cell, possibleVictims, len(possibleVictims))


                for e in game.enemies:
                    for c in e.cells:
                        if enemyComingthrough(cell, c):
                            target = cell.position + (c.target - c.position)
                            #cell.burst()
                            pass

                if (target != None):
                    cell.move(target)
                else:
                    print ('   KES TU FAIS, VA PAS LÀ ')
