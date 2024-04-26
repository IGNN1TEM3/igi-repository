# Laboratory work №4
# Title: Working with files, classes, serializers, regular expressions and standard libraries.
# Completed by: German Baranovsky 253502
# v1.0 4/27/2024

import task1 as t1
import task2 as t2
import task3 as t3
import task4 as t4
import task5 as t5


def chose_task():
    """Returns user's command choice.'"""
    print("Command list:\nt1 - task 1\t t2 - task 2\nt3 - task 3\tt4 - task 4\nt5 - task 5\tq - quiet")
    return input("Command: ")


if __name__ == '__main__':
    t = None
    print("Laboratory work 4")
    while True:
        choice = chose_task()
        if choice == "t1":
            t = t1.TaskOne()
            t.run()
        elif choice == "t2":
            t = t2.TaskTwo()
            t.run()
        elif choice == "t3":
            t = t3.TaskThree()
            t.run()
        elif choice == "t4":
            t = t4.TaskFour()
            t.run()
        elif choice == "t5":
            t = t5.TaskFive()
            t.run()
        elif choice == "q":
            break
