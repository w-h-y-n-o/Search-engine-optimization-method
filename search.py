from decimal import Decimal
import time

start_time = time.time()

file = 'xyz.txt'

r0 = 0.1
x0 = 112917.160
y0 = 91608.705

p = 0
qx = 0
qy = 0
qr = 0
f = 0

# функция для вычисления значения целевой функции
def pvv(x0, y0, r0):
    s_vv = 0
    vv = 0
    x0 = Decimal(str(x0))
    y0 = Decimal(str(y0))
    r0 = Decimal(str(r0))
    with open(file, 'r', encoding='utf-8') as points:
        for xy in points:
            xy = xy.strip('\n').split()
            xy = [Decimal(i) for i in xy]
            try:
                vv = (((x0 - xy[0]) ** 2 + (y0 - xy[1]) ** 2) ** (Decimal('1') / Decimal('2')) - r0) ** 2
            except OverflowError:
                print(xy)
            s_vv += vv

    global p
    p += 1

    print(s_vv)
    print(p)
    return s_vv


def direction_and_step(x0, y0, r0, step_x=0.1, step_y=0.01, step_r=0.1, a=0.5):
    # Поиск направления минимума по оси X
    while True:
        global qx
        qx += 1

        # Пробный шаг
        xn0 = x0 + step_x
        if pvv(xn0, y0, r0) < pvv(x0, y0, r0):
            x0 = xn0
            dirx = 1
            break

        xn0 = x0 - step_x
        if pvv(xn0, y0, r0) < pvv(x0, y0, r0):
            x0 = xn0
            dirx = 0
            break

        # шаг слишком большой, поэтому нужно его уменьшить и повторить цикл
        step_x = step_x * a

    # Поиск направления минимума по оси Y
    while True:
        global qy
        qy += 1

        # Пробный шаг
        yn0 = y0 + step_y
        if pvv(x0, yn0, r0) < pvv(x0, y0, r0):
            y0 = yn0
            diry = 1
            break

        yn0 = y0 - step_y
        if pvv(x0, yn0, r0) < pvv(x0, y0, r0):
            y0 = yn0
            diry = 0
            break

        # шаг слишком большой, поэтому нужно его уменьшить и повторить цикл
        step_y = step_y * a

    while True:
        global qr
        qr += 1

        # Пробный шаг
        rn0 = r0 + step_r
        if pvv(x0, y0, rn0) < pvv(x0, y0, r0):
            r0 = rn0
            dirr = 1
            break

        rn0 = r0 - step_r
        if pvv(x0, y0, rn0) < pvv(x0, y0, r0):
            r0 = rn0
            dirr = 0
            break

        # шаг слишком большой, поэтому нужно его уменьшить и повторить цикл
        step_r = step_r * a

    return dirx, diry, dirr, step_x, step_y, step_r


# Функци, реализующая перемещение по осям
def search(x0, y0, r0):
    # начальные значения
    xn0 = x0
    yn0 = y0
    rn0 = r0

    while True:
        global f
        f += 1

        # условие выхода из цикла
        if (abs(pvv(xn0, yn0, rn0) - pvv(x0, y0, r0)) <= 0.0000001) and (abs(pvv(xn0, yn0, rn0) - pvv(x0, y0, r0)) != 0):
            break

        for_search = direction_and_step(x0, y0, r0, step_x=0.1, step_y=0.01, step_r=0.1, a=0.5)
        dirx = for_search[0]
        diry = for_search[1]
        dirr = for_search[2]
        step_x = for_search[3]
        step_y = for_search[4]
        step_r = for_search[5]

        # перемещение по оси X
        if dirx == 0:
            xn0 = x0 - step_x
            if pvv(xn0, y0, r0) < pvv(x0, y0, r0):
                x0 = xn0
                xn0 -= step_x
            else:
                continue
        elif dirx == 1:
            xn0 = x0 + step_x
            if pvv(xn0, y0, r0) < pvv(x0, y0, r0):
                x0 = xn0
                xn0 += step_x
            else:
                continue

        # перемещение по оси Y
        if diry == 0:
            yn0 = y0 - step_y
            if pvv(x0, yn0, r0) < pvv(x0, y0, r0):
                y0 = yn0
                yn0 -= step_y
            else:
                continue
        elif diry == 1:
            yn0 = y0 + step_y
            if pvv(x0, yn0, r0) < pvv(x0, y0, r0):
                y0 = yn0
                yn0 += step_y
            else:
                continue

        # перемещение по оси R
        if dirr == 0:
            rn0 = r0 - step_r
            if pvv(x0, y0, rn0) < pvv(x0, y0, r0):
                r0 = rn0
                rn0 -= step_r
            else:
                continue
        elif dirr == 1:
            rn0 = r0 + step_r
            if pvv(x0, y0, rn0) < pvv(x0, y0, r0):
                r0 = rn0
                rn0 += step_r
            else:
                continue

    # Округление значений до нужной точности
    x0 = round(x0, 3)
    y0 = round(y0, 3)
    r0 = round(r0, 3)
    m = round((pvv(x0, y0, r0) / Decimal('131')) ** (Decimal('1') / Decimal('2')), 3)  # СКО
    return x0, y0, r0, m, p, qx, qy, qr, f


end = search(x0, y0, r0)
print('X0 =', end[0], 'м')
print('Y0 =', end[1], 'м')
print('R =', end[2], 'м')
print('СКО =', end[3], 'м')
print('Кол-во итераций поиска направления по оси X =', end[5])
print('Кол-во итераций поиска направления по оси Y =', end[6])
print('Кол-во итераций поиска направления по оси R =', end[7])
print('Кол-во итераций поискового метода =', end[8])
print('Время выполнения программы:', round(time.time() - start_time, 0), 'с')
