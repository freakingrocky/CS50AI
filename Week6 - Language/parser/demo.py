import os
from sys import argv


def print_sentence(path):
    with open(path, 'r') as f:
        print(f.readline().strip('\n').strip('.').center(os.get_terminal_size().columns, "_"))


def correct():
    for i in range(1, 11):
        print(f"Correct Sentence {str(i)}".center(os.get_terminal_size().columns, "="))
        print_sentence("./sentences/"+str(i)+".txt")
        os.system('cmd /c "python parser.py ./sentences/$.txt"'.replace("$", str(i)))
    print("\nDONE TESTING...\n\n\n")


def incorrect():
    for i in range(1, 3):
        print(f"Incorrect Sentence {str(i)}".center(os.get_terminal_size().columns, "="))
        print_sentence("./reject/"+str(i)+".txt")
        os.system('cmd /c "python parser.py ./reject/$.txt"'.replace("$", str(i)))
    print("\nDONE REJECTION TESTING...\n\n")


if len(argv) == 2:
    if argv[1].lower() == "correct":
        correct()
    if argv[1].lower() == "incorrect":
        incorrect()
    exit()

correct()
incorrect()
