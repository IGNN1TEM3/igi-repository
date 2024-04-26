# Task 4
import abc
import math
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Shape(abc.ABC):
    @abc.abstractmethod
    def area(self):
        pass


class FigureColor:
    def __init__(self, color):
        self.__color = color

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color


class Triangle(Shape):
    _name = "Triangle"

    def __new__(cls, a, b, gamma, color):
        print(f"{cls._name} is created.")
        return super().__new__(cls)

    def __init__(self, a, b, gamma, color):
        self.a = a
        self.b = b
        self.gamma = gamma
        self.color = FigureColor(color)

    def area(self):
        """Return the area of the triangle."""
        rads = math.radians(self.gamma)
        return self.a * self.b * math.sin(rads) / 2

    @classmethod
    def name(cls):
        """Return the name of the class."""
        return cls._name

    def info(self):
        """Print a description of the current triangle."""
        print("{color} {name}, square: {area}.".format(color=self.color.color, name=Triangle.name(), area=self.area()))


class TaskFour:
    def __init__(self):
        self.triangle = None
        self.img_filename = "img/triangle.png"

    def input_values(self):
        """Input two sides of the triangle and angel between, and triangle color.
        Initialize fields of the class or prints out a message."""
        print("Enter a,b - sides of triangle and gamma angel(in degrees) and color.")
        a = input("a: ")
        b = input("b: ")
        gamma = input("gamma: ")
        color = input("color: ")
        valid, message = TaskFour.check_validity(a, b, gamma, color)
        if not valid:
            print(message)
        else:
            color = message
            a = float(a)
            b = float(b)
            gamma = float(gamma)
            self.triangle = Triangle(a, b, gamma, color)

    @staticmethod
    def check_validity(a, b, gamma, color):
        """Returns tuple of bool validity and error message or new color."""
        try:
            a = float(a)
            b = float(b)
            gamma = float(gamma)
            color_m = re.search(r"(\w*blue\w*|\w*red\w*|\w*green\w*|\w*purple\w*)", color)
            if color_m is None:
                return False, "Undefined color (use primitive ones)."
            if a > 0 and b > 0 and 0 < gamma < 180:
                return True, f"{color_m.group(0)}"
            return False, "Invalid a,b or gamma."

        except ValueError:
            return False, "Value Error"

    def print_triangle_info(self):
        """Print a description of the current triangle."""
        self.triangle.info()

    def plot(self):
        """Plot the triangle."""
        if self.triangle is None:
            print("Triangle not created.")
            return

        a = self.triangle.a
        b = self.triangle.b
        gamma_radians = math.radians(self.triangle.gamma)
        c = math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(gamma_radians))

        # Points:
        a_point = (0, 0)
        b_point = (c, 0)
        c_point = (
            (b ** 2 + c ** 2 - a ** 2) / (2 * c), math.sqrt(b ** 2 - ((b ** 2 + c ** 2 - a ** 2) / (2 * c)) ** 2))

        fig, ax = plt.subplots()
        tr = patches.Polygon([a_point, b_point, c_point], closed=True, color=self.triangle.color.color)
        ax.text(c / 2 - 1, -1, f"This is {Triangle.name()}", fontsize=10)
        ax.add_patch(tr)
        ax.set_xlim(min(a_point[0], c_point[0]), max(b_point[0], c_point[0]), )
        ax.set_ylim(-1, max(a, b, c) + 1)

    def show_plot(self):
        """Print out the triangle plot."""
        self.plot()
        plt.show()

    def save_plot(self):
        """Save the triangle plot into the file=self.img_filename."""
        self.plot()
        plt.savefig(f"{self.img_filename}")

    @staticmethod
    def print_command_list():
        """Print out the command list."""
        print(
            "Available commands:\n/i - show triangle info\n/p - print triangle\n/s - save triangle into the file\n/c "
            "- change values\n/q - quiet")

    def run(self):
        print("Firstly initialize a triangle:")
        while self.triangle is None:
            self.input_values()

        while True:
            TaskFour.print_command_list()
            command = input("Command: ")
            if command.startswith("/i"):
                self.print_triangle_info()
            elif command.startswith("/p"):
                self.show_plot()
            elif command.startswith("/s"):
                self.save_plot()
            elif command.startswith("/c"):
                self.input_values()
            elif command.startswith("/q"):
                break
