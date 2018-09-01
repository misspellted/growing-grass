## Algorithm 1: Cardinally-adjacent neighbors. If at least on neighbor is grass, a dirt tile converts to grass.

## Set this to define the initial count of grass seedings.
SEED_COUNT = 3

import pygame
import random
import zero

class TileMapOne(zero.TileMap):
    def __init__(this, rows=zero.FIELD_ROWS, columns=zero.FIELD_COLUMNS):
        zero.TileMap.__init__(this, rows, columns)

    def onTick(this):
        ## Pick a random tile.
        row = random.randint(0, this.rows - 1)
        column = random.randint(0, this.columns - 1)

        tile = this.getTile(row, column)

        if not tile is None:
            ## If the tile hasn't grown grass... give it a chance.
            if not tile.hasGrownGrass():
                ## For this algorithm, only the adjacent neighbors are included (N, E, S, W).

                ## Inspect neighbors.
                neighbors = list()

                neighbors.append(this.getTile(row - 1, column))
                neighbors.append(this.getTile(row, column + 1))
                neighbors.append(this.getTile(row + 1, column))
                neighbors.append(this.getTile(row, column - 1))

                contribution = 0

                for neighbor in neighbors:
                    ## Each neighbor gives a 25% chance for the current tile to grow grass.
                    contribution += 0.25 if isinstance(neighbor, zero.Tile) and neighbor.hasGrownGrass() else 0.00

##                print "Contribution of neighbors for (" + str(row) + ", " + str(column) + "):", contribution

                if 0 < contribution:
                    tile.growGrass()

def seedRandomGrass(field):
    row = random.randint(0, field.getRowCount() - 1)
    column = random.randint(0, field.getColumnCount() - 1)

    print "Seeding grass at (" + str(row) + "," + str(column) + ")."

    field.seed(row, column)

def main():
    field = zero.Field(TileMapOne())

    for seedling in range(SEED_COUNT):
        seedRandomGrass(field)

    field.run()
    field.close()

if __name__ == "__main__":
    main()
