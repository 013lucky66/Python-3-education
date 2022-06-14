from math import pi, cos, sin, tan, log10, floor
from random import uniform
import matplotlib.pyplot as plt
import numpy as np
# Метрологическая модель времяимпульсного УЗР

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
    #l = len(str(minx)[str(minx).find('.') + 1:])
    izmdata.append(uniform(minx, maxx))
    i = 0
    while len(izmdata) < n:
        minxx = izmdata[i] * (1 - percent / 100)
        maxxx = izmdata[i] * (1 + percent / 100)
        k = uniform(minxx, maxxx)
        if minx <= k <= maxx:
            izmdata.append(k)
            i += 1
    return izmdata

# Функция вычисления абсолютной погрешности результата прямого измерения (от 1e-5)
def absol_err(x, n = 3):      # x - результат измерения, n - мин. кол. значащих цифр
    oshibka = ''
    if x - int(x) == 0:
        x = int(x)
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
dqm = round((4 * (otn_err(Lpp, 3)**2) + 4 * (otn_err(d, 3)**2) + (otn_err(pl, 4)**2) + \
    (otn_err(dT, 3)**2) + (otn_err(Kg, 3)**2) + 4 * (otn_err(Tsr, 9)**2) + \
            2 * ((absol_err(alpha, 4)) ** 2) * ((3 + cos(4 * alpha)) / (1 - cos(4 * alpha))))**0.5, 4)
print('Относительная погрешность расчета массового расхода: ' + str(round_sig(dqm * 100, 4)) + ' %')

# Строим диаграмму относительных погрешностей составляющих результирующей погрешности
spisok_err = [round(otn_err(Lpp, 3) * 1e2, 4), round(otn_err(d, 3) * 1e2, 4), \
    round(otn_err(pl, 4) * 1e2, 4), round(otn_err(dT, 3) * 1e2, 4), \
        round(otn_err(Kg, 3) * 1e2, 4), round(otn_err(Tsr, 9) * 1e2, 4), \
             round((absol_err(alpha, 3) * ((ctg(alpha)) ** 2 +(tan(alpha)) ** 2)) * 1e2, 4)]


nazv = ['Lпп', 'd', 'pl', 'dT', 'Kg', 'T', 'alpha']
fig1 = plt.figure('Диаграмма погрешностей УЗР', figsize = (10, 5))
plt.grid(True, alpha = 0.3)
plt.bar(nazv, spisok_err)
addlabels(nazv, spisok_err)
plt.ylabel('Относительная погрешность, %', {'fontname':'Times New Roman'}, fontweight='normal', \
    fontsize=14)

# Строим расходограмму
# Определяем значения расхода
T1din = randomizer(4.83836e-4, 4.88007e-4)
dTdin = randomizer(1e-7, 8.5e-6)
T2din = []
for i in range(len(T1din)):
    T2din.append(round(T1din[i] + dTdin[i], 9))
spisok_qm = []
errdin = 1
Re2 = 1e4
for i in range(len(T1din)):
    while errdin > errnorm:
        qm1 = round(((((d / sin(alpha)) + Lk) ** 2) * (d ** 2) * pl * pi * dTdin[i]) / ((8 + 3.6 \
            * (gidro_kef(Re) ** 0.5)) * d * ctg(alpha) * T1din[i] * T2din[i]), 4)
        Re = round((4 * qm1) / (pi * nu * d), 0)
        qm = round(((((d / sin(alpha)) + Lk) ** 2) * (d ** 2) * pl * pi * dTdin[i]) / ((8 + 3.6 \
            * (gidro_kef(Re) ** 0.5)) * d * ctg(alpha) * T1din[i] * T2din[i]), 4)
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
fig2 = plt.figure('Суточная расходограмма УЗР', figsize = (10, 5))
plt.ylim(0, 15000)
plt.xlim(0, 24)
plt.grid(True, alpha = 0.3)
plt.xlabel('Время, ч', {'fontname':'Times New Roman'}, fontweight='normal', fontsize=14)
plt.ylabel('Массовый расход, т/ч', {'fontname':'Times New Roman'}, fontweight='normal', fontsize=14)
plt.plot(t, spisok_qm)
plt.fill_between(t, spisok_qm, color = 'gray', alpha = 0.2)
plt.text(10, 1000, str(m) + ' т', fontsize=16, bbox=dict( color='gray', alpha = 0.5))

# Строим график изменеия погрешностей в зависимости от расхода
# Определяем значения величин
T1din = []
for i in range(48):
    T1din.append(round(4.83836e-4 + i * 8.67e-8, 9))
dTdin = []
for i in range(48):
    dTdin.append(round(1e-7 + i * 1.75e-7, 9))
T2din = []
for i in range(48):
    T2din.append(round(T1din[i] + dTdin[i], 9))
errdin = 1
Re2 = 1e4
spisok_qm = []
Kgdin = []
for i in range(len(T1din)):
    while errdin > errnorm:
        qm1 = round(((((d / sin(alpha)) + Lk) ** 2) * (d ** 2) * pl * pi * dTdin[i]) / ((8 + 3.6 \
            * (gidro_kef(Re) ** 0.5)) * d * ctg(alpha) * T1din[i] * T2din[i]), 4)
        Re = round((4 * qm1) / (pi * nu * d), 0)
        qm = round(((((d / sin(alpha)) + Lk) ** 2) * (d ** 2) * pl * pi * dTdin[i]) / ((8 + 3.6 \
            * (gidro_kef(Re) ** 0.5)) * d * ctg(alpha) * T1din[i] * T2din[i]), 4)
        errdin = abs((qm - qm1) / qm)
    Kgdin.append(round(1 + 0.45 * (gidro_kef(Re) ** 0.5), 2))
    spisok_qm.append(round_sig(qm, 3))
    errdin = 1
    Re2 = 1e4
# Вычисляем погрешности
dKgdin = [otn_err(s) * 100 for s in Kgdin]
ddTdin = []
for i in range(6):
    ddTdin.append(otn_err(dTdin[i], 3) * 100)
for i in range(6, len(dTdin)):
    ddTdin.append(otn_err(dTdin[i], 4) * 100)
# Строим график
fig3 = plt.figure('График погрешностей УЗР', figsize = (10, 5))
plt.xlim(spisok_qm[0], spisok_qm[47])
plt.ylim(0, 1.2)
plt.grid(True, alpha = 0.3)
plt.xlabel('Расход, кг/с', {'fontname':'Times New Roman'}, fontweight='normal', fontsize=14)
plt.ylabel('Относительная погрешность, %', {'fontname':'Times New Roman'}, fontweight='normal', fontsize=14)
plt.plot(spisok_qm, dKgdin, linewidth = '5', label='Погрешность гидродинамического коэффициента')
plt.plot(spisok_qm, ddTdin, linewidth = '5', label='Погрешность разности распространения УЗС')
plt.legend(loc='best')
plt.show()
plt.show()


