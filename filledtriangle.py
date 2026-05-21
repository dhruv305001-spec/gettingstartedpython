def main():
    h = int(input('Enter height of triangle: '))
    c = '*'
    filledupsidedowntriangle(h, c)
    filledtriangle(h, c)
    print()


def filledtriangle(h, c, s=' '):
    for i in range(h):
        for j in range(h-i-1):
            print(s, end='')
        for k in range(2*i+1):
            print(c, end='')
        print()


def filledupsidedowntriangle(h, c, s=' '):
    for i in range(h):
        for j in range(i):
            print(s, end='')
        for k in range(2*(h-i)-1):
            print(c, end='')
        print()
        
main()