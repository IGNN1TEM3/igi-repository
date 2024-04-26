import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import statistics as stats
import random


class TaskThree:
    def __init__(self):
        self.iterations = 0
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.variance = 0
        self.stddev = 0

    @staticmethod
    def calculate_ln(x, eps=1e-6, max_iter=500):
        """Calculates function ln(1-x) and returns result {float}"""
        result = -x
        term = -x
        iteration = 1
        while abs(term) > eps and iteration <= max_iter:
            term = term * x * iteration / (iteration + 1)
            result += term
            iteration += 1
        return result

    def calculate_with_attrs(self, x, eps=1e-5, max_iter=500):
        """Calculates function ln(1-x) and additional attributes """
        args = []
        result = -x
        term = -x
        args.append(x)
        iteration = 1
        while abs(term) > eps and iteration <= max_iter:
            term = term * x * iteration / (iteration + 1)
            args.append(term)
            result += term
            iteration += 1
        self.iterations = iteration
        self.mean = stats.mean(args)
        self.median = stats.median(args)
        self.mode = stats.mode(args)
        self.variance = stats.variance(args)
        self.stddev = stats.stdev(args)
        return result

    def show_results(self):
        """Shows results of calcultation ln(1-x)"""
        x = random.random()
        f = self.calculate_with_attrs(x)
        print(f"For x = {x} we have following results:")
        print(f"Ln(1-x) = {f}")
        print(f"Mean = {self.mean}")
        print(f"Median = {self.median}")
        print(f"Mode = {self.mode}")
        print(f"Variance = {self.variance}")
        print(f"Standard Deviation = {self.stddev}")

    @staticmethod
    def plot():
        """Plots ln(1-x)"""
        x = np.arange(-1, 0.9, 0.1)
        vect_ln = np.vectorize(TaskThree.calculate_ln)
        y1 = vect_ln(x)
        y2 = np.log(1 - x)
        fig, ax = plt.subplots()
        ax.grid(True)
        ax.plot(x, y1, 'r', linewidth=2, label='My_ln(1-x)')
        ax.plot(x, y2, 'b', linewidth=1, label='Np_ln(1-x)')
        plt.annotate("Asymptote: x=1", xy=(0, 0), xytext=(0.7, 0))
        plt.legend()
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title("LN(1-x) comparison")

    @staticmethod
    def print_plot():
        """Prints plot of the ln(1-x)"""
        TaskThree.plot()
        plt.show()

    @staticmethod
    def save_plot():
        """Saves plot of the ln(1-x) into a file=img/ln.png"""
        TaskThree.plot()
        plt.savefig("img/ln.png")

    def run(self):
        print("Task 3 commands:\n/t - table result with random x\n/p - print plot\n/s - save plot\n/q - quit")
        while True:
            command = input("Command: ")
            if command == "/t":
                self.show_results()
            elif command == "/p":
                self.print_plot()
            elif command == "/s":
                self.save_plot()
            elif command == "/q":
                break
