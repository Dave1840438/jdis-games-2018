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
        if size > v.radius * 2:
            return True

    return False


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

    return [ec.position for ec in allEnemyCells if (ec.mass*1.1) <= cell.mass ]


class AI:
    def __init__(self):
        pass

    def step(self, game: Game):
        """
        Given the state of the 'game', decide what your cells ('game.me.cells')
        should do.

        :param game: Game object
        """

        print("Tick #{}".format(game.tick))

        for cell in game.me.cells:
            if cell.mass >= 500:
                cell.trade(abs(cell.mass-250))
            else:
                distance = cell.position.distance_to(cell.target)


                possibleVictims = findVictims(cell, game.enemies)

                target = closestRessource(game, cell, game.resources.allResources + possibleVictims)

                #if distance < 10:
                    #target = Vec2(random.randint(0, game.map.width), random.randint(0, game.map.height))
                if (target != None):
                    cell.move(target)
                else:
                    print ('   KES TU FAIS, VA PAS LÀ ')
