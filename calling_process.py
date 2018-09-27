import os
import sys

program = "python"
print("Calling process")
arguments = ["training_day_5.py"]
os.execvp(program, (program, )+ tuple(arguments))
print("Ending process")

os.path.