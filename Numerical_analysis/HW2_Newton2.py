# Newton Method
# using approximation to find minimum
import matplotlib.pyplot as plt
import numpy as np

h=0.1

def f(x):
    return 5*pow(x,4)-22.4*pow(x,3)+15.85272*pow(x,2)+24.161472*x-23.4824832

def derivFunc(x):
    return (f(x+h)-f(x))/h

def secondDerivFunc(x):
    return (derivFunc(x)-derivFunc(x-h)) / h

def newton(x):
    dx = derivFunc(x) / secondDerivFunc(x)
    while abs(dx) > 0.0000001:
        dx = derivFunc(x) / secondDerivFunc(x)
        # x(i+1) = x(i) - f'(x) / f''(x) +dx
        x = x - dx + dx/2
    print("x of the minimum : ", x)


g = int(input('Initial guess : '))  # Initial guess
newton(g)

# x = np.arange(-1, 0, 0.01)
# plt.plot(x, 5*pow(x,4)-22.4*pow(x,3)+15.85272*pow(x,2)+24.161472*x-23.4824832)
# plt.show()
