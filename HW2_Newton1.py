# Newton Method
# using exact 1st and 2nd derivatives to find minimum
import matplotlib.pyplot as plt
import numpy as np
def f(x):
    return 5*pow(x,4)-22.4*pow(x,3)+15.85272*pow(x,2)+24.161472*x-23.4824832

def derivFunc(x):
    return 20*pow(x,3)-67.2*pow(x,2)+31.70544*x+24.161472

def secondDerivFunc(x):
    return 60*pow(x,2)-134.4*x+31.70544

def newton(x):
    dx = derivFunc(x) / secondDerivFunc(x)
    while abs(dx) > 0.0000001:
        dx = derivFunc(x) / secondDerivFunc(x)
        # x(i+1) = x(i) - f'(x) / f''(x) +dx
        x = x - dx + dx/2
    print("x of the minimum : ", x)

g = int(input('Initial guess : '))
newton(g)

# x = np.arange(2, 3, 0.01)
# plt.plot(x, 5*pow(x,4)-22.4*pow(x,3)+15.85272*pow(x,2)+24.161472*x-23.4824832)
# plt.show()