import pygame
from typing import List, Dict
from pygame.surface import Surface

import random


class PositiveInt(int):

    def __new__(cls, value, *args, **kwargs) -> 'PositiveInt':
        if value < 0:
            raise ValueError("positive types must not be less than zero")
        return  super(cls, cls).__new__(cls, value)
    
CARRE_SIZE = 30
GRID_SEPARATOR_SIZE = 1

class ByteInt(int):

    def __new__(cls, value, *args, **kwargs)-> 'ByteInt':
        if value not in range(256):
            raise ValueError("ByteInt types must be between 0 and 255")
        return  super(cls, cls).__new__(cls, value)

class QuadrilateralSize:

    _x: 'PositiveInt'
    _y: 'PositiveInt'

    def __init__(self, x:'PositiveInt', y:'PositiveInt') -> None:
        self._x = x
        self._y = y

    def __eq__(self, __o: object) -> bool:
        return __o._x == self._x and __o._y == self._y

    def getSize(self) -> Dict[str, 'PositiveInt']:
        return {
            'x': self._x,
            'y': self._y
        }

class CarreSize(QuadrilateralSize):

    def __init__(self, size:'PositiveInt') -> None:
        super().__init__(x=size, y=size)

class Color:

    _red     : 'ByteInt'
    _green   : 'ByteInt'
    _blue    : 'ByteInt'

    def __init__(self, red:'ByteInt', green:'ByteInt', blue:'ByteInt') -> None:
        self._red   = red
        self._green = green
        self._blue  = blue

    def __eq__(self, __o: object) -> bool:
        return __o._red == self._red and __o._green == self._green and __o._blue == self._blue

    def getPrimaryColors(self) -> Dict[str, 'ByteInt']:
        return {
            'red'   : self._red,
            'green' : self._green,
            'blue'  : self._blue,
        }
    
class ColorBlack(Color):
    def __init__(self) -> None:
        super().__init__(red=ByteInt(0), green=ByteInt(0), blue=ByteInt(0))

class ColorWhite(Color):
    def __init__(self) -> None:
        super().__init__(red=ByteInt(255), green=ByteInt(255), blue=ByteInt(255))

class OfficialCarreType(int):

    MINE            : int = -1
    FLAG            : int = -2
    MINE_EXPLOSED   : int = -3
    BLACK           : int = -4
    WHITE           : int = -5
    
    def __new__(cls, value, *args, **kwargs) -> 'OfficialCarreType':
        rangeExpected = range(-5, 9)
        if value not in rangeExpected:
            raise ValueError(f"value must be one of {rangeExpected}")
        return  super(cls, cls).__new__(cls, value)

class OfficialPicture():

    _value      : 'Surface'
    _original   : 'Surface'
    
    def __init__(self, type:'OfficialCarreType') -> None:

        specialPictureDict = {
            OfficialCarreType.MINE: "mine.png",
            OfficialCarreType.FLAG: "flag.png",
            OfficialCarreType.MINE_EXPLOSED: "mineExplosed.png",
        }

        if type in specialPictureDict:
            path = specialPictureDict[type]
        elif type in range(9):
            path = f"{type}.png"
        else:
            return

        picture = pygame.image.load(path)

        # Redimensionner l'image pour qu'elle entre dans le carré
        if picture.get_width() > picture.get_height():
            scale = CARRE_SIZE / picture.get_width()
        else:
            scale = CARRE_SIZE / picture.get_height()
        self._value = pygame.transform.scale(picture, (int(picture.get_width() * scale), int(picture.get_height() * scale)))
        self._original = picture

    def getPicture(self) -> 'Surface':
        return self._value

OFFICIAL_PICTURE = {officialType: OfficialPicture(officialType).getPicture() for officialType in range(-3, 9)}

class QuadrilateralIdentity:

    _size   :'QuadrilateralSize'
    _color  :'Color'

    def __init__(self, size:'QuadrilateralSize', color:'Color') -> None:
        self._size = size
        self._color = color

    def __eq__(self, __o: object) -> bool:
        return __o._size == self._size and __o._color == self._color

    def getColor(self) -> Dict[str, 'ByteInt']:
        return self._color.getPrimaryColors()

    def getSize(self) -> Dict[str, 'PositiveInt']:
        return self._size.getSize()

class CarreIdentity(QuadrilateralIdentity):

    def __init__(
            self,
            size: 'CarreSize',
            color: 'Color' = Color(
                red     = ByteInt(0),
                green   = ByteInt(0),
                blue    = ByteInt(0)
            )
        ) -> None:
        super().__init__(size=size, color=color)

class Point:

    _x: 'PositiveInt'
    _y: 'PositiveInt'

    def __init__(self, x: 'PositiveInt', y: 'PositiveInt') -> None:
        self._x = x
        self._y = y

    def __eq__(self, __o: object) -> bool:
        return __o._x == self._x and __o._y == self._y

    def getPoint(self) -> Dict[str, 'PositiveInt']:
        return {
            'x': self._x,
            'y': self._y
        }

class Quadrilateral:
    _identity: 'QuadrilateralIdentity'
    _position: 'Point'

    def __init__(self, identity: 'QuadrilateralIdentity', position: 'Point') -> None:
        self._identity = identity
        self._position = position

    def __eq__(self, __o: object) -> bool:
        return __o._identity == self._identity and __o._position == self._position

    def changePosition(self, newPosition:'Point') -> None:
        self._position = newPosition

    def draw(self, screen:'Surface') -> None:

        primaryColor    = self._identity.getColor()
        size            = self._identity.getSize()
        position        = self._position.getPoint()

        pygame.draw.rect(
            screen,
            ( primaryColor['red'], primaryColor['green'], primaryColor['blue'] ),
            ( position['x'], position['y'], size['x'], size['y'] )
        )

class Carre(Quadrilateral):

    def __init__(self, identity: 'CarreIdentity', position: 'Point') -> None:
        super().__init__(identity=identity, position=position)

class CarrePicture(Carre):

    _picture: 'Surface'

    def __init__(self, identity: 'CarreIdentity', position: 'Point', type:'OfficialCarreType') -> None:
        super().__init__(identity, position)
        self._picture = OFFICIAL_PICTURE[type]

    def __eq__(self, __o: object) -> bool:
        return hasattr(__o, '_picture') and __o._picture == self._picture

    def draw(self, screen:'Surface') -> None:
        super().draw(screen=screen)

        position    = self._position.getPoint()
        screen.blit(self._picture, (position['x'], position['y']))

class CarreMine(CarrePicture):

    def __init__(self, identity: 'CarreIdentity', position: 'Point') -> None:
        super().__init__(identity=identity, position=position, type=OfficialCarreType.MINE)

class CarreFlag(CarrePicture):

    def __init__(self, identity: 'CarreIdentity', position: 'Point') -> None:
        super().__init__(identity=identity, position=position, type=OfficialCarreType.FLAG)

class Digit(int):

    def __new__(cls, value, *args, **kwargs) -> 'Digit':
        if value not in range(10):
            raise ValueError("not digit value")
        return  super(cls, cls).__new__(cls, value)

class CarreNumber(CarrePicture):

    def __init__(self, identity: 'CarreIdentity', position: 'Point', number: 'Digit') -> None:
        super().__init__(identity=identity, position=position, type=number)

class MineSchemaType(int):
    
    def __new__(cls, value, *args, **kwargs) -> 'MineSchemaType':
        rangeExpected = range(-1, 9)
        if value not in rangeExpected:
            raise ValueError(f"value must be one of {rangeExpected}")
        return  super(cls, cls).__new__(cls, value)

class Coord:
    _coordX: 'PositiveInt'
    _coordY: 'PositiveInt'

    def __init__(self, coordX: 'PositiveInt', coordY: 'PositiveInt') -> None:
        self._coordX = coordX
        self._coordY = coordY

    def _createCarreIdentity(self, color: 'Color'=ColorBlack()) -> 'CarreIdentity':
        return CarreIdentity(size=CarreSize(size=CARRE_SIZE), color=color)

    def _createCarrePosition(self) -> 'Point':
        x = PositiveInt(self._carrePositionCalcul(self._coordX))
        y = PositiveInt(self._carrePositionCalcul(self._coordY))

        return Point(x=x, y=y)

    def createCarre(self, type:'OfficialCarreType') -> 'Carre':
        if type == OfficialCarreType.FLAG:
            return CarreFlag(identity=self._createCarreIdentity(), position=self._createCarrePosition())
        if type == OfficialCarreType.MINE:
            return CarreMine(identity=self._createCarreIdentity(), position=self._createCarrePosition())
        if type == OfficialCarreType.BLACK:
            return Carre(identity=self._createCarreIdentity(), position=self._createCarrePosition())
        if type in range(9):
            return CarreNumber(identity=self._createCarreIdentity(), position=self._createCarrePosition(), number=Digit(type))

    def displaySlot(self, gridValue: List['SlotLine']) -> None:
        gridValue[self._coordY].displaySlotByCoord(coordX=self._coordX)

    def retrieveProximityCoord(self, gridSize: 'PositiveInt') -> List['Coord']:
        proximityCoords = []

        # line before
        if self._coordY > 0:
            for x in [self._coordX - 1, self._coordX, self._coordX + 1]:
                if x in range(gridSize): proximityCoords.append(Coord(coordX=x, coordY=self._coordY - 1))

        # currentLine
        for x in [self._coordX - 1, self._coordX + 1]:
            if x in range(gridSize): proximityCoords.append(Coord(coordX=x, coordY=self._coordY))

        # line after
        if self._coordY < gridSize - 1 :
            for x in [self._coordX - 1, self._coordX, self._coordX + 1]:
                if x in range(gridSize): proximityCoords.append(Coord(coordX=x, coordY=self._coordY + 1))

        return proximityCoords

    def incrementMineSchema(self, mineSchema=List[List[MineSchemaType]]) -> None:
        if mineSchema[self._coordY][self._coordX] >= 0:
            mineSchema[self._coordY][self._coordX] += 1

    def getSchemaValue(self, mineSchema=List[List[MineSchemaType]]) -> 'MineSchemaType':
        return mineSchema[self._coordY][self._coordX]

    def carreIsDisplay(self, carre: 'Carre')-> bool:
        return carre not in [
            Carre(identity=self._createCarreIdentity(), position=self._createCarrePosition()),
            CarreFlag(identity=self._createCarreIdentity(), position=self._createCarrePosition())
        ]

    def slotIsDiplay(self, gridValue: List['SlotLine']) -> bool:
        return gridValue[self._coordY]._value[self._coordX].isDisplay()

    def slotIsFlaged(self, carre: 'Carre')-> bool:
        return carre == CarreFlag(identity=self._createCarreIdentity(), position=self._createCarrePosition())

    def toggleFlag(self, gridValue: List['SlotLine']) -> None:
        gridValue[self._coordY]._value[self._coordX].toggleFlag()

    def _carrePositionCalcul(self, cardinal: 'PositiveInt') -> 'PositiveInt':
        return PositiveInt(cardinal * CARRE_SIZE + (1 + cardinal) * GRID_SEPARATOR_SIZE)

class Slot:
    _carre      : 'Carre'
    _coord      : 'Coord'

    def __init__(self, coord: 'Coord') -> None:
        self._coord = coord
        self._carre = coord.createCarre(type=OfficialCarreType.BLACK)

    def draw(self, screen:'Surface') -> None:
        self._carre.draw(screen=screen)

    def display(self) -> None:
        pass

    def isDisplay(self) -> bool:
        return self._coord.carreIsDisplay(carre=self._carre)

    def toggleFlag(self) -> None:
        if self.isDisplay(): return
        if not self._coord.slotIsFlaged(carre=self._carre):
            self._carre = self._coord.createCarre(type=OfficialCarreType.FLAG)
        else:
            self._carre = self._coord.createCarre(type=OfficialCarreType.BLACK)


class SlotMine(Slot):

    def display(self) -> None:
        self._carre = self._coord.createCarre(type=OfficialCarreType.MINE)

class SlotEmpty(Slot):

    _mineCountAtProximity: 'PositiveInt'

    def __init__(self, coord: 'Coord', mineCountAtProximity: 'PositiveInt') -> None:
        self._mineCountAtProximity = mineCountAtProximity
        super().__init__(coord)

    def display(self) -> None:
        self._carre = self._coord.createCarre(type=self._mineCountAtProximity)

class SlotLine:
    _value: List['Slot']

    def __init__(self, mineSchemaLine: List['MineSchemaType'], coordY:'PositiveInt') -> None:
        self._value = []
        for schema in mineSchemaLine:
            coord = Coord(coordX=len(self._value), coordY=coordY)
            if schema ==  -1: 
                slot = SlotMine(coord=coord)
            else:
                slot = SlotEmpty(coord=coord, mineCountAtProximity=schema)
            self._value.append(slot)

    def draw(self, screen:'Surface') -> None:
        for slot in self._value:
            slot.draw(screen=screen)

    def displaySlotByCoord(self, coordX: 'PositiveInt') -> None:
        self._value[coordX].display()

    def displayAll(self) -> None:
        for slot in self._value:
            slot.display()

class Grid:
    _value      : List['SlotLine']
    _mineSchema : List[List['MineSchemaType']]

    def __init__(self, size: 'PositiveInt', mineCount: 'PositiveInt') -> None:

        if mineCount > size * size:
            raise Exception("mine count is too big")

        self._value = []

        self._mineSchema = self._createMineSchema(gridSize=size, mineCount=mineCount)
        self._addMineCountAtProximityOnSchema()

        for shemaLine in self._mineSchema:
            slotLine = SlotLine(mineSchemaLine=shemaLine, coordY=len(self._value))
            self._value.append(slotLine)

    def draw(self, screen:'Surface') -> None:
        for slotLine in self._value:
            slotLine.draw(screen=screen)

    def displaySlotByClick(self, clickPosition:'Point') -> None:
        coordX, coordY = self._getCoordsFromPoint(point=clickPosition)
        if coordX is None or coordY is None: return

        self._displaySlot(coord=Coord(coordX=coordX, coordY=coordY))

    def displayAll(self) -> None:
        for slotLine in self._value:
            slotLine.displayAll()

    def toggleFlag(self, clickPosition:'Point') -> None:
        coordX, coordY = self._getCoordsFromPoint(point=clickPosition)
        if coordX is None or coordY is None: return

        Coord(coordX=coordX, coordY=coordY).toggleFlag(gridValue=self._value)

    def _displaySlot(self, coord: 'Coord') -> None:

        # recurence here
        coord.displaySlot(gridValue=self._value)
        if coord.getSchemaValue(mineSchema=self._mineSchema) == 0:
            proximityCoords = coord.retrieveProximityCoord(gridSize=len(self._mineSchema))
            for proximityCoord in proximityCoords:
                if not proximityCoord.slotIsDiplay(gridValue=self._value):
                    self._displaySlot(coord=proximityCoord)

    def _createMineSchema(self, gridSize: 'PositiveInt', mineCount: 'PositiveInt') -> List[List['MineSchemaType']]:
        slotCount = gridSize * gridSize
        schema = [MineSchemaType(-1)] * mineCount + [MineSchemaType(0)] * (slotCount - mineCount)
        random.shuffle(schema)

        shemaList = []
        for numSlotLine in range(gridSize):
            shemaList.append(schema[numSlotLine * gridSize:(numSlotLine + 1) * gridSize])

        return shemaList

    def _addMineCountAtProximityOnSchema(self) -> None:

        gridSize = len(self._mineSchema)
        for schemaLineNum in range(gridSize):
            for schemaSlotNum in range(gridSize):
                if self._mineSchema[schemaLineNum][schemaSlotNum] == MineSchemaType(-1):
                    coord = Coord(coordY=schemaLineNum, coordX=schemaSlotNum)
                    proximityCoords = coord.retrieveProximityCoord(gridSize=gridSize)
                    for proximityCoord in proximityCoords:
                        proximityCoord.incrementMineSchema(mineSchema=self._mineSchema)

    def _getCoordsFromPoint(self, point: 'Point') -> tuple('PositiveInt'):
        clickY = point.getPoint()['y']
        clickX = point.getPoint()['x']

        coordX = self._clickCoordCalcul(cardinal=clickX)
        coordY = self._clickCoordCalcul(cardinal=clickY)

        return coordX, coordY

    def _clickCoordCalcul(self, cardinal:'PositiveInt') -> 'PositiveInt':
        check = GRID_SEPARATOR_SIZE
        for carreCount in range(len(self._value)):
            if cardinal <= check + CARRE_SIZE:
                return carreCount
            check += CARRE_SIZE
            if cardinal <= check + GRID_SEPARATOR_SIZE:
                return None
            check += GRID_SEPARATOR_SIZE
        return None

class GameData:
    _grid   : 'Grid'
    _screen : 'Surface'

    def __init__(self, gridSize: 'PositiveInt' = 20, mineCount: 'PositiveInt' = 10) -> None:
        screenSize = PositiveInt(gridSize * CARRE_SIZE + (gridSize + 1)*GRID_SEPARATOR_SIZE)
        self._screen = pygame.display.set_mode((screenSize, screenSize))

        self._grid = Grid(size=gridSize, mineCount=mineCount)

    def draw(self) -> None:
        self._screen.fill((ByteInt(255), ByteInt(255), ByteInt(255)))
        self._grid.draw(screen=self._screen)

    def displaySlotByClick(self, clickPosition:'Point') -> None:
        self._grid.displaySlotByClick(clickPosition=clickPosition)

    def displayAll(self) -> None:
        self._grid.displayAll()

    def toggleFlag(self, clickPosition:'Point') -> None:
        self._grid.toggleFlag(clickPosition=clickPosition)

# Initialiser Pygame
pygame.init()

# initier une grille
gridSize    = PositiveInt(10)
mineCount   = PositiveInt(10)
gameData    = GameData(gridSize=gridSize, mineCount=mineCount)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:

            mouse_x, mouse_y = pygame.mouse.get_pos()
            clickPosition = Point(x=mouse_x, y=mouse_y)

            if event.button == 1: # left click
                gameData.displaySlotByClick(clickPosition=clickPosition)
                #gameData.displayAll()

            if event.button == 3: # right click
                gameData.toggleFlag(clickPosition=clickPosition)

    # Mettre à jour l'affichage
    gameData.draw()
    pygame.display.update()

# Quitter Pygame
pygame.quit()