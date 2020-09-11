# Newton-Raphson Method
def f(x):
    return 5*pow(x,4)-22.4*pow(x,3)+15.85272*pow(x,2)+24.161472*x-23.4824832

def derivFunc(x):
    return 20*pow(x,3)-67.2*pow(x,2)+31.70544*x+24.161472

def newtonRaphson(x):
    dx = f(x) / derivFunc(x)
    while abs(dx) > 0.0000001:
        dx = f(x) / derivFunc(x)

        # x(i+1) = x(i) - f(x) / f'(x)
        x = x - dx
    print("root : ", x)

g = int(input('Initial guess : '))  
newtonRaphson(g)

# 허용오차를 0.00000001 이렇게만 해줘도
# -1.04400000000000~ 파이썬이 출력하는 자릿수까지 0이 채워져서
# -1.044 까지만 출력된다
# 그러므로 허용오차는 0.0000001까지만 하기