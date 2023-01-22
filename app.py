'''Imports'''
# sys module
import sys
# PyGame module
import pygame
# Random module
import random
# Map coordinates as a file
from mapCoordinates import standardMapCoordinates

import numpy as np

'''Variable for testing'''
global TEST
TEST = False


'''Global variables/constants'''
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')


'''Class declarations'''
class Game(): ...
class Scene(): ...
class MainMenu(): ...
class InGame(): ...
class Pause(): ...
class End(): ...
class Text(): ...

'''Text class'''
class Text():
	def __init__(self, text:str, fontSizePixel:int, position:tuple[int,int]=(0,0), font:str='unispace bd.ttf', antialias:bool=True, textColor=WHITE) -> None:
		self.text = text
		self.fontSizePixel = fontSizePixel
		self.position = position
		self.font = self.validateFont(font)
		self.rendered = self.font.render(self.text, antialias, textColor)
		self.rectangle = self.rendered.get_rect(topleft = (self.position))

		self.textSize = self.font.size(self.text)
		self.width = self.textSize[0]
		self.height = self.textSize[1]
	# Changes text
	def changeTo(self, text):
		self.text = text
	
	def changePosition(self, position):
		self.position = position
		self.rectangle = self.rendered.get_rect(topleft = (self.position))

	def doesCollide(self, x:int, y:int):
		return self.rectangle.collidepoint(x, y) 

	def validateFont(self, font:str) -> pygame.font.Font:
		try:
			return pygame.font.Font(font, self.fontSizePixel)
		except FileNotFoundError as e:
			defaultFontPath = '/unispace bd.ttf'
			print(f'{e}')
			print(f'Using the default font: {defaultFontPath}')
			return pygame.font.Font(defaultFontPath, self.fontSizePixel)
'''Scene class'''
class Scene():
	def __init__(self, game:Game) -> None:
		self.current = None
		self.game = game
	# Initializes scenes
	def initialize(self) -> None:
		self.menu = MainMenu(self.game)
		self.inGame = InGame(self.game)
		self.pause = Pause(self.game)
		self.end = End(self.game)
		self.changeTo(self.menu)
	# Pauses game
	def pauseScene(self) -> None:
		self.changeTo(self.pause)
	# Unpauses game
	def unpauseScene(self) -> None:
		self.changeTo(self.inGame)
	# Changes scene
	def changeTo(self, scene:Scene) -> None:
		self.current = scene
	# Draws current scene
	def draw(self):
		self.current.draw()
	# Updates the current scene
	def update(self, x:int, y:int) -> None:
		# self.current.update(x, y)
		pass
'''Main menu class'''
class MainMenu(Scene):
	def __init__(self, game=Game) -> None:
		super().__init__(game)
		self.name = 'Main Menu'
		self.initialize()
	# Initializes scene
	def initialize(self):
		fontSize = 50
		self.play = Text('PLAY', fontSize)
		self.play.changePosition((self.game.windowWidth//2 - self.play.width//2, 1.5 * self.play.fontSizePixel))
		self.quit = Text('QUIT', fontSize)
		self.quit.changePosition((self.game.windowWidth//2 - self.play.width//2, 4 * self.quit.fontSizePixel))
	# Draws scene
	def draw(self) -> None:
		if self.game.score != 0: self.game.score = 0
		self.game.screen.fill(BLACK)
		self.game.screen.blit(self.play.rendered, self.play.position)
		self.game.screen.blit(self.quit.rendered, self.quit.position)
	# Updates if buttons are clicked
	def update(self, x:int, y:int) -> None:
		if self.play.doesCollide(x, y):
			self.game.scene.changeTo(self.game.scene.inGame)
		if self.quit.doesCollide(x, y):
			self.game.quit()
'''In game class'''
class InGame(Scene):
	def __init__(self, game=Game) -> None:
		super().__init__(game)
		self.name = 'InGame'
		self.fontSizePixel = 20
	# Draws game and score
	def draw(self):
		self.game.draw()
		self.score = Text(f'SCORE {self.game.score:2}', self.fontSizePixel)
		self.score.changePosition((self.game.windowWidth - self.score.width - 1, 0))
		self.game.screen.blit(self.score.rendered, self.score.position)
	# Does not do anything
	def update(self, x: int, y: int) -> None:
		pass
'''Pause class'''
class Pause(Scene):
	def __init__(self, game=Game) -> None:
		super().__init__(game)
		self.initialize()
		self.name = 'Paused'
	# Initializes class
	def initialize(self):
		fontSizePixel = 50
		self.paused = Text('PAUSED', fontSizePixel)
		self.paused.changePosition((self.game.windowWidth//2 - self.paused.width//2, self.game.windowHeight//2 - self.paused.fontSizePixel))
		self.resume = Text('PAUSED', fontSizePixel)
		self.resume.changePosition((self.game.windowWidth//2 - self.resume.width//2, self.game.windowHeight//2 + self.resume.fontSizePixel))
	# Updates if buttons are clicked
	def update(self, x:int, y:int):
		if self.resume.doesCollide(x, y):
			self.game.scene.changeTo(self.game.scene.inGame)
	# Draws a pause in the middle of the screen
	def draw(self):
		game.screen.blit(self.paused.rendered, self.paused.position)
'''End class'''
class End(Scene):
	def __init__(self, game=Game) -> None:
		super().__init__(game)
		self.name = 'End'
	# Initializes text
	def initialize(self) -> None:
		# TODO: You won info with points, green text color
		# TODO: You lost info with points, red text color
		fontSize = 50
		self.gameEnded = Text('GAME ENDED', fontSize)
		self.gameEnded.changePosition((self.game.windowWidth//2 - self.gameEnded.width//2, 1 * self.gameEnded.fontSizePixel))

		self.finalScore = Text(f'FINAL SCORE: {self.game.score}', fontSize)
		self.finalScore.changePosition((self.game.windowWidth//2 - self.finalScore.width//2, 3 * self.finalScore.fontSizePixel))

		fontSize = 30
		self.menu = Text('MAIN MENU', fontSize)
		self.menu.changePosition((self.game.windowWidth//2 - self.menu.width//2, self.game.windowHeight - 3 * self.menu.fontSizePixel))
	# Draws the game ended screen with score
	def draw(self):
		self.initialize()
		self.game.screen.fill(BLACK)
		game.screen.blit(self.gameEnded.rendered, self.gameEnded.position)
		game.screen.blit(self.finalScore.rendered, self.finalScore.position)
		game.screen.blit(self.menu.rendered, self.menu.position)
	# Updates if button is clicked
	def update(self, x:int, y:int) -> None:
		if self.menu.doesCollide(x, y):
			self.game.scene.changeTo(self.game.scene.menu)
'''Direction class'''
class Direction():
	def __init__(self, size:tuple, direction=None) -> None:
		self.left = -1,  0
		self.right = 1,  0
		self.up = 	 0, -1
		self.down =  0,  1
		self.size = size
		self.currentDirection = self.left if direction is None else direction
	# Gets direction with hokus pokus tuple magic
	def getDirection(self) -> tuple[int, int]:
		return self.multiplyTuple(self.multiplyTuple(self.size, 1, 1), *self.currentDirection)
	# Gives rotation in degrees
	def rotationDegrees(self):
		x = 0
		if self.currentDirection[0] ==  1: x = 0
		if self.currentDirection[1] == -1: x = 90
		if self.currentDirection[0] == -1: x = 180
		if self.currentDirection[1] ==  1: x = 270
		return x
	# Sets random direction
	def randomDirection(self):
		r = random.randrange(0, 4)
		if r == 0: self.currentDirection = self.up
		if r == 1: self.currentDirection = self.left
		if r == 2: self.currentDirection = self.down
		if r == 3: self.currentDirection = self.right
	# Returns multiplied tuple[0] by x and tuple[1] by y
	def multiplyTuple(self, sizeTuple:tuple, x:int, y:int):
		return sizeTuple[0] * x, sizeTuple[1] * y
'''Game object class'''
class GameObject():
	def __init__(self, positionX:int=0, positionY:int=0, name:str='', color:pygame.Color=BLACK, imagePath:str=None, screen:pygame.Surface=None) -> None:
		self.positionX = positionX
		self.positionY = positionY
		self.name = name
		self.color = color
		self.imagePath = imagePath
		self.image = None
		self.screen = screen

		if color is not None:
			self.color = pygame.color.Color(color)
		
		if imagePath is not None:
			self.image = pygame.image.load(imagePath)
			self.image = pygame.transform.scale(self.image, (32, 32))
			self.imageRectangle = self.image.get_rect(x=positionX, y=positionY)
			self.imageWidth = self.image.get_width()
			self.imageHeight = self.image.get_height()
	# Draws object on screen
	def draw(self):
		if self.image is not None:
			self.imageRectangle = self.image.get_rect(x=self.positionX, y=self.positionY)
			self.screen.blit(self.image, self.imageRectangle)
	# Checks positions
	def checkcollision(self, x:int, y:int):
		return self.positionX == x or self.positionY == y
'''Enemy class'''
class Enemy(GameObject):
	def __init__(self, positionX:int=0, positionY:int=0, name:str='', color: pygame.Color = BLACK, imagePath: str = None, screen:pygame.Surface=None) -> None:
		super().__init__(positionX, positionY, name, color, imagePath, screen)
		self.direction = Direction(self.image.get_size(), direction=Direction((0,0)).up)
		self.startingPosition = positionX, positionY
	# Resets the starting positions
	def resetStartingPosition(self):
		self.positionX, self.positionY = self.startingPosition
	# Moves in direction
	def move(self):
		px, py = self.direction.getDirection()
		self.positionX += int(px)
		self.positionY += int(py)
'''Player class'''
class Player(GameObject):
	def __init__(self, positionX, positionY, name, color: pygame.Color = None, imagePath: str = None, screen=None) -> None:
		super().__init__(positionX, positionY, name, color, imagePath, screen)
		self.direction = Direction(self.image.get_size())
		self.lastRotation = self.direction.rotationDegrees()
		self.startingPosition = positionX, positionY
	# Resets to starting position
	def resetStartingPosition(self):
		self.positionX, self.positionY = self.startingPosition
	# Moves
	def move(self):
		px, py = self.direction.getDirection()
		self.positionX += int(px)
		self.positionY += int(py)
	# Draws
	def draw(self):
		rotation = self.direction.rotationDegrees()
		if self.lastRotation != rotation:
			self.lastRotation = rotation
		if self.image is not None:
			self.imageRectangle = self.image.get_rect(x=self.positionX, y=self.positionY)
			self.screen.blit(pygame.transform.rotate(self.image, rotation), self.imageRectangle)
	# Sets the currect direction
	def right(self): self.direction.currentDirection = self.direction.right
	def left(self): self.direction.currentDirection = self.direction.left
	def up(self): self.direction.currentDirection = self.direction.up
	def down(self): self.direction.currentDirection = self.direction.down
	# Checks collisions
	def checkcollisions(self, obj:GameObject):
		return self.imageRectangle.colliderect(obj.imageRectangle)
'''Wall class'''
class Wall(GameObject):
	def __init__(self, positionX, positionY, name, color: pygame.Color = None, imagePath: str = None, screen=None) -> None:
		super().__init__(positionX, positionY, name, color, imagePath, screen)
		self.imagePath = imagePath
	# Draws
	def draw(self) -> None:
		if self.image is not None:
			self.imageRectangle = self.image.get_rect(x=self.positionX, y=self.positionY)
			self.screen.blit(self.image, self.imageRectangle)
'''Point class'''
class Point(GameObject):
	def __init__(self, positionX:int, positionY:int, name:str, color: pygame.Color = None, imagePath: str = None, type:int=0, screen=None) -> None:
		super().__init__(positionX, positionY, name, color, imagePath, screen)
		self.type = type
		# TODO: Implement boost
		self.boost = True if type > 2 else False
		self.visible = True
		self.none = pygame.image.load('./images/none.png')
	# Draws
	def draw(self) -> None:
		self.imageRectangle = self.image.get_rect(x=self.positionX, y=self.positionY)
		if self.visible:
			self.screen.blit(self.image, self.imageRectangle)
		else:
			self.screen.blit(self.none, self.imageRectangle)
	# Hides the point
	def hide(self):
		self.visible = False
	# Shows the point
	def show(self):
		self.visible = True
'''Blank class'''
class Blank(GameObject):
	def __init__(self, positionX:int=0, positionY:int=0, name:str='', color: pygame.Color = BLACK, imagePath: str = None, screen:pygame.Surface=None) -> None:
		super().__init__(positionX, positionY, name, color, imagePath, screen)
		self.image = pygame.image.load('./images/none.png')

'''Game class'''
class Game():
	# Class constructor
	def __init__(self, windowWidth:int=640, windowHeight:int=480, fps:int=5, mapAsMatrix:list[list]=[]) -> None:
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight

		self.matrix = mapAsMatrix
		self.originalMatrix = np.copy(mapAsMatrix)
		
		self.fps = fps
		
		self.initialize()
		self.initializeObjects()

		self.scene = Scene(self)
		self.scene.initialize()
		
		if TEST:
			self.scene.changeTo(self.scene.inGame)

		self.loadMap(mapAsMatrix2x2=mapAsMatrix)
		self.addToMatrix2x2()

		self.addPlayers()

		self.maximumScore = len(self.points)

		self.paused = True
		self.RUNNING = True
		
	# Initializes objects
	def initializeObjects(self):
		self.player = None
		self.enemies = []
		self.objects = []
		self.points = []
	# Adds players
	def addPlayers(self):
		self.addObject(Player(32*9, 32*7, 'PACMAN', None, './images/pacman.png', self.screen))
		self.addObject(Enemy(32*8, 32*5, 'Ragdolle', None, './images/enemy1.png', self.screen))
		self.addObject(Enemy(32*9, 32*5, 'Oilerov', None, './images/enemy2.png', self.screen))
	# Initializes the game
	def initialize(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
		self.setCaption('HARDCORE Pac-Man @AdamValašťan')
		self.score = 0
	# Sets the window caption
	def setCaption(self, caption:str='') -> None:
		pygame.display.set_caption(caption)
	# Loads the playable map from 2x2 array
	def loadMap(self, mapAsMatrix2x2):		
		matrixWidth = len(mapAsMatrix2x2[0])
		matrixHeight = len(mapAsMatrix2x2)
		wallCharacter = mapAsMatrix2x2[0][0]
		for rowIndex, row in enumerate(mapAsMatrix2x2):
			for columnIndex, value in enumerate(row):
				if value != wallCharacter:
					if value == 1: self.addObject(Point(columnIndex*32, rowIndex*32, 'Point1', None, './images/point1.png', 1, self.screen))
					if value == 2: self.addObject(Point(columnIndex*32, rowIndex*32, 'Point2', None, './images/point2.png', 2, self.screen))
					if value in (8, 9):
						self.addObject(Blank(columnIndex*32, rowIndex*32, 'Nothing', None, './images/none.png', self.screen))
					continue
				""" Wall-detection algorithm """
				imageNumber = 0
				if 0<=columnIndex+1<matrixWidth and mapAsMatrix2x2[rowIndex][columnIndex+1] == wallCharacter: imageNumber += 1
				if 0<=rowIndex-1<matrixHeight and mapAsMatrix2x2[rowIndex-1][columnIndex] == wallCharacter: imageNumber   += 2
				if 0<=columnIndex-1<matrixWidth and mapAsMatrix2x2[rowIndex][columnIndex-1] == wallCharacter: imageNumber += 4
				if 0<=rowIndex+1<matrixHeight and mapAsMatrix2x2[rowIndex+1][columnIndex] == wallCharacter: imageNumber   += 8
				self.addObject(Wall(columnIndex*32, rowIndex*32, 'Wall', None, f'./images/walls/wall{imageNumber}.png', self.screen))
	# Adds an object to belonging arrays
	def addObject(self, gameObject:GameObject):
		if isinstance(gameObject, Player): 	self.player = gameObject
		if isinstance(gameObject, Enemy):	self.enemies.append(gameObject)
		if isinstance(gameObject, Point): 	self.points.append(gameObject)
		if isinstance(gameObject, GameObject): self.objects.append(gameObject)
	# Changes the nxn matrix
	def addToMatrix2x2(self):
		for o in self.objects:
			i:int = o.positionY // o.imageHeight
			j:int = o.positionX // o.imageWidth
			self.matrix[i][j] = o
	# Updates the screen from double buffer
	def update(self):
		pygame.display.flip()
		game.clock.tick(self.fps)
	# Moves the player and checkes the interference with other objects
	def movePlayer(self):
		playerDirection = self.player.direction.currentDirection

		nextX = self.player.positionY // self.player.imageHeight + playerDirection[1]
		nextY = self.player.positionX // self.player.imageWidth + playerDirection[0]
		
		currentX = self.player.positionY // self.player.imageHeight
		currentY = self.player.positionX // self.player.imageWidth
		
		if isinstance(self.matrix[currentX][currentY], Point):
			if self.matrix[currentX][currentY].visible:
				self.score += 1
				self.matrix[currentX][currentY].hide()
		
		for n in self.enemies:
			if self.player.checkcollisions(n):
				self.endCurrentGame()
				return
		
		if isinstance(self.matrix[nextX][nextY], Wall):
			# Don't move
			return
		
		self.player.move()
	# Moves all the enemies and checkes the interference with other objects
	def moveEnemies(self):
		for n in self.enemies:
			n.direction.randomDirection()

			enemyDirection = n.direction.currentDirection

			nextX = n.positionY // n.imageHeight + enemyDirection[1]
			nextY = n.positionX // n.imageWidth + enemyDirection[0]

			if isinstance(self.matrix[nextX][nextY], Wall):
				continue
			if isinstance(self.matrix[nextX][nextY], Enemy):
				continue
			n.move()
	# Checks collisions on all objects
	def checkCollisionOnAllObjects(self):
		for enemy in self.enemies:
			if self.player.checkcollisions(enemy):
				self.endCurrentGame()
	# Draws all the objects
	def draw(self):
		if self.score >= self.maximumScore:
			self.endCurrentGame()
		self.moveEnemies()
		self.movePlayer()
		self.drawAllObjects()
		self.checkCollisionOnAllObjects()
	# Draws all objects
	def drawAllObjects(self):
		for _object in self.objects:
			_object.draw()
	# Draws the current scene
	def drawScene(self):
		self.scene.draw()
	# Pauses the current game
	def pause(self):
		if self.paused:
			self.scene.unpauseScene()
			self.paused = False
			return
		self.scene.pauseScene()
		self.paused = True
	# Exits the current game completely
	def quit(self):
		self.RUNNING = False
	# Ends the current game
	def endCurrentGame(self):
		self.scene.changeTo(self.scene.end)

		self.initializeObjects()
		self.reappearEverything()
		self.loadMap(self.originalMatrix)
		self.addToMatrix2x2()
		self.addPlayers()
		
	# Shows all points
	def reappearEverything(self):
		for obj in self.objects:
			if isinstance(obj, Point):
				obj.show()
		# self.pause()
	# Resets the player position
	def resetMovableObjects(self):
		self.player.resetStartingPosition()
		for enemy in self.enemies: enemy.resetStartingPosition()
		# self.addToMatrix2x2()
	# Resets the score
	def resetScore(self):
		self.score = 0
	# Checks if the current game is on
	def isInGame(self) -> bool:
		return self.scene.current == self.scene.inGame
	# Checks if the current game is paused
	def isPaused(self) -> bool:
		return self.scene.current == self.scene.pause


'''Game creating'''
WINDOW_WIDTH = 32*19
WINDOW_HEIGHT = 32*11
FPS = 10
game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, fps=FPS, mapAsMatrix=standardMapCoordinates)


'''Main event loop'''
while game.RUNNING:
	# Processing events
	for event in pygame.event.get():
		# Check left mouse button click
		if pygame.mouse.get_pressed(3)[0]:
			game.scene.current.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
		# Checks the keys if the game is playing or paused
		if game.isInGame() or game.isPaused():
			# Checks if any key is pressed
			if event.type == pygame.KEYDOWN:
				# Checks if the game should be paused
				if event.key == pygame.K_ESCAPE \
					or event.key == pygame.K_p: game.pause()
				# Moves the player according to arrow keys
				if event.key == pygame.K_RIGHT: game.player.right()
				if event.key == pygame.K_LEFT: 	game.player.left()
				if event.key == pygame.K_UP: 	game.player.up()
				if event.key == pygame.K_DOWN: 	game.player.down()
		# Checks if the game is about to be quitted
		if event.type == pygame.QUIT:
			game.quit()
	# Draws the current scene
	game.drawScene()
	# Update double buffer
	game.update()


'''Quit afterparty'''
# Quits the game
pygame.quit()
# Frees the resources
sys.exit()
