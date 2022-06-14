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

# Функция расчета коэффициента гидравлического сопротивления
def gidro_kef(x, y=0.5):     # x - значение Re, y - значение диаметра трубопровода
    # считаем, что трубы новые сварные стальные
    asperity = 0.05 / (y * 1000)
    if x < 2300:
        return (64 / x)
    elif 2300 < x < (10 / asperity):
        return (0.3164 * (x ** (-0.25)))
    elif (10 / asperity) < x < (500 / asperity):
        return (0.11 * (((68 / x) + asperity) ** 0.25))
    else:
        return (0.11 * (asperity ** 0.25))

d = 0.500                    # диаметр проточной части расходомера, м
alpha = round(pi / 4, 4)     # угол между осью трубопровода и вектором УЗС, рад
Lk = 0.025                   # длина пути УЗС в карманах ПЭП, м
Lpp = round((d / sin(alpha) \
    + Lk), 3)                # общая длина пути УЗС, м
T1 = 4.85944e-4              # время распространения УЗС по потоку, с
T2 = 4.90218e-4              # время распространения УЗС против потока, с
dT = round(T2-T1, 9)         # разность времен распространения, с
Tsr = round((T1+T2) / 2, 9)  # среднее время распространения УЗС, с
pl = 845.0                   # плотность нефти, кг/(м**3)
nu = 0.05                    # динамическая вязкость, Па*с
err = 1                      # ошибка итераций
errnorm = 1e-4               # допустимая относительная разность между итерациями
imax = 1000                  # допустимое количество итераций
i = 0                        # номер итерации
Re = 1e4                     # начальное число Рейнольдса

# Определяем значение массового расхода на основании исходных данных с помошью метода итераций
while err > errnorm:
    qm1 = round(((((d / sin(alpha)) + Lk) ** 2) * (d ** 2) * pl * pi * dT) / ((8 + 3.6 \
        * (gidro_kef(Re) ** 0.5)) * d * ctg(alpha) * T1 * T2), 4)
    Re = round((4 * qm1) / (pi * nu * d), 0)
    qm = round(((((d / sin(alpha)) + Lk) ** 2) * (d ** 2) * pl * pi * dT) / ((8 + 3.6 \
        * (gidro_kef(Re) ** 0.5)) * d * ctg(alpha) * T1 * T2), 4)
    err = abs((qm - qm1) / qm)
    i += 1
Kg = round(1 + 0.45 * (gidro_kef(Re) ** 0.5), 2)
qm = round_sig(qm)
if qm - int(qm) == 0:
    qm = int(qm)
print('Массовый расход для начальных условий составляет: ' + str(qm) + ' кг/с')

# Определяем относительную погрешность расчета массового расхода как результата косвенного измерения
dqm = round((4 * ((absol_err(Lpp, 3) / Lpp)**2) + 4 * ((absol_err(d, 3) / d)**2) \
    + ((absol_err(pl, 4) / pl)**2) + ((absol_err(dT, 4) / dT)**2) + \
        ((absol_err(Kg, 3) / Kg)**2) + 4 * ((absol_err(Tsr, 9) / Tsr)**2) + \
            2 * ((absol_err(alpha, 4)) ** 2) * ((3 + cos(4 * alpha)) / (1 - \
                cos(4 * alpha))))**0.5, 4)
print('Относительная погрешность расчета массового расхода: ' + str(round_sig(dqm * 100, 4)) + ' %')

