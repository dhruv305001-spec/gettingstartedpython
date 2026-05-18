
def PrintVertical(n,c):
    for i in range(n):
        print(c)

def PrintHorizontal(n,c):
    for i in range(n):
        print(c, end='')
    
    

def main():
    n = input('Enter a number: ')
    c = '*'
    PrintVertical(int(n),c)
    print()
    PrintHorizontal(int(n),c)
    
main()