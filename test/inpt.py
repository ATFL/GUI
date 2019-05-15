A = 0

def do_function(num):
    if num == '0':
        print("off")
    elif num == '1':
        print("on")
    else:
        print("invalid")

while True:
    A = input("Press Num 1 or 0: ")
    do_function(A)
