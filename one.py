## Algorithm 1: Cardinally-adjacent neighbors. If at least on neighbor is grass, a dirt tile converts to grass.

## Set this to define the initial count of grass seedings.
SEED_COUNT = 3

import pygame
import random
import zero

class One(zero.Algorithm):
    def __init__(this, tileMap):
        zero.Algorithm.__init__(this, tileMap)

    def seed(this, seedlings):
        for seeding in range(seedlings):
            ## Pick a random tile.
            row, column = this.getRandomTileCoordinates()

            print "Growing grass at (" + str(row) + "," + str(column) + ")."

            this.growGrass(row, column)

    def getRandomTileCoordinates(this):
        return (random.randint(0, this.rows - 1), random.randint(0, this.columns - 1))

    def hasGrassNeighbors(this, row, column):
        ## Inspect neighbors.
        neighbors = list()

        neighbors.append(this.isGrassTile(row - 1, column))
        neighbors.append(this.isGrassTile(row, column + 1))
        neighbors.append(this.isGrassTile(row + 1, column))
        neighbors.append(this.isGrassTile(row, column - 1))

        return (True in neighbors)

    def onTick(this):
        ## For this algorithm, only the cardinally-adjacent (N, E, S, W) neighbors of a random tile are inspected
        ## to determine if the current tile can grow grass.

        ## Pick a random tile.
        row, column = this.getRandomTileCoordinates()

        if not this.isGrassTile(row, column):
            if this.hasGrassNeighbors(row, column):
                this.growGrass(row, column)

def main():
    tileMap = zero.TileMap(zero.FIELD_ROWS, zero.FIELD_COLUMNS)
    algorithm = One(tileMap)

    field = zero.Field(tileMap, algorithm)

    algorithm.seed(SEED_COUNT)

    field.run()
    field.close()

if __name__ == "__main__":
    main()
