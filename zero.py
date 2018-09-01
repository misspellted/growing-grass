## Algorithm "0": Provide the common visualization components for demonstrating actual algorithms.

## Set these to define the size of the Field instance.
FIELD_ROWS = 50
FIELD_COLUMNS = 80

import pygame
import random

class TileChangedListener:
    def onTileChanged(this, grewGrass):
        pass

class Tile:
    def __init__(this):
        this.grewGrass = False
        this.tileChangedListener = None

    def setTileChangedListener(this, listener):
        this.tileChangedListener = listener

    def hasGrownGrass(this):
        return this.grewGrass

    def growGrass(this):
        if not this.grewGrass:
            this.grewGrass = True

            if not this.tileChangedListener is None:
                this.tileChangedListener.onTileChanged(True)

class TileViewChangedListener:
    def onTileViewChanged(this, row, column):
        pass

class TileView(TileChangedListener):
    LENGTH = 16
    HEIGHT = 16

    DIRT_COLOR = (63, 63, 0, 255)
    GRASS_COLOR = (0, 255, 0, 255)

    def __init__(this, tile, row, column):
        if not isinstance(tile, Tile):
            raise ValueError("A tile is required.")

        this.rendering = pygame.Surface((TileView.LENGTH, TileView.HEIGHT), pygame.SRCALPHA, 32)
        this.rendering.fill(TileView.DIRT_COLOR)

        tile.setTileChangedListener(this)

        this.tileViewChangedListener = None
        this.row = row
        this.column = column

    def setTileViewChangedListener(this, listener):
        this.tileViewChangedListener = listener

    def onTileChanged(this, grewGrass):
        this.rendering.fill(TileView.GRASS_COLOR)

        if not this.tileViewChangedListener is None:
            this.tileViewChangedListener.onTileViewChanged(this.row, this.column)

    def render(this):
        return this.rendering

class TileMap:
    def __init__(this, rows, columns):
        this.tiles = list()
        this.rows = rows
        this.columns = columns

        for tileIndex in range(rows * columns): this.tiles.append(Tile())

    def getRowCount(this):
        return this.rows

    def getColumnCount(this):
        return this.columns

    def getTile(this, row, column):
        tileIndex = (row * this.columns + column) if 0 <= row < this.rows and 0 <= column < this.columns else -1

        return this.tiles[tileIndex] if 0 <= tileIndex else None

    def onTick(this):
        ## Override this method to inject the algorithm into the visualization of the algorithm.
        pass

class TileMapView(TileViewChangedListener):
    BACKGROUND_COLOR = (0, 0, 0, 0)

    def __init__(this, tileMap):
        if not isinstance(tileMap, TileMap):
            raise ValueError("A tile map is required.")

        this.tileViews = list()
        this.rows = tileMap.getRowCount()
        this.columns = tileMap.getColumnCount()

        for row in range(this.rows):
            for column in range(this.columns):
                tileView = TileView(tileMap.getTile(row, column), row, column)
                tileView.setTileViewChangedListener(this)
                this.tileViews.append(tileView)

        this.rendering = pygame.Surface((this.columns * TileView.LENGTH, this.rows * TileView.HEIGHT), pygame.SRCALPHA, 32)
        this.rendering.fill(TileMapView.BACKGROUND_COLOR)

    def onTileViewChanged(this, row, column):
        tileView = this.tileViews[row * this.columns + column]
        this.rendering.blit(tileView.render(), (column * TileView.LENGTH, row * TileView.HEIGHT))

    def render(this):
        return this.rendering

class PyGameEventApp:
    def __init__(this, debugMessages=False):
        this._debugging = debugMessages
        this.running = False

    def onKeyDown(this, key):
        if this._debugging: print str.format("KeyDown: {0}", key)

    def onKeyUp(this, key):
        if this._debugging: print str.format("KeyUp: {0}", key)

    def onQuit(this):
        this.running = False
        if this._debugging: print "Quitting..."

    def onUpdate(this):
        if this._debugging: print "Updating..."

    def run(this):
        this.running = True
        while this.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    this.onQuit()
                elif event.type == pygame.KEYDOWN:
                    this.onKeyDown(event.key)
                elif event.type == pygame.KEYUP:
                    this.onKeyUp(event.key)
            if this.running:
                this.onUpdate()

class Field(PyGameEventApp):
    def __init__(this, tileMap, caption="Field o' Grass"):
        if not isinstance(tileMap, TileMap):
            raise ValueError("A tile map is required.")

        PyGameEventApp.__init__(this)
        pygame.display.init()

        this.length = tileMap.getColumnCount() * TileView.LENGTH
        this.height = tileMap.getRowCount() * TileView.HEIGHT

        this._screen = pygame.display.set_mode((this.length, this.height), pygame.DOUBLEBUF, 32)
        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(0)

        this.tileMap = tileMap
        this.tileMapView = TileMapView(this.tileMap)

    def onKeyDown(this, key):
        if key == pygame.K_ESCAPE:
            this.running = False

    def onUpdate(this):
        ## Request an update to the tile map (poke the algorithm).
        this.tileMap.onTick()

        ## Draw the tile map to the screen.
        this._screen.blit(this.tileMapView.render(), (0, 0))
        pygame.display.flip()

    def close(this):
        pygame.display.quit()

    def getLength(this):
        return this.length

    def getHeight(this):
        return this.height

    def getRowCount(this):
        return this.tileMap.getRowCount()

    def getColumnCount(this):
        return this.tileMap.getColumnCount()

    def seed(this, row, column):
        tile = this.tileMap.getTile(row, column)

        if not tile is None:
            tile.growGrass()
