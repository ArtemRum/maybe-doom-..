import random

def generate_maze(width, height):
    # Создаем пустую карту
    maze = [[0 for _ in range(width)] for _ in range(height)]
    
    
    # Генерируем полностью связанный граф клеток
    divide(maze, 1, 1, width-2, height-2)
    
    
    
    # Удаляем лишние стены, чтобы соответствовать условию не более двух единиц вокруг нуля
    for i in range(height-1):
        for j in range(width-1):
            if maze[i][j] == 0:
                if count_surrounding_walls(maze, i, j) > 2:
                    remove_excess_walls(maze, i, j)
    
    for i in range(width):
        maze[0][i] = 1
        maze[height-1][i] = 1
    for i in range(height):
        maze[i][0] = 1
        maze[i][width-1] = 1
    # Установка стартовой и конечной точек
    maze[1][0] = 2
    maze[height-2][width-1] = 3
    return maze

def divide(maze, x, y, width, height):
    if width < 3 or height < 3:
        return
    
    if width < height:
        split_horizontally(maze, x, y, width, height)
    elif height < width:
        split_vertically(maze, x, y, width, height)
    else:
        if random.choice([True, False]):
            split_horizontally(maze, x, y, width, height)
        else:
            split_vertically(maze, x, y, width, height)

def split_horizontally(maze, x, y, width, height):
    try:
        divide_point = random.randint(2, height-2)
    except ValueError:
        divide_point = 2
    passage = random.randint(x + 1, x + width - 1)
    for i in range(x, x + width + 1):
        maze[y + divide_point][i] = 1
    maze[y + divide_point][passage] = 0  # Соединяем клетки
    # Гарантируем связность
    adjacent_passage = random.randint(y, y + divide_point - 1)
    maze[adjacent_passage][passage] = 0
    adjacent_passage = random.randint(y + divide_point + 1, y + height)
    maze[adjacent_passage][passage] = 0
    divide(maze, x, y, width, divide_point - 1)
    divide(maze, x, y + divide_point + 1, width, height - divide_point - 1)

def split_vertically(maze, x, y, width, height):
    try:
        divide_point = random.randint(2, width-2)
    except ValueError:
        divide_point = 2
    passage = random.randint(y + 1, y + height - 1)
    for i in range(y, y + height + 1):
        maze[i][x + divide_point] = 1
    maze[passage][x + divide_point] = 0  # Соединяем клетки
    # Гарантируем связность
    adjacent_passage = random.randint(x, x + divide_point - 1)
    maze[passage][adjacent_passage] = 0
    adjacent_passage = random.randint(x + divide_point + 1, x + width)
    maze[passage][adjacent_passage] = 0
    divide(maze, x, y, divide_point - 1, height)
    divide(maze, x + divide_point + 1, y, width - divide_point - 1, height)

def count_surrounding_walls(maze, x, y):
    count = 0
    if maze[x+1][y] == 1:
        count += 1
    if maze[x-1][y] == 1:
        count += 1
    if maze[x][y+1] == 1:
        count += 1
    if maze[x][y-1] == 1:
        count += 1
    return count

def remove_excess_walls(maze, x, y):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze)-1 and 0 <= ny < len(maze[0])-1 and maze[nx][ny] == 1:
            maze[nx][ny] = 0
            break

# Генерация лабиринта размером 32x12
maze = generate_maze(32, 12)
print(*maze, sep='\n')