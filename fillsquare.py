def PrintSquare(n, c):
    for i in range(n):
        for j in range(n):
            print(c, end=' ')
        print()

def PrintSquareFaster(n, c):
    for i in range(n**2):
        print(c,end=' ')
        if (i+1) % n == 0:
            print()
def main():
    s = input('Enter the side of the square: ')
    c = '*'
    PrintSquareFaster(int(s), c)

main()