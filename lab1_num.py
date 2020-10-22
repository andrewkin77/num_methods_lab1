import math
import matplotlib.pyplot as plt
import numpy as np


def func_test(x, y):
    return ((-3 / 2) * y)


def func_1(x, y):
    a = ((1 + x ** 2) ** (-1 / 3))
    return a * (y ** 2) + y - (y ** 3) * math.sin(10 * x)


def f_1(x, u_1, u_2, a, b):
    return u_2


def f_2(x, u_1, u_2, a, b):
    return -(a * u_2 + b * u_1)


def RK_4(a, b, N_max, x_0, u1_0, u2_0, x_end, h):
    U1 = [u1_0]
    U2 = [u2_0]
    X = [x_0]
    counter = 0

    while x_0 <= x_end:
        k_1 = h * f_1(x_0, u1_0, u2_0, a, b)
        l_1 = h * f_2(x_0, u1_0, u2_0, a, b)
        k_2 = h * f_1(x_0 + h / 2, u1_0 + k_1 / 2, u2_0 + l_1 / 2, a, b)
        l_2 = h * f_2(x_0 + h / 2, u1_0 + k_1 / 2, u2_0 + l_1 / 2, a, b)
        k_3 = h * f_1(x_0 + h / 2, u1_0 + k_2 / 2, u2_0 + l_2 / 2, a, b)
        l_3 = h * f_2(x_0 + h / 2, u1_0 + k_2 / 2, u2_0 + l_2 / 2, a, b)
        k_4 = h * f_1(x_0 + h, u1_0 + k_3, u2_0 + l_3, a, b)
        l_4 = h * f_2(x_0 + h, u1_0 + k_3, u2_0 + l_3, a, b)

        x_0 = x_0 + h
        u1_0 = u1_0 + 1 / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
        u2_0 = u2_0 + 1 / 6 * (l_1 + 2 * l_2 + 2 * l_3 + l_4)
        U1.append(u1_0)
        U2.append(u2_0)
        X.append(x_0)

    plt.plot(U1, U2)
    data = [X, U1, U2]
    return data


def RK4(x_i, y_i, h, func, v_max):
    y = np.longdouble(y_i)
    k1 = np.longdouble(h * func(x_i, y))
    if abs(k1) > v_max:
        return v_max
    k2 = np.longdouble(h * func(x_i + h / 2, y + k1 / 2))
    if abs(k2) > v_max:
        return v_max
    k3 = np.longdouble(h * func(x_i + h / 2, y + k2 / 2))
    if abs(k3) > v_max:
        return v_max
    k4 = np.longdouble(h * func(x_i + h, y + k3))
    if abs(k4) > v_max:
        return v_max
    y += np.longdouble((1 / 6) * (k1 + 2 * k2 + 2 * k3 + k4))
    return y


def func_num_sln(x0, u0, x_max, h, Nmax, max_error, func, error_control):
    v_max = 10e30
    c1 = 0
    c2 = 0
    x = x0
    v = u0
    v2 = u0
    i = 1

    X = [x0]
    V = [u0]
    # X2 = []
    V2 = [u0]
    C1 = [c1]
    C2 = [c2]
    H = [h]
    Error_arr = [abs(v2 - v) / 15]

    while x <= x_max - h:
        temp = RK4(x, v, h, func, v_max)
        temp2 = RK4(x, v2, h / 2, func, v_max)
        # v_half = temp2
        temp2 = RK4(x + h / 2, temp2, h / 2, func, v_max)
        if temp == v_max or temp2 == v_max:
            break
        if error_control and abs(temp2 - temp) > max_error:
            h /= 2
            c1 += 1
            pass
        x += h
        v = temp
        v2 = temp2
        X.append(x)
        V.append(v)
        # X2.append(x-h/2)
        # V2.append(v_half)
        # X2.append(x)
        V2.append(v2)
        C1.append(c1)
        H.append(h)
        Error_arr.append(abs(v2 - v) / 15)
        if error_control:
            if abs(v2 - v) < (max_error / 32):
                h *= 2
                c2 += 1
        C2.append(c2)
        if error_control:
            if i == Nmax:
                break
        i += 1
        # if abs(v) > v_max:
        # break

    data = [X, V, V2, Error_arr, H, C1, C2]
    return data


def test_precise_sln(x0, u0, h, x_max):
    X = []
    U = []
    # h = 0.001
    X.append(x0)
    U.append(u0)
    x = x0
    u = u0
    c = u0 * math.exp((3 / 2) * x0)
    while x < x_max:
        x += h
        u = c * math.exp((-3 / 2) * x)
        X.append(x)
        U.append(u)
    data = [X, U]
    return data


def draw(data, error_control, is_test):
    plt.plot(data[0], data[1], label='Regular step')
    if error_control:
        plt.plot(data[0], data[2], label='Half Step')
    if is_test:
        plt.plot(data[len(data) - 2], data[len(data) - 1], label='Precise solution')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title("Plot")
    plt.legend()
    plt.show()

# def clear():
# 	plt.clf()
