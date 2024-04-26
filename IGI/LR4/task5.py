# Task 5
import numpy as np
import pandas as pd


class TaskFive:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.matrix = None

    @staticmethod
    def check_validity(n, m):
        """Checks validity of input and returns bool"""
        try:
            n = int(n)
            m = int(m)
            if n <= 0 or m <= 0:
                return False
            else:
                return True
        except ValueError:
            return False

    def input_values(self):
        """Inputs values of matrix and generates new matrix"""
        print("Enter n and m matrix dimensions.")
        n = input("n: ")
        m = input("m: ")
        if TaskFive.check_validity(n, m):
            self.n = int(n)
            self.m = int(m)
        else:
            print("Invalid input.")
        self.generate_matrix()

    def generate_matrix(self):
        """Generates matrix with n rows and m columns of random ints"""
        self.matrix = np.random.randint(-1000, 1000, size=(self.n, self.m))

    def print_matrix(self):
        """Prints matrix"""
        print("Current Matrix:")
        df = pd.DataFrame(self.matrix)
        print(df.to_string(index=False, header=False))

    def solve_personal_task(self):
        """Solve personal(counts even|odd elements of matrix and calculates correlation if possible) task and prints
        results."""
        even_nums = []
        odd_nums = []

        for i in range(self.n):
            for j in range(self.m):
                if self.matrix[i][j] % 2 == 0:
                    even_nums.append(self.matrix[i][j])
                else:
                    odd_nums.append(self.matrix[i][j])

        # 1
        print(f"Even numbers count: {len(even_nums)}\nOdd numbers count: {len(odd_nums)}")
        # 2
        try:
            if 0 < len(even_nums) == len(odd_nums):
                cor = np.corrcoef(even_nums, odd_nums)[0, 1]
                print(f"Correlation coefficient x/y : {cor}")
            else:
                print("Can't calculate correlation coefficient")
        except Exception as e:
            print(e)

    @staticmethod
    def print_command_list():
        """Prints command list for task 5"""
        print(
            "Available commands:\n/i - input new values\n/r - regenerate matrix\n/s - solve task\n/p - print "
            "matrix\n/q - quiet")

    def run(self):
        while self.n == 0:
            self.input_values()

        while True:
            TaskFive.print_command_list()
            command = input("Enter command: ")
            if command == "/i":
                self.input_values()
            elif command == "/r":
                self.generate_matrix()
            elif command == "/s":
                self.solve_personal_task()
            elif command == "/p":
                self.print_matrix()
            elif command == "/q":
                break
