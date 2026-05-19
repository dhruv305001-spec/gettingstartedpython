def main():
    l = input('Enter the length of the rectangle: ')
    b = input('Enter the breadth of the rectangle: ')
    c = '*'
    filledfasterrectangle(l , b , c)
    print()
    filledfasterrectangle(b , l , c)

def filledfasterrectangle(l, b, c):
    for i in range(int(l)*int(b)):
        print(c, end=' ')
        if (i + 1) % int(l) == 0:
            print()

def filledrectangle(l, b, c):
    for i in range(int(b)):
        for j in range(int(l)):
            print(c, end=' ')
        print()

main()