## Algorithm 1: Neighbors only, with some randomization for chance, to convert a dirt entity to a grass entity.

## Take a grid of entities, and randomly choose a starting entity.
## For each tick, determine the chances of any entities with a potential for conversion.
## For each entity with potential, if the calculated chance to convert exceeds some threshold, convert to a grass entity.
## Update the grid of entities.

class Entity:
    def onTick(this, neighbors):
        return NotImplemented

class DirtEntity(Entity):
    def onTick(this, neighbors):
        ## TODO: Examine neighbors to see if any of them are grass entities.
        ## If no neighboring entities are grass types, then there is no chance to convert to grass.
        ## Otherwise, do some kind of math to get to a value to determine if this entity will convert.
        pass

class GrassEntity:
    def onTick(this, neighbors):
        ## This entity is already a grass entity, so there is nothing to do.
        pass

class Field:
    def __init__(this, length, height):
        this.__entities = list()
        this.__dimensions = (length, height)

        for l in range(length):
            for h in range(height):
                this.__entities.append(DirtEntity())

    def __getEntityIndex(this, x, y):
        entityIndex = -1

        length, height = this.__dimensions

        if 0 <= x < length and 0 <= y < height:
            entityIndex = y * length + x

        return entityIndex

    def getEntity(this, x, y):
        entity = None

        entityIndex = this.__getEntityIndex(x, y)

        if 0 <= entityIndex:
            entity = this.__entities[entityIndex]

        return entity

    def getEntityNeighbors(this, x, y):
        n = this.getEntity(x, y - 1)
        e = this.getEntity(x + 1, y)
        s = this.getEntity(x, y + 1)
        w = this.getEntity(x - 1, y)

        neighbors = list()

        if not n is None:
            neighbors.append(n)

        if not e is None:
            neighbors.append(e)

        if not s is None:
            neighbors.append(s)

        if not w is None:
            neighbors.append(w)

        return neighbors

def main():
    field = Field(3, 3) ## Start with a simple 3x3 field.
    print "Length of neighbors of (0, 0):", len(field.getEntityNeighbors(0, 0))
    print "Length of neighbors of (1, 0):", len(field.getEntityNeighbors(1, 0))
    print "Length of neighbors of (2, 0):", len(field.getEntityNeighbors(2, 0))

    print "Length of neighbors of (0, 1):", len(field.getEntityNeighbors(0, 1))
    print "Length of neighbors of (1, 1):", len(field.getEntityNeighbors(1, 1))
    print "Length of neighbors of (2, 1):", len(field.getEntityNeighbors(2, 1))

    print "Length of neighbors of (0, 2):", len(field.getEntityNeighbors(0, 2))
    print "Length of neighbors of (1, 2):", len(field.getEntityNeighbors(1, 2))
    print "Length of neighbors of (2, 2):", len(field.getEntityNeighbors(2, 2))

if __name__ == "__main__":
    main()

