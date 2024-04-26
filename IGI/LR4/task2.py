import re
import zipfile
import os


class TaskTwo:
    def __init__(self, fname="files/task2_text.txt"):
        self.input_filename = fname
        self.output_filename = "files/task2_output.txt"
        self.text = ""
        self.answers = ""

    def read_file(self):
        """Reads entire text from file=input_filename to self.text"""
        try:
            with open(self.input_filename, "r") as f:
                self.text = f.read()
        except FileNotFoundError:
            print(f"File {self.input_filename} not found.")

    def solve_general_task(self):
        """Solves general task and write results into self.answers."""
        # Sentence count:
        match = re.findall(r"[.!?]\s|[.!?]$", self.text)
        if match:
            self.answers += f"All sentence count: {len(match)}\n"
        else:
            self.answers += "All sentence count: 0\n"

        # Sentence by type count:
        self.answers += f"Affirmative sentence count: {len(re.findall(r"\.\s|\.$", self.text))}\n"
        self.answers += f"Interrogative sentence count: {len(re.findall(r"\?\s|\?$", self.text))}\n"
        self.answers += f"Exclamatory sentence count: {len(re.findall(r"!\s|!$", self.text))}\n"

        # Sentence avg length:
        sentences = re.findall(r"[^.!?]+[.!?]", self.text)
        sentences_length = [len(re.findall(r"\b\w+\b", sentence)) for sentence in sentences]
        if sentences_length:
            avg_sentence_length = sum(sentences_length) / len(sentences)
        else:
            avg_sentence_length = 0
        self.answers += f"Average sentence length: {avg_sentence_length}\n"

        # Avg word length
        words = re.findall(r"\b\w+\b", self.text)
        avg_word_length = sum(len(word) for word in words) / len(words)
        self.answers += f"Average word length: {avg_word_length}\n"

        # Smiles count:
        smiles_count = len(re.findall(r"[:;]-*[)(\]\[]+", self.text))
        self.answers += f"Smiles count: {smiles_count}\n"

    def solve_personal_task(self):
        """Solves personal task and writes results into self.answers."""
        symbol = input("Input one symbol to replace spaces: ")
        while len(symbol) != 1:
            symbol = input("Input one symbol to replace spaces: ")
        new_text = re.sub(r"\s+", symbol, self.text)
        self.answers += f"Updated text:\n{new_text}\n"

        # Is GUID:
        guid = re.search(r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$", self.text)
        if guid:
            self.answers += f"String IS GUID\n"
        else:
            self.answers += "String is NOT GUID\n"

        # Capital letters count:
        capital = len(re.findall(r"[A-Z]", self.text))
        self.answers += f"Capital letters count: {capital}\n"
        # first z-word:
        z_word = re.search(r"\b\w+z\w+\b", self.text)
        if z_word:
            self.answers += f"First z-word: {z_word.group(0)}\n"
        else:
            self.answers += f"No z-words!\n"

        # Text without words starts with a
        upd_text = re.sub(r"\ba\w+", "", self.text)
        upd_text = re.sub(r"\s+", " ", upd_text)
        self.answers += f"Updated 2 text:\n{upd_text}\n"

    def write_file_and_archive(self):
        """Writes self.answers into the file named self.output_filename and archive it."""
        try:
            with open(self.output_filename, "w") as f:
                f.write(self.answers)
            archive_filename = os.path.splitext(self.input_filename)[0] + ".zip"
            with zipfile.ZipFile(archive_filename, "w") as myzip:
                myzip.write(self.input_filename)

        except FileNotFoundError:
            print(f"File {self.output_filename} not found.")

    def get_archive_file_info(self):
        """Prints information about archive file."""
        print("Archive info: ")
        archive_filename = os.path.splitext(self.input_filename)[0] + ".zip"
        try:
            with zipfile.ZipFile(archive_filename, "r") as myzip:
                for info in myzip.infolist():
                    print(f"Filename: {info.filename}")
                    print(f"Size: {info.file_size}")
                    print(f"Modified datetime: {info.date_time}")

        except FileNotFoundError:
            print(f"File {self.input_filename} not found.")

    def run(self):
        self.read_file()
        self.solve_general_task()
        self.solve_personal_task()
        print(self.answers)
        self.write_file_and_archive()
        self.get_archive_file_info()
