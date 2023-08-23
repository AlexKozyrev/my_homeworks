from random import randint


def move(game_matrix, player_name):  # ход игрока
    incorrect_input = True
    print("Ход игрока который играет за", form_out(player_name))
    while incorrect_input:
        text_inp = input("Введите координаты вашего хода в формате номер ряда номер стобца (Y X):")
        try:
            a, b = map(int, text_inp.split())
            if a in range(3) and b in range(3) and game_matrix[a][b] == -1:
                if player_name == 0:
                    game_matrix[a][b] = 0
                else:
                    game_matrix[a][b] = 1
                incorrect_input = False
            elif game_matrix[a][b] != -1:
                print("Данная клетка поля уже занята")
            else:
                print("Ваш ход за пределами поля")
        except ValueError:
            print("Это не правильный ввод, попробуйте еще раз")
    print_field(game_matrix)
    return game_matrix


def bot_move(game_matrix, bot):  #алгоритм действий бота
    bot_x = -1
    bot_y = -1
    bot_rand_x = -1
    bot_rand_y = -1
    clear = -1
    print("Ходит бот")
    for i in range(3):
        for j in range(3):
            matrix_predict = game_matrix.copy()  #
            if matrix_predict[i][j] == -1:
                clear += 1
                think = randint(0, clear)
                if think == clear:
                    bot_rand_x = i
                    bot_rand_y = j
                matrix_predict[i][j] = 1
                if check_win(matrix_predict, bot, 0):
                    bot_x = i
                    bot_y = j
                matrix_predict[i][j] = -1
                matrix_predict[i][j] = 0
                if check_win(matrix_predict, bot, 0):
                    bot_x = i
                    bot_y = j
                matrix_predict[i][j] = -1
    if bot_x == -1:
        bot_x = bot_rand_x
        bot_y = bot_rand_y

    print("Бот выбрал", bot_x, bot_y)
    game_matrix[bot_x][bot_y] = 1
    print_field(game_matrix)
    return game_matrix


def check_row(a, b, c):  #проверка того, что вся линия заполнена одинаковыми символами
    if a is b and b is c and c != -1:
        return 1
    else:
        return 0


def check_win(game_matrix, player_name, status):  #проверка на победу одного из игроков
    win = 0
    win += check_row(game_matrix[0][0], game_matrix[1][1], game_matrix[2][2])
    win += check_row(game_matrix[0][2], game_matrix[1][1], game_matrix[2][0])
    for i in range(3):
        win += check_row(game_matrix[i][0], game_matrix[i][1], game_matrix[i][2])
        win += check_row(game_matrix[0][i], game_matrix[1][i], game_matrix[2][i])
    if win:
        if status:
            print("Победа игрока, который играл за", form_out(player_name))
        return True
    else:
        return False


def check_end(move_count, matrix, player_id):  #проверка окончания игры и варианта ничьей
    if move_count == 10:
        if not check_win(matrix, player_id, 1):
            print("Ничья")
        return False
    else:
        return True


def form_out(field_point):  #изменение формата вывода элементов
    if field_point == -1:
        return "-"
    elif field_point == 0:
        return "x"
    else:
        return "o"


def print_field(matrix_field):  #вывод игрового поля
    print("  0 1 2")
    row_count = 0
    for row in matrix_field:
        print(row_count, end=" ")
        for x in row:
            print(form_out(x), end=" ")
        row_count += 1
        print()


def game():  # тело игры
    field_matrix = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
    player = 1
    gamemode = 1
    incorrect_input = True
    while incorrect_input:
        text_inp = input(
            "Добро пожаловать в игру крестики-нолики! Введите 1 для режима против игрока, 2 против компьютера")
        try:
            if text_inp == "1":
                gamemode = 1
                incorrect_input = False
            elif text_inp == "2":
                gamemode = 2
                incorrect_input = False
        except ValueError:
            print("Это не правильный ввод, попробуйте еще раз")
    mov_count = 1
    print_field(field_matrix)
    while check_end(mov_count, field_matrix, player) and not check_win(field_matrix, player, 1):
        if player == 0:
            player += 1
            if gamemode == 1:
                move(field_matrix, player)
            else:
                bot_move(field_matrix, player)
        else:
            player -= 1
            move(field_matrix, player)
        mov_count += 1


game()
