from H2_components import *
valve1 = Valve('vavle1',18)

while True:
    A = input("1 for HIGH, 0 for LOW")
    print(A)
    if A == '1':
        print("LOW")
        valve1.enable()
    else:
        print("HIGH")
        valve1.disable()