def main():
    n = int(input("Enter number of Fibonacci numbers : "))
    fibonacci(n)


def fibonacci(n):
    num1 = 0
    num2 = 1
    for i in range(n):
        print(num1)
        num2 = num1 + num2
        num1 = num2 - num1

main()