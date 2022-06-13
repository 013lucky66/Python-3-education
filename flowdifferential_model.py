from math import e, pi, log10, floor
from random import randint
import matplotlib.pyplot as plt
import numpy as np


# Задаем функции и исходные данные 
# Функция округления по количесвту значащих цифр
def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)

# Функция добавления меток значений
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center', \
            bbox = dict(color = 'gray', alpha = 0.75))

# Функция генерации списка псевдослучайных чисел с контролируемым разбросом
def randomizer (minx, maxx, percent=25, n=48):
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

# Функция по определению коэффициента истечения
def kef_ist (beta, Re, L1, L2, exp):
    kef = 0.5961 + 0.0261*(beta**2) - 0.216*(beta**8) + 0.000521*((1e6*beta/Re)**0.7) \
         + (beta**3.5)*(0.0188 + 0.0063*((1.9e4*beta/Re)**0.8))*((1e6/Re)**0.3) \
              + (0.043 + 0.8*(exp**(-10*L1)) - 0.123*(exp**(-7*L1))) \
                  *(1 - 0.11*((1.9e4*beta/Re)**0.8))*(beta/(1 - beta**4)) \
                      - 0.031*(beta**1.3)*(2*L2/(1-beta) - 0.8*((2*L2/(1-beta))**1.1))
    return round(kef, 4)

d = 0.125         # диаметр отверстия диафрагмы, м
D = 0.500         # диаметр измерительного трубопровода, м
pl = 845.0        # плотность нефти, кг/(м**3)
dp = 100000       # перепад давлений, Па
nu = 0.05         # динамическая вязкость, Па*с
err = 1           # ошибка итераций
errnorm = 0.0001  # допустимая относительная разность между итерациями
imax = 1000       # допустимое количество итераций
i = 0             # номер итерации
beta = d / D      # бета-отношение
Re = Re1 = 1e6    # начальное число Рейнольдса
exp = e           # основание натурального логарифма


# Предлагаем выбрать метод отбора
print('Пожалуйста, напишите цифру, соответствующую методу отбора давления:')
print('1 - угловой')
print('2 - фланцевый')
print('3 - радиальный')
A = int(input())
if A == 1:
    L1 = L2 = 0
elif A == 2:
    L1 = L2 = 0.47
elif A == 3:
    L1 = L2 = 1 / D
else:
    print('Введено некорректное значение. Пожалуйста, начните заново.')


# Определяем значение числа Рейнольдса на основании исходных данных с помошью метода итераций
while err > errnorm:
    Re = Re1
    C1 = kef_ist (beta, Re, L1, L2, exp)
    Re = round(((D*nu)**(-1)) * (d**2) * C1 * ((1 - beta**4)**(-0.5)) * ((2*pl*dp)**0.5), 4)
    C2 = kef_ist (beta, Re, L1, L2, exp)
    Re1 = round(Re * C2 / C1, 4)
    err = abs((Re1 - Re) / Re1)
    i += 1


# Находим значение массового расхода
C = round(kef_ist (beta, Re1, L1, L2, exp), 4)
qm  = round_sig(C * ((1 - beta**4)**(-0.5)) * pi * ((d**2) / 4) * ((2*pl*dp)**0.5), 3)
if qm - int(qm) == 0:
    qm = int(qm)
print('Массовый расход для начальных условий составляет: ' + str(qm) + ' кг/с')


# Определяем относительную погрешность определения массового расхода как результата косвенного измерения
dqm = round((((absol_err(C, 4) / C)**2) + 16*((absol_err(d) / d)**2) + 4*((absol_err(D) / D)**2)\
     + 0.25*((absol_err(pl, 4) / pl)**2) + 0.25*((absol_err(dp) / dp)**2))**0.5, 4)
print('Относительная погрешность расчета массового расхода: ' + str(round_sig(dqm * 100, 4)) + ' %')

# Строим диаграмму относительных погрешностей составляющих результирующей опгрешности
spisok_err = [(round(absol_err(C) / C, 5))*1e2, (round(absol_err(d) / d, 5))*1e2, \
    (round(absol_err(D) / D, 5))*1e2, (round(absol_err(pl) / pl, 5))*1e2, \
        (round(absol_err(dp) / dp, 5))*1e2]
nazv = ['C', 'd', 'D', 'pl', 'dp']
fig1 = plt.figure('Диаграмма погрешностей', figsize = (10, 5))
plt.grid(True, alpha = 0.3)
plt.bar(nazv, spisok_err)
addlabels(nazv, spisok_err)
plt.ylabel('Относительная погрешность, %', {'fontname':'Times New Roman'}, fontweight='normal', \
    fontsize=14)


# Строим расходограмму
# Определяем значения расхода
dpdin = randomizer(75000, 13000000)
spisok_qm = []
errdin = 1
Re2 = Re3 =1e6
for element in dpdin:
    while errdin > errnorm:
        C1din = kef_ist (beta, Re2, L1, L2, exp)
        Re2 = round(((D*nu)**(-1)) * (d**2) * C1din * ((1 - beta**4)**(-0.5)) * ((2*pl*element)**0.5), 4)
        C2din = kef_ist (beta, Re2, L1, L2, exp)
        Re3 = round(Re2 * C2din / C1din, 4)
        errdin = abs((Re3 - Re2) / Re3)
    Cdin = round(kef_ist (beta, Re3, L1, L2, exp), 4)
    spisok_qm.append(round_sig((Cdin * ((1 - beta**4)**(-0.5)) * pi * ((d**2) / 4) * ((2*pl*element)**0.5) * 3.6), 3))
    errdin = 1
    Re2 = Re3 =1e6
# Вычисляем накопленный расход
m = 0
for i in range(1, len(spisok_qm)):
    m += round(0.5 * 0.5 * (spisok_qm[i] + spisok_qm[i - 1]), 3)
# Строим график
t = np.linspace(0, 24, 48)
fig2 = plt.figure('Суточная расходограмма', figsize = (10, 5))
plt.ylim(0, 8000)
plt.xlim(0, 24)
plt.grid(True, alpha = 0.3)
plt.xlabel('Время, ч', {'fontname':'Times New Roman'}, fontweight='normal', fontsize=14)
plt.ylabel('Массовый расход, т/ч', {'fontname':'Times New Roman'}, fontweight='normal', fontsize=14)
plt.plot(t, spisok_qm)
plt.fill_between(t, spisok_qm, color = 'gray', alpha = 0.2)
plt.text(10, 500, str(m) + ' т', fontsize=16, bbox=dict( color='gray', alpha = 0.5))

# Строим график изменеия погрешностей в зависимости от расхода
# Определяем значения величин
dpdin = np.linspace(75e3, 13e6, 48)
spisok_qm = []
Cdin = []
errdin = 1
Re2 = Re3 =1e6
for i in range(len(dpdin)):
    while errdin > errnorm:
        C1din = kef_ist (beta, Re2, L1, L2, exp)
        Re2 = round(((D*nu)**(-1)) * (d**2) * C1din * ((1 - beta**4)**(-0.5)) * ((2*pl*dpdin[i])**0.5), 4)
        C2din = kef_ist (beta, Re2, L1, L2, exp)
        Re3 = round(Re2 * C2din / C1din, 4)
        errdin = abs((Re3 - Re2) / Re3)
    Cdin.append(round(kef_ist (beta, Re3, L1, L2, exp), 3))
    spisok_qm.append(round_sig(Cdin[i] * ((1 - beta**4)**(-0.5)) * pi * ((d**2) / 4) * ((2*pl*dpdin[i])**0.5), 3))
    errdin = 1
    Re2 = Re3 =1e6
# Вычисляем погрешности
dCdin = [(absol_err(s) / s) * 100 for s in Cdin]
ddpdin = [(absol_err(s) / s) * 100 for s in dpdin]
# Строим график
fig3 = plt.figure('График погрешностей', figsize = (10, 5))
plt.xlim(spisok_qm[0], spisok_qm[47])
plt.ylim(0, 0.2)
plt.grid(True, alpha = 0.3)
plt.xlabel('Расход, кг/с', {'fontname':'Times New Roman'}, fontweight='normal', fontsize=14)
plt.ylabel('Относительная погрешность, %', {'fontname':'Times New Roman'}, fontweight='normal', fontsize=14)
plt.plot(spisok_qm, dCdin, linewidth = '5', label='Погрешность коэффициента истечения')
plt.plot(spisok_qm, ddpdin, linewidth = '5', label='Погрешность перепада давлений')
plt.legend(loc='best')
plt.show()



