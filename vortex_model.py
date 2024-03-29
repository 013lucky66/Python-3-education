from math import pi, log10, floor
from random import randint
import matplotlib.pyplot as plt
import numpy as np
# Метрологическая модель вихревого расходомера с теолм обтекания в проточной части

# Задаем функции и исходные данные 
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

# Функция вычисления относительной погрешности результата прямого измерения вида dx / x
def otn_err(x, n=3):   # x - результат измерения, n - мин. кол. значащих цифр
    oshibka = ''
    if x < 1:
        while x < 1:
            x *= 10
            x = round_sig(x, n)
    if x - int(x) == 0:
        x = int(x)
        if len(str(x)) < n:
            k = '.' + str(n - len(str(x))) + 'f'
            y = str(format(x, k))
        else:
            y = str(x)
    else:
        k = '.' + str(n - 1) + 'f'
        y = str(format(x, k))
    for i in range(len(y)):
        if y[i] != '.' and i != len(y) - 1:
            oshibka += '0'
        elif y[i] == '.':
            oshibka += '.'
        else:
            oshibka += '1'
    return float(oshibka) / (round_sig(x, n))

d = 0.300         # диаметр проточной части расходомера, м
f = 150           # частота вихреобразования, Гц
pl = 845.0        # плотность нефти, кг/(м**3)
nu = 0.05         # динамическая вязкость, Па*с
err = 1           # ошибка итераций
errnorm = 1e-4    # допустимая относительная разность между итерациями
imax = 1000       # допустимое количество итераций
i = 0             # номер итерации
Re = 1e4          # начальное число Рейнольдса

# Определяем значение массового расхода на основании исходных данных с помошью метода итераций
while err > errnorm:
    if Re < 2300:
        qm1 = round((f * pl * (d ** 3)) / (1.3356 * (1 - (21.2 / Re))), 4)
    else:
        qm1 = round((f * pl * (d ** 3)) / (1.3356 * (1 - (12.7 / Re))), 4)
    Re = round((4 * qm1) / (pi * nu * d), 0)
    if Re < 2300:
        qm = round((f * pl * (d ** 3)) / (1.3356 * (1 - (21.2 / Re))), 4)
    else:
        qm = round((f * pl * (d ** 3)) / (1.3356 * (1 - (12.7 / Re))), 4)
    err = abs((qm - qm1) / qm)
    i += 1
if Re < 2300:
        St = round_sig(0.212 * (1 - 21.2 / Re), 3)
else:
    St = round_sig(0.212 * (1 - 12.7 / Re), 3)
qm = round_sig(qm)
if qm - int(qm) == 0:
    qm = int(qm)
print('Массовый расход для начальных условий составляет: ' + str(qm) + ' кг/с')

# Определяем относительную погрешность расчета массового расхода как результата косвенного измерения
dqm = round((((otn_err(f, len(str(f))))**2) + ((otn_err(pl, 4))**2) + 9 * ((otn_err(d, 3))**2) + \
    ((otn_err(St, 3))**2))**0.5, 4)
print('Относительная погрешность расчета массового расхода: ' + str(round_sig(dqm * 100, 4)) + ' %')

# Строим диаграмму относительных погрешностей составляющих результирующей погрешности
spisok_err = [round(otn_err(f, len(str(f))) * 1e2, 4), round(otn_err(pl, 4) * 1e2, 4), \
    round(otn_err(d, 3) * 1e2, 4), round(otn_err(St, 3) * 1e2, 4)]
nazv = ['f', 'pl', 'd', 'St']
fig1 = plt.figure('Диаграмма погрешностей вихревого расходомера', figsize = (8, 5))
plt.grid(True, alpha = 0.3)
plt.bar(nazv, spisok_err)
addlabels(nazv, spisok_err)
plt.ylabel('Относительная погрешность, %', {'fontname':'Times New Roman'}, fontweight='normal', \
    fontsize=14)

# Строим расходограмму
# Определяем значения расхода
fdin = randomizer(10, 270)
spisok_qm = []
errdin = 1
Re2 = 1e4
for element in fdin:
    while errdin > errnorm:
        if Re2 < 2300:
            qm1 = round((element * pl * (d ** 3)) / (1.3356 * (1 - (21.2 / Re2))), 4)
        else:
            qm1 = round((element * pl * (d ** 3)) / (1.3356 * (1 - (12.7 / Re2))), 4)
        Re2 = round((4 * qm1) / (pi * nu * d), 0)
        if Re2 < 2300:
            qm = round((element * pl * (d ** 3)) / (1.3356 * (1 - (21.2 / Re2))), 4)
        else:
            qm = round((element * pl * (d ** 3)) / (1.3356 * (1 - (12.7 / Re2))), 4)
        errdin = abs((qm - qm1) / qm)
    spisok_qm.append(round_sig(qm * 3.6, 3))
    errdin = 1
    Re2 = 1e4
# Вычисляем накопленный расход
m = 0
for i in range(1, len(spisok_qm)):
    m += round(0.5 * 0.5 * (spisok_qm[i] + spisok_qm[i - 1]), 3)
# Строим график
t = np.linspace(0, 24, 48)
fig2 = plt.figure('Суточная расходограмма вихревого расходомера', figsize = (10, 5))
plt.ylim(0, 17000)
plt.xlim(0, 24)
plt.grid(True, alpha = 0.3)
plt.xlabel('Время, ч', {'fontname':'Times New Roman'}, fontweight='normal', fontsize=14)
plt.ylabel('Массовый расход, т/ч', {'fontname':'Times New Roman'}, fontweight='normal', fontsize=14)
plt.plot(t, spisok_qm)
plt.fill_between(t, spisok_qm, color = 'gray', alpha = 0.2)
plt.text(10, 1000, str(m) + ' т', fontsize=16, bbox=dict( color='gray', alpha = 0.5))

# Строим график изменеия погрешностей в зависимости от расхода
# Определяем значения величин
fdin = [s for s in range(10, 270, 5)]
spisok_qm = []
Stdin = []
errdin = 1
Re2 = 1e3
for element in fdin:
    while errdin > errnorm:
        if Re2 < 2300:
            qm1 = round((element * pl * (d ** 3)) / (1.3356 * (1 - (21.2 / Re2))), 4)
        else:
            qm1 = round((element * pl * (d ** 3)) / (1.3356 * (1 - (12.7 / Re2))), 4)
        Re2 = round((4 * qm1) / (pi * nu * d), 0)
        if Re2 < 2300:
            qm = round((element * pl * (d ** 3)) / (1.3356 * (1 - (21.2 / Re2))), 4)
        else:
            qm = round((element * pl * (d ** 3)) / (1.3356 * (1 - (12.7 / Re2))), 4)
        errdin = abs((qm - qm1) / qm)
    spisok_qm.append(round_sig(qm, 3))
    if Re < 2300:
        Stdin.append(round_sig(0.212 * (1 - 21.2 / Re), 3))
    else:
        Stdin.append(round_sig(0.212 * (1 - 12.7 / Re), 3))
    errdin = 1
    Re2 = 1e4
# Вычисляем погрешности
dfdin = [(otn_err(s, len(str(s)))) * 100 for s in fdin]
dStdin = [(otn_err(s, 3)) * 100 for s in Stdin]
# Строим график
fig3 = plt.figure('График погрешностей вихревого расходомера', figsize = (10, 5))
plt.xlim(spisok_qm[0], spisok_qm[47])
plt.ylim(0, 11)
plt.grid(True, alpha = 0.3)
plt.xlabel('Расход, кг/с', {'fontname':'Times New Roman'}, fontweight='normal', fontsize=14)
plt.ylabel('Относительная погрешность, %', {'fontname':'Times New Roman'}, fontweight='normal', fontsize=14)
plt.plot(spisok_qm, dfdin, linewidth = '3', linestyle = 'solid', label='Погрешность детектирования вихрей')
plt.plot(spisok_qm, dStdin, linewidth = '3', linestyle = 'dashed', label='Погрешность определения числа Струхаля')
plt.legend(loc='best')
plt.show()