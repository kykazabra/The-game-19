import numpy as np


# Функция, которая проверяет коректность введенных данных
def pos_check_np(p1, p2, gf):
    x1 = p1[0] - 1
    y1 = p1[1] - 1
    x2 = p2[0] - 1
    y2 = p2[1] - 1

    if gf[x1,y1] == 0 or gf[x2,y2] == 0: return ('impossible') # Проверка, не являются ли элементы вычеркнутыми
    if x1 == x2 and y1 == y2: return ('impossible') # Проверка, не введены ли 2 раза одинаковые координаты
    if not(x1 == x2 or y1 == y2): return ('impossible') # Проверка, совпадает ли хотябы одна координата
    if gf[x1, y1] + gf[x2, y2] != 10 and gf[x1, y1] != gf[x2, y2]: return ('impossible')  # Проверка на выполнение условий вычеркивания
    rng_x = abs(x1 - x2)
    rng_y = abs(y1 - y2)
    if (rng_x == 0 and rng_y == 1) or (rng_x == 1 and rng_y == 0): return ('possible') # Проверка, находятся ли элементы в соседних клетках
    x_max = max(x1, x2)
    x_min = min(x1, x2)
    y_max = max(y1, y2)
    y_min = min(y1, y2)
    if rng_x == 0 or rng_y == 0: # Цикл проверки в случае, если между элементами расположены зачеркнутые
        flag = 1
        if rng_y == 0: # Проверка, если совпадает столбец
            for i in range(x_min + 1, x_max):
                if gf[i,y1] != 0: flag = 0
        if rng_x == 0: # Проверка, если совпадает строка
            for i in range(y_min + 1, y_max):
                if gf[x1,i] != 0: flag = 0
        if flag == 1:
            return ('possible')
        else:
            return ('impossible')
    else:
        return ('impossible')

#Функция, которая проверяет, наступил ли конец раунда путем подсчета возможных ходов
def round_end_np(gf):
    flag = 0
    for i in range(gf.shape[0]): # Цикл проверки по строкам
        b = gf[i, :] # Извлечение i-той строки
        c = b[b != 0] # Удаление всех нулей из строки
        for j in range(c.shape[0] - 1): # Проверка на возможность нахождения пар
            if c[j] + c[j + 1] == 10 or c[j] == c[j + 1]: flag += 1

    for i in range(gf.shape[1]): # Цикл проверки по столбцам
        b = gf[:, i] # Извлечение j-того столбца
        c = b[b != 0]
        for j in range(c.shape[0] - 1):
            if c[j] + c[j + 1] == 10 or c[j] == c[j + 1]: flag += 1

    if flag:
        return ('in')
    else:
        return ('end')

# Функция, обновляющая игровое поле после конца хода
def rewrite_np(gf):
    global tail #Колличество нулей, дописанных в конец в прошлом раунде
    a = gf.ravel()[: gf.ravel().shape[0] - tail]  # Одномерный массив из исходного без дописанных в предыдущем раунде нулей
    b = gf[gf != 0] # Создание новой части поля - одномерный массив из исходого без зачеркнутых ячеек
    c = np.append(a, b)
    tail = (9 - (c.shape[0] % 9)) % 9
    # Добавление в него недостающего колличества пустых элементов для выравнивания до кратности 9 и возврат старого поля вместе с новой частью
    return (np.append(c, np.zeros(tail, dtype=int)).reshape(-1,9))

#Функция, которая выводит игровое поле
def printing_np(gf):
    print('.  . ', end = '')
    for i in range(1, 10): print(i, end=' . ')
    print();
    print('. ', '━'*37) # Разделитель
    for j in range(gf.shape[0]):
        print(j+1, ' | ', end='') # Числовая сетка
        for i in range(gf.shape[1]):
            print(gf[j,i] if gf[j,i] > 0 else '■',  end=' | ')
            # Вывод и замена '0' на '■' элемента
        print()
        print('. ', '━'*37)


# Основная функция

str1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
str2 = [1, 1, 1, 2, 1, 3, 1, 4, 1]
str3 = [5, 1, 6, 1, 7, 1, 8, 1, 9]
gfnp = np.array([str1, str2, str3]) # Начальное игровое поле


tail = 0

printing_np(gfnp)
in_game = 'in' # Установка состояния 'в игре'
while in_game != 'end':
    in_round = 'in' # Установка состояния 'в раунде'
    count = 0
    while in_round != 'end':
        p1 = input('Введите координаты 1 цифры (строка, столбец через пробел): ')
        p2 = input('Введите координаты 2 цифры (строка, столбец через пробел): ')
        if p1 == 'end' or p2 == 'end': # Проверка, не хочет ли пользователь принудительно завершить игру
            print()
            print('Игра окончена')
            exit() # Принудительное завершение программы
        print()
        p1 = p1.split()
        p2 = p2.split()
        # Далее идет блок проверки корректности введенных данных
        is_ok = 'ok'
        if len(p1) != 2 and len(p2) != 2: # Проверка, 2 ли числа в каждой строке
            is_ok = 'not_ok'
        if p1[0].isdigit() and p1[1].isdigit() and p2[0].isdigit() and p2[1].isdigit(): # Проверка, числа ли введены
            p1 = list(map(int, p1))
            p2 = list(map(int, p2))
            if (p1[1] < 1 or p1[1] > 9) or (p2[1] < 1 or p2[1] > 9) or (p1[0] < 1 or p1[0] > gfnp.shape[0]) or (p2[0] < 1 or p2[0] > gfnp.shape[0]): # Проверка, находятся ли числа в нужном диапазоне
                is_ok = 'not_ok'
        else: is_ok = 'not_ok'
        if is_ok == 'not_ok': print('Ввод некорректен, повторите попытку')
        else:
            if pos_check_np(p1, p2, gfnp) == 'possible': # Зачеркивание выбраных элементов, если это возможно
                gfnp[p1[0] - 1, p1[1] - 1] = 0
                gfnp[p2[0] - 1, p2[1] - 1] = 0
                printing_np(gfnp) # Вывод нового состояния поля
            else:
                print('Ввод некорректен, повторите попытку')
            in_round = round_end_np(gfnp) # Проверка, есть ли еще возможные ходы, или можно заканчивать раунд

    gfnp = rewrite_np(gfnp) # Переписывание поля
    print('Раунд завершен, перерисовываю поле...')
    print()
    printing_np(gfnp)
    if round_end_np(gfnp) == 'end': in_game = 'end' # Проверка, есть ли еще ходы в новом поле, или можно заканчивать игру

print()
print('Игра окончена')