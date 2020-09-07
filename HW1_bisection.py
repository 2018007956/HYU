# Bisection Method
def f(x):
    return 5*pow(x,4)-22.4*pow(x,3)+15.85272*pow(x,2)+24.161472*x-23.4824832

xl = int(input('lower bound : '))
xu = int(input('upper bound : '))

def bisection(xl, xu):
    if f(xl)*f(xu) > 0:
        print('No root found')
    else:
        while (xu-xl)/2 > 0.0000001: #tolerance: 허용오차
            m = (xu+xl)/2
            if f(m) == 0:
                return m
            elif f(xl)*f(m)>0:
                xl = m
            else:
                xu = m
        return m

root = bisection(xl, xu)
print('root: ', root)

