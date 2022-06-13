from math import pi, cos, sin, log10, floor
from random import randint
import matplotlib.pyplot as plt
import numpy as np

# Задаем функции и исходные данные
# Функция нахождения катангенса
def ctg(x):
    return (cos(x) / sin (x))

# Функция округления по количесвту значащих цифр
def round_sig(x, sig=3):
    return round(x, sig-int(floor(log10(abs(x))))-1)

# Функция добавления меток значений
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center', \
            bbox = dict(color = 'gray', alpha = 0.75))

# Функция генерации списка псевдослучайных чисел с контролируемым разбросом
def randomizer (minx, maxx, percent=10, n=48):
    # percent - максимальное разлиие между соседними измерениями
    # n - количество измерений
    # minx, maxx - минимальное и максимальное значения
    izmdata = []
    izmdata.append(randint(minx, maxx))
    i = 0
    while len(izmdata) < n:
        minxx = int(izmdata[i] * (1 - percent / 100))
        maxxx = int(izmdata[i] * (1 + percent / 100))
        k = randint(minxx, maxxx)
        if minx <= k <= maxx:
            izmdata.append(k)
            i += 1
    return izmdata

# Функция вычисления абсолютной погрешности результата прямого измерения
def absol_err(x, n = 3):      # x - результат измерения, n - мин. кол. значащих цифр
    oshibka = ''
    if len(str(x)) < n + 1 and not str(x)[0] == '0' and not str(x).find('.') == -1:
        k = '.' + str(n + 2 - len(str(x))) + 'f'
        y = str(format(x, k))
    elif len(str(x)) < n and not str(x)[0] == '0' and str(x).find('.') == -1:
        k = '.' + str(n - len(str(x))) + 'f'
        y = str(format(x, k))
    elif len(str(x)) < n + 1 and str(x)[0] == '0':
        k = '.' + str(n + 3 - len(str(x))) + 'f'
        y = str(format(x, k))
    else:
        y = str(x)
    for i in range(len(y)):
        if y[i] != '.' and i != len(y) - 1:
            oshibka += '0'
        elif y[i] == '.':
            oshibka += '.'
        else:
            oshibka += '1'
    return float(oshibka)

d = 0.500                    # диаметр проточной части расходомера, м
alpha = round(pi / 4, 4)     # угол между осью трубопровода и вектором УЗС, рад
Lk = 0.025                   # длина пути УЗС в карманах ПЭП, м
T1 = 4.85944e-4              # время распространения УЗС по потоку, с
T2 = 4.90218e-4              # время распространения УЗС против потока, с
pl = 845.0                   # плотность нефти, кг/(м**3)
nu = 0.05                    # динамическая вязкость, Па*с
err = 1                      # ошибка итераций
errnorm = 1e-4               # допустимая относительная разность между итерациями
imax = 1000                  # допустимое количество итераций
i = 0                        # номер итерации
Re = 1e4                     # начальное число Рейнольдса

# Определяем значение массового расхода на основании исходных данных с помошью метода итераций



