import time, keyboard, random, sys, os

WIDTH, HEIGHT = 60, 25
FOOD, POINT, SNAKE, BORDER = 'F', ' ', '#', "@"
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __iadd__(self, obj):
        if isinstance(obj, Position):
            self.x += obj.x
            self.y += obj.y
        return self
    def __eq__(self, obj):
        if self.x == obj.x and self.y == obj.y:
            return True
        return False
    def __str__(self):
        return f"Position({self.x}, {self.y})"

class Node:
    def __init__(self):
        self.position = Position()
        self.next = None
    def setPosition(self, x, y):
        self.position.x = x
        self.position.y = y

def initGrid():
    grid = []
    for _ in range(WIDTH):
        pos = []
        for _ in range(HEIGHT):
            pos.append(POINT)
        grid.append(pos)
    return grid

def displayGrid(grid, score):
    buffer = "Score: " + str(score) + "\n\n"
    buffer += BORDER * (WIDTH+2) + "\n"
    for y in range(HEIGHT):
        buffer += BORDER
        for x in range(WIDTH):
            buffer += grid[x][y]
        buffer += BORDER + "\n"
    buffer += BORDER * (WIDTH+2) + "\n"
    sys.stdout.write(buffer)
    sys.stdout.flush()

def updateGrid(grid, nodes, foods):
    for node in nodes: 
        grid[node.position.x][node.position.y] = SNAKE
    for food in foods.list: 
        grid[food.x][food.y] = FOOD

def clearGrid(grid):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            grid[x][y] = POINT

class Foods:
    def __init__(self, foodsn=1):
        self.list = []
        self.foodsn = foodsn
    def fill(self):
        while len(self.list) < self.foodsn:
            self.list.append(Position(random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)))
    def checkCollision(self, pos):
        collided = []
        for food in self.list:
            if pos == food:
                collided.append(food)
        return collided

class Snake:
    def __init__(self, headx, heady):
        self.nodes = []
        self.extend(headx, heady)
        self.head = self.nodes[0]
        self.dir = RIGHT
        self.extend(headx-self.dir[0], heady-self.dir[1])
        self.extend(headx-self.dir[0]*2, heady-self.dir[1]*2)
    def extend(self, x=0, y=0):
        node = Node()
        node.setPosition(x, y)
        self.nodes.append(node)
    def update(self):
        for index in range(len(self.nodes)-1, 0, -1):
            self.nodes[index].setPosition(self.nodes[index-1].position.x, self.nodes[index-1].position.y)
    def movement(self):
        if self.dir == RIGHT:
            self.head.position += Position(1, 0)
        elif self.dir == LEFT:
            self.head.position += Position(-1, 0)
        elif self.dir == DOWN:
            self.head.position += Position(0, 1)
        elif self.dir == UP:
            self.head.position += Position(0, -1)
    def checkBound(self):
        if self.head.position.x > WIDTH-1:
            self.head.setPosition(0, self.head.position.y)
        if self.head.position.y > HEIGHT-1:
            self.head.setPosition(self.head.position.x, 0)
        if self.head.position.x < 0:
            self.head.setPosition(WIDTH-1, self.head.position.y)
        if self.head.position.y < 0:
            self.head.setPosition(self.head.position.x, HEIGHT-1)
    def controls(self):
        if keyboard.is_pressed('A') or keyboard.is_pressed('left'):
            if snake.dir[0] != 1: snake.dir = LEFT
        elif keyboard.is_pressed('D') or keyboard.is_pressed('right'):
            if snake.dir[0] != -1: snake.dir = RIGHT
        elif keyboard.is_pressed('W') or keyboard.is_pressed('up'):
            if snake.dir[1] != 1: snake.dir = UP
        elif keyboard.is_pressed('S') or keyboard.is_pressed('down'):
            if snake.dir[1] != -1: snake.dir = DOWN

if __name__=="__main__":
    grid = initGrid()
    clear = "cls" if sys.platform == "win32" else "clear"
    score = 0
    snake = Snake(2, 0)
    foods = Foods()
    foods.fill()
    running = True
    while running:
        if keyboard.is_pressed('Space'):
            snake.extend()
        elif keyboard.is_pressed('Escape'):
            running = False
        snake.controls()
        snake.update()
        snake.movement()
        snake.checkBound()
        for index in range(len(snake.nodes)):
            if index != 0:
                if snake.head.position == snake.nodes[index].position:
                    running = False
                    break
        collided = foods.checkCollision(snake.head.position)
        if len(collided) != 0:
            for food in collided:
                foods.list.remove(food)
                foods.fill()
                snake.extend(snake.nodes[-1].position.x, snake.nodes[-1].position.y)
                score += 1
        updateGrid(grid, snake.nodes, foods)
        os.system(clear)
        displayGrid(grid, score)
        clearGrid(grid)
        time.sleep(0.1)