"""
This is the file that should be used to code your AI.
"""
import random
import math
from planar import Vec2

from game.models import *


def checkVirusCollision(game, cell, target):

    size = cell.radius

    for v in game.viruses:

        if v.radius * 1.1 >= cell.radius:
            continue

        angle = abs((target - cell.position).angle_to(v.position - cell.position))

        distance = math.sin(angle) * cell.position.distance_to(v.position)
        if size > v.radius * 2 or v.position.distance_to(target) < 100:
            return True

    return False

def getDangerousEnemies(game, cell, target):
    allEnemyCells = []
    for e in game.enemies:
        allEnemyCells = allEnemyCells+e.cells

    return [ec.position for ec in allEnemyCells if ec.radius >= (cell.radius*1.1) ]









def enemyComingthrough(cell, enemyCell):

    pos = cell.position
    ePos = enemyCell.position

    eDirection = enemyCell.target - ePos
    eToMe = pos - ePos

    if pos.distance_to(ePos) < 250:
        if abs(eDirection.angle_to(eToMe)):
            pass




def closestRessource(game, cell, targets):

    result = None
    min = 99999999999;

    for r in targets:
        distance = cell.position.distance_to(r)
        if distance < min and not checkVirusCollision(game, cell, r):
            min = distance
            result = r

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
    return allEnemyCells[math.ceil(len(allEnemyCells)*0.95)].mass*2 # x2 because the cells after the split should be at the 75ht percentile

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
                    target = closestRessource(game, cell, game.resources.allResources + possibleVictims)
                else:
                    if not cell.burst:
                        cell.burst()
                    target = closestRessource(game, cell, possibleVictims)

                #if distance < 10:
                    #target = Vec2(random.randint(0, game.map.width), random.randint(0, game.map.height))
                if (target != None):
                    cell.move(target)
                else:
                    print ('   KES TU FAIS, VA PAS LÀ ')
