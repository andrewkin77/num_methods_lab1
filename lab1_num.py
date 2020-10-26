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
    return -(a * (u_2 ** 2) + b * u_1)


def RK4_s(x_0, u1_0, u2_0, f_1, f_2, a, b, h, v_max):
    u1 = u1_0
    u2 = u2_0
    k_1 = np.longdouble(h * f_1(x_0, u1_0, u2_0, a, b))
    if abs(k_1) > v_max:
        return v_max, v_max
    l_1 = np.longdouble(h * f_2(x_0, u1_0, u2_0, a, b))
    if abs(l_1) > v_max:
        return v_max, v_max
    k_2 = np.longdouble(h * f_1(x_0 + h / 2, u1_0 + k_1 / 2, u2_0 + l_1 / 2, a, b))
    if abs(k_2) > v_max:
        return v_max, v_max
    l_2 = np.longdouble(h * f_2(x_0 + h / 2, u1_0 + k_1 / 2, u2_0 + l_1 / 2, a, b))
    if abs(l_2) > v_max:
        return v_max, v_max
    k_3 = np.longdouble(h * f_1(x_0 + h / 2, u1_0 + k_2 / 2, u2_0 + l_2 / 2, a, b))
    if abs(k_3) > v_max:
        return v_max, v_max
    l_3 = np.longdouble(h * f_2(x_0 + h / 2, u1_0 + k_2 / 2, u2_0 + l_2 / 2, a, b))
    if abs(l_3) > v_max:
        return v_max, v_max
    k_4 = np.longdouble(h * f_1(x_0 + h, u1_0 + k_3, u2_0 + l_3, a, b))
    if abs(k_4) > v_max:
        return v_max, v_max
    l_4 = np.longdouble(h * f_2(x_0 + h, u1_0 + k_3, u2_0 + l_3, a, b))
    if abs(l_4) > v_max:
        return v_max, v_max
    u1 += np.longdouble(1 / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4))
    if abs(u1) > v_max:
        return v_max, v_max
    u2 += np.longdouble(1 / 6 * (l_1 + 2 * l_2 + 2 * l_3 + l_4))
    if abs(u2) > v_max:
        return v_max, v_max
    return u1, u2


def num_sol_3_task(a, b, N_max, f_1, f_2, x_0, u1_0, u2_0, x_end, h, e, error_control):
    v_max = 10e30
    c1 = 0
    c2 = 0
    u1_ds = u1_0
    u2_ds = u2_0
    S_nor = 0
    counter = 1

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

    while x_0 <= x_end - h:
        temp_1, temp_2 = RK4_s(x_0, u1_0, u2_0, f_1, f_2, a, b, h, v_max)
        temp1_ds, temp2_ds = RK4_s(x_0, u1_0, u2_0, f_1, f_2, a, b, h / 2, v_max)
        temp1_ds, temp2_ds = RK4_s(x_0 + h / 2, temp1_ds, temp2_ds, f_1, f_2, a, b, h / 2, v_max)
        if temp_1 == v_max or temp_2 == v_max or temp1_ds == v_max or temp1_ds == v_max:
            break
        S_nor = abs(((temp_1 - temp1_ds) ** 2 + (temp_2 - temp2_ds) ** 2) ** (1 / 2))
        if error_control and S_nor > e:
            h = h / 2
            c1 += 1
        else:
            u1_0 = temp_1
            u2_0 = temp_2
            u1_ds = temp1_ds
            u2_ds = temp2_ds
            x_0 = x_0 + h
            H.append(h)
            U1_ds.append(u1_ds)
            U2_ds.append(u2_ds)
            U1.append(u1_0)
            U2.append(u2_0)
            U1_U1ds.append(u1_0 - u1_ds)
            U1_U1ds.append(u2_0 - u2_ds)
            X.append(x_0)
            Error_arr.append(S_nor / 15)
            if error_control:
                if S_nor < e / 32:
                    h = 2 * h
                    c2 += 1
            C2.append(c2)
            C1.append(c1)
        if error_control:
            if counter >= N_max:
                break
        counter = counter + 1

    data = [X, U1, U1_ds, Error_arr, H, C1, C2, U2, U2_ds]
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
        if error_control and (abs(temp2 - temp) > max_error):
            h /= 2
            c1 += 1
        else:
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
    X = [x0]
    U = [u0]
    # h = 0.001
    x = x0
    u = u0
    c = u0 * math.exp((3 / 2) * x0)
    while x < x_max - h:
        x += h
        u = c * math.exp((-3 / 2) * x)
        X.append(x)
        U.append(u)
    data = [X, U]
    return data


def draw(data, error_control, is_test, is_func2):
    fig, ax = plt.subplots()
    if is_func2:
        fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()
    ax.plot(data[0], data[1], label='Regular step')
    ax.set_xlabel('X')
    ax.set_ylabel('V')
    ax.set_title('V(x) plot')
    if is_func2:
        ax1.plot(data[0], data[len(data)-2], label='Regular step', color='tab:green')
        ax1.set_xlabel('X')
        ax1.set_ylabel("V'")
        ax1.set_title("V'(x) plot")
        ax2.plot(data[1], data[len(data)-2], label='Regular step', color='tab:red')
        ax2.set_xlabel('V')
        ax2.set_ylabel("V'")
        ax2.set_title("V'(v) plot")
    if error_control:
        ax.plot(data[0], data[2], label='Half Step')
        if is_func2:
            ax1.plot(data[0], data[len(data) - 1], label='Half Step', color='tab:purple')
            ax2.plot(data[2], data[len(data) - 1], label='Half Step', color='tab:pink')
    if is_test:
        ax.plot(data[len(data) - 2], data[len(data) - 1], label='Precise solution')
    ax.legend()
    if is_func2:
        ax1.legend()
        ax2.legend()
    plt.show()


