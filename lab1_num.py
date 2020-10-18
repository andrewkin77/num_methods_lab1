import math
import matplotlib.pyplot as plt
import numpy as np

def func_test(x, y):
    return ((-3/2)*y)

def func_1(x, y):
    a = ((1+x**2)**(-1/3))
    return a * (y**2) + y - (y**3) * math.sin(10*x)

def RK4(x_i, y_i, h, func):
    y = y_i
    k1 = h * func(x_i, y)
    k2 = h * func(x_i + h/2, y + k1/2)
    k3 = h * func(x_i + h/2, y + k2/2)
    k4 = h * func(x_i + h, y + k3)
	if (abs(k1) + abs(k2) + abs(k3) + abs(k4) > 10000):
		return 10000
    y += (1/6)*(k1 + 2*k2 + 2*k3 + k4)
    return y

def func_num_sln(x0, u0, x_max, h, Nmax, max_error, func, error_control):
	X = []
	V = []
	X2 = []
	V2 = []
	C1 = []
	C2 = []
	H = []
	Error_arr = []

	X.append(x0)
	V.append(u0)
	X2.append(x0)
	V2.append(u0)

	#v_max = 10e3
	c1 = 0
	c2 = 0
	x = x0
	v = u0
	v2 = u0
	i = 1

	while x < x_max:
		temp = RK4(x, v, h, func)
		temp2 = RK4(x, v2, h/2, func)
		v_half = temp2
		temp2 = RK4(x + h/2, temp2, h/2, func)
		if temp == 10000 or temp2 == 10000:
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
		X2.append(x-h/2)
		V2.append(v_half)
		X2.append(x)
		V2.append(v2)
		C1.append(c1)
		H.append(h)
		Error_arr.append(abs(v2 - v) / 15)
		if error_control:
			if abs(v2 - v) < (max_error/32):
				h *= 2
				c2 += 1
			if i == Nmax:
				break
		i += 1
		C2.append(c2)
		#if abs(v) > v_max:
			#break

	data = [X, V, X2, V2, Error_arr, C1, C2]
	return data

def test_precise_sln(x0, u0, h, x_max):
	X = []
	U = []
	#h = 0.001
	X.append(x0)
	U.append(u0)
	x = x0
	u = u0
	c = u0 * math.exp((3/2)*x0)
	while x < x_max:
		x+=h
		u = c * math.exp((-3/2)*x)
		X.append(x)
		U.append(u)
	data = [X, U]
	return data

def draw(data, error_control, is_test):
	plt.plot(data[0], data[1], label='Regular step')
	if error_control:
		plt.plot(data[2], data[3], label='Half Step')
	if is_test:
		plt.plot(data[len(data)-2], data[len(data)-1], label='Precise solution')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title("Plot")
	plt.legend()
	plt.show()

# def clear():
# 	plt.clf()
