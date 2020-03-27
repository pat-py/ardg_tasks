class FizzBuzz:

    @staticmethod
    def get_numbers():
        print(
            "Enter two integers between 1 and 10000 that match the condition: the second number is greater than the first.")

        while True:
            try:
                n, m = int(input("First integer: ")), int(input("Second integer: "))
            except ValueError:
                print("Sorry, it's not an integer. Try again: ")
                continue
            if not 1 <= n < m <= 10000:
                print("Numbers don't match the condition")
                continue
            else:
                break
        numbers = [n, m]
        return numbers

    @staticmethod
    def print_numbers(numbers):

        for num in range(numbers[0], numbers[1] + 1):
            if num % 3 == 0 and num % 5 == 0:
                print("FizzBuzz")
            elif num % 3 == 0:
                print("Fizz")
            elif num % 5 == 0:
                print("Buzz")
            else:
                print(num)


if __name__ == "__main__":
    numbers = FizzBuzz.get_numbers()
    FizzBuzz.print_numbers(numbers)
