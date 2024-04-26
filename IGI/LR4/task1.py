# Task 1
from datetime import datetime as dt
import pickle
import csv


class HistoryIvents:
    def __init__(self):
        self.__data = [{dt(1863, 1, 22): "Kalinovsky's uprising."},
                       {dt(1067, 3, 3): "Battle of the Nemiga River."},
                       {dt(1918, 3, 25): "Proclamation of the Belarusian People's Republic."},
                       {dt(1410, 7, 15): "Battle of Grunwald."},
                       ]

    @property
    def events(self):
        """Property which returns list of events."""
        return self.__data

    @events.setter
    def events(self, data):
        self.__data = data


class TaskOne:
    def __init__(self, fname="files/task1.csv"):
        self.HIvents = HistoryIvents()
        self.filename = fname
        self.task_condition = 1
        self.desc = "Task 1: belarusian history events."

    @staticmethod
    def check_date_validity(answer):
        """Static method to check date validity and return datetime obj or None."""
        try:
            date_obj = dt.strptime(answer, "%Y-%m-%d")
        except ValueError:
            return None

        return date_obj

    @staticmethod
    def check_century_validity(cent):
        """Static method to check int validity and return int or None."""
        try:
            cent = int(cent)
            if 0 <= cent <= 21:
                return cent
            return None
        except ValueError:
            return None

    def input_ivents(self):
        """Method for reinitializing list of events."""
        choice = input("Enter:\n1 - for using custom ivents dict\nother - for using default ivents dict\n")
        if choice != "1":
            return

        events = []
        while True:
            date = input("Enter date of the event (YYYY-MM-DD) or 'q' to quite: ")
            if date == "q":
                break

            valid_date = TaskOne.check_date_validity(date)
            if valid_date is None:
                print("Invalid date entered.")
                continue

            event_desc = input("Enter event description: ")
            events.append({valid_date: event_desc})

        self.HIvents.events = events
        self.serialize_events()

    def input_task_condition(self):
        """Method for setting task condition."""
        choice = input("Enter the task condition:\n1 - using CSV file\n2 - using pickle module\n")
        if choice == "1":
            self.task_condition = 1
            self.filename = "files/task1.csv"
        elif choice == "2":
            self.task_condition = 2
            self.filename = "files/task1.pkl"
        else:
            print("Invalid task condition. 1-st condition is used by default.")

    def serialize_events(self):
        """Serialize list of events according to task condition."""
        if self.task_condition == 1:
            try:
                data_to_write = [(list(d.keys())[0].strftime('%Y-%m-%d'), list(d.values())[0]) for d in
                                 self.HIvents.events]
                with open(self.filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(data_to_write)
            except Exception as e:
                print(e)
            finally:
                print("{CSV}:Events serialized successfully.")
        else:
            try:
                with open(self.filename, "wb") as file:
                    pickle.dump(self.HIvents.events, file)
            except Exception as e:
                print(e)
            finally:
                print("{Pickle}:Ivents serialized successfully.")

    def show_events(self):
        """Method for showing list of events."""
        print("Date \t Event")
        for event in self.HIvents.events:
            print(f"{list(event.keys())[0].strftime("%Y-%m-%d")}:\t{event[list(event.keys())[0]]}")

    def show_events_by_century(self, century):
        """Shows list of event according to century{int} """
        for event in self.HIvents.events:
            if (list(event.keys())[0].year // 100) + 1 == century:
                print(f"{list(event.keys())[0].strftime("%Y-%m-%d")}:\t{event[list(event.keys())[0]]}")

    @staticmethod
    def show_available_commands():
        """Shows list of available commands."""
        print("Available commands:\n/ie - input events\n/c - change task condition\n/s - show events\n/sc - show "
              "events by century\n/cl - show commands list\n/q - to quite task")

    def run(self):
        print(self.desc)
        TaskOne.show_available_commands()
        while True:
            command = input("Command: ")
            if command == "/ie":
                self.input_ivents()
            elif command == "/c":
                self.input_task_condition()
            elif command == "/s":
                self.show_events()
            elif command == "/sc":
                cent = TaskOne.check_century_validity(input("Enter century: "))
                if cent is None:
                    print("Invalid century.")
                    continue
                self.show_events_by_century(cent)
            elif command == "/cl":
                self.show_available_commands()
            elif command == "/q":
                break
