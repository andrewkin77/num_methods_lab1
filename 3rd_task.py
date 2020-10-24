import matplotlib.pyplot as plt
import math
import numpy as np


def f_1(x, u_1, u_2, a, b):
    return u_2


def f_2(x, u_1, u_2, a, b):
    return -(a * (u_2 ** 2) + b * u_1)


def RK4(x_0, u1_0, u2_0, f_1, f_2, a, b, h):
    u1 = np.longdouble(u1_0)
    u2 = np.longdouble(u2_0)
    k_1 = np.longdouble(h * f_1(x_0, u1_0, u2_0, a, b))
    l_1 = np.longdouble(h * f_2(x_0, u1_0, u2_0, a, b))
    k_2 = np.longdouble(h * f_1(x_0 + h / 2, u1_0 + k_1 / 2, u2_0 + l_1 / 2, a, b))
    l_2 = np.longdouble(h * f_2(x_0 + h / 2, u1_0 + k_1 / 2, u2_0 + l_1 / 2, a, b))
    k_3 = np.longdouble(h * f_1(x_0 + h / 2, u1_0 + k_2 / 2, u2_0 + l_2 / 2, a, b))
    l_3 = np.longdouble(h * f_2(x_0 + h / 2, u1_0 + k_2 / 2, u2_0 + l_2 / 2, a, b))
    k_4 = np.longdouble(h * f_1(x_0 + h, u1_0 + k_3, u2_0 + l_3, a, b))
    l_4 = np.longdouble(h * f_2(x_0 + h, u1_0 + k_3, u2_0 + l_3, a, b))
    u1 += np.longdouble(1 / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4))
    u2 += np.longdouble(1 / 6 * (l_1 + 2 * l_2 + 2 * l_3 + l_4))
    return u1, u2


def num_sol_3_task(a, b, N_max, f_1, f_2, x_0, u1_0, u2_0, x_end, h, e, error_control):
    c1 = 0
    c2 = 0
    u1_ds = 0
    u2_ds = 0
    S_nor = 0
    C1 = [c1]
    C2 = [c2]
    U1 = [u1_0]
    U1_ds = [u1_0]
    U1_U1ds = [0]
    U2 = [u2_0]
    U2_ds = [u2_0]
    U2_U2ds = [0]
    H = [h]
    Error_arr = [0]
    X = [x_0]
    counter = 0

    while x_0 <= x_end and counter < N_max:
        u1_0, u2_0 = RK4(x_0, u1_0, u2_0, f_1, f_2, a, b, h)
        if (error_control):
            u1_ds, u2_ds = RK4(x_0, u1_0, u2_0, f_1, f_2, a, b, h / 2)
            u1_ds, u2_ds = RK4(x_0, u1_ds, u2_ds, f_1, f_2, a, b, h / 2)
            S_nor = abs(((u1_ds - u1_0) ** 2 + (u2_ds - u2_0) ** 2) ** (1 / 2))
            while S_nor > e:
                h = h / 2
                u1_0, u2_0 = RK4(x_0, u1_0, u2_0, f_1, f_2, a, b, h)
                u1_ds, u2_ds = RK4(x_0, u1_0, u2_0, f_1, f_2, a, b, h / 2)
                u1_ds, u2_ds = RK4(x_0, u1_ds, u2_ds, f_1, f_2, a, b, h / 2)
                S_nor = abs(((u1_ds - u1_0) ** 2 + (u2_ds - u2_0) ** 2) ** (1 / 2))
                c1 += 1

        x_0 = x_0 + h
        counter = counter + 1
        H.append(h)
        U1_ds.append(u1_ds)
        U2_ds.append(u2_ds)
        U1.append(u1_0)
        U2.append(u2_0)
        U1_U1ds.append(u1_0 - u1_ds)
        U1_U1ds.append(u2_0 - u2_ds)
        X.append(x_0)
        Error_arr.append(S_nor / 15)
        if error_control and S_nor < e / 32:
            h = 2 * h
            c2 += 1
        C2.append(c2)
        C1.append(c1)

    data = [X, U1, U1_ds, U2, U2_ds, Error_arr, H, C1, C2]
    plt.plot(U1, U2)
    #    plt.plot(U1, X)
    #    plt.plot(U2, X)
    return data


a = num_sol_3_task(1, 1, 5000, f_1, f_2, 1, 0.001, 0.0002, 5, 0.001, 0.0001, 1)