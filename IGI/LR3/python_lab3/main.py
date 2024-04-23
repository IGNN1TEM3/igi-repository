# Laboratory work №3
# Title: Standard data types, collections, functions, modules.
# Completed by: German Baranovsky 253502
# v1.0 4/23/2024

import task1 as t1
import task2 as t2
import task3 as t3
import task4 as t4
import task5 as t5
import helper as hp


command_dict = {
    "/c": hp.print_command_list,
    "/t1": t1.task1_solve,
    "/t2": t2.task2_solve,
    "/t3": t3.task3_solve,
    "/t4": t4.task4_solve,
    "/t5": t5.task5_solve,
}

print("LABORATORY WORK №3 V1.0")


hp.print_command_list()

while True:
    buffer = input("Command: ")
    if buffer == "/q":
        break
    elif buffer in command_dict:
        command_dict[buffer]()
    else:
        print("Undefined command!")
