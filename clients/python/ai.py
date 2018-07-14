"""
This is the file that should be used to code your AI.
"""
import random
from planar import Vec2

from game.models import *



def closestRessource(position, resources):

    result = None
    min = 99999999999;

    for r in resources.allResources:
        distance = position.distance_to(r)
        if distance < min:
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
            if cell.mass >= 110:
                cell.trade(abs(cell.mass-50))
            else:
                distance = cell.position.distance_to(cell.target)


                possibleVictims = findVictims(cell, game.enemies)
                
                target = closestRessource(cell.position, game.resources.allResources + possibleVictims)

                #if distance < 10:
                    #target = Vec2(random.randint(0, game.map.width), random.randint(0, game.map.height))
                if (target != None):
                    cell.move(target)
                else:
                    print ('   KES TU FAIS, VA PAS LÀ ')
