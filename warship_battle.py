import random


class BoardOutException(Exception):
    pass


class Dot:  # класс точки с координатами
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:  # класс корабль
    def __init__(self, bow, length, direction):
        self.bow = bow
        self.length = length
        self.direction = direction
        self.lives = length

    def dots(self):  # возвращает точки, которые занимает корабль
        ship_dots = []
        for i in range(self.length):
            x, y = self.bow.x, self.bow.y
            if self.direction == 0:
                x += i
            else:
                y += i
            ship_dots.append(Dot(x, y))
        return ship_dots


class Board:  # класс игрового поля
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]
        self.ships = []
        self.contour_dots = []
        self.shots = []

    def add_ship(self, ship):  # добавление корабля на поле
        for dot in ship.dots():
            if self.out(dot) or dot in [d for s in self.ships for d in s.dots()] or dot in self.contour_dots:
                raise BoardOutException()
        for dot in ship.dots():
            self.field[dot.x][dot.y] = "■"
            self.ships.append(ship)
            self.contour(dot)

    def contour(self, ship_dot, verb=False):  # проверка окружающих точек на наличие корабля
        near = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 0),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for x, y in near:
            cur = Dot(ship_dot.x + x, ship_dot.y + y)
            if not (self.out(cur)) and cur not in [d for s in self.ships for d in
                                                   s.dots()] and cur not in self.contour_dots:
                if verb:
                    self.field[cur.x][cur.y] = "."
                self.contour_dots.append(cur)

    def out(self, dot):  # проверка нахождения точки в границах доски
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def shot(self, dot):  # выстрел в точку
        if self.out(dot):
            raise BoardOutException()

        if dot in self.shots:
            raise ValueError()

        self.shots.append(dot)

        for ship in [s for s in self.ships if isinstance(s, Ship)]:
            if dot in ship.dots():
                ship.lives -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship_dot=ship.bow, verb=True)
                    print("Корабль потоплен!")
                    return False
                else:
                    print("Попадание!")
                    return True

        self.field[dot.x][dot.y] = "Т"
        print("Мимо.")
        return False

    def __str__(self):  # вывод доски на экран
        res = ""
        res += " | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1}| {' | '.join(row)} |"
        if self.hid:
            res = res.replace("■", "O")
        return res


class Player:  # базовый класс родитель для игроков
    def __init__(self, board: Board, enemy: Board):
        self.board = board
        self.enemy = enemy

    def ask(self):  # будет определен в наследниках
        raise NotImplementedError()

    def move(self):  # запрос выстрела и отправка координат на вражеское поле
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardOutException:
                print("Выстрел за пределами поля")
            except ValueError:
                print("В эту клетку уже стреляли")


class AI(Player):  # наследник класса игрок с переопределением метода ask для компьютера
    def ask(self):
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        return Dot(x, y)


class User(Player):  # наследник класса игрок с переопределением метода ask для игрока
    def ask(self):
        while True:
            try:
                cords = input("Введите координаты: ").split()
                if len(cords) != 2:
                    raise ValueError
                x, y = cords
                if not (x.isdigit()) or not (y.isdigit()):
                    raise ValueError
                x, y = int(x), int(y)
                return Dot(x - 1, y - 1)
            except ValueError:
                print("Неверный ввод, введите 2 числа")


class Game:  # класс игровой логики
    def __init__(self, size=6):
        self.size = size
        user = self.random_board()
        ai = self.random_board()
        ai.hid = True
        self.ai = AI(ai, user)
        self.user = User(user, ai)

    def random_board(self):  # создание случайной доска
        board = None
        while board is None:  # Повторять, пока доска не создана успешно
            board = self.create_board()
        return board

    def create_board(self):  # создать доску с нужным количеством кораблей
        board = Board(size=self.size)
        attempts = 0
        num_ships = {3: 1, 2: 2, 1: 4}  # словарь с количеством кораблей каждой длины
        for length in reversed(range(1, 4)):
            for _ in range(num_ships[length]):
                while True:
                    attempts += 1
                    if attempts > 5000:
                        return None
                    x = random.randint(0, self.size - 1)
                    y = random.randint(0, self.size - 1)
                    direction = random.choice([0, 1])
                    ship = Ship(Dot(x, y), length, direction)
                    try:
                        board.add_ship(ship)
                        break
                    except BoardOutException:
                        pass
        return board

    def greet(self):
        print("Игра МОРСКОЙ БОЙ")
        print("Уничтожьте корабли соперника первым чтобы победить, вводя координаты выстрела во время своего хода")
        print("Формат ввода координат своего выстрела: x y")
        print("x - номер строки (от 1 до 6)")
        print("y - номер колонки (от 1 до 6)")

    def loop(self):
        num = 0
        while True:
            if num % 2 == 0:
                print("Ваш ход")
                print("Поле игрока:")
                print(self.user.board)
                print(" ")
                print("Поле компьютера:")
                print(self.ai.board)
                repeat = self.user.move()
            else:
                print("Ход компьютера")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("Вы победили!!!")
                break

            if self.user.board.count == 7:
                print("Компьютер выиграл")
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()


Game().start()
