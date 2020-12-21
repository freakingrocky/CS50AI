"""Demonstrate the project using all combimations."""
import os
from time import sleep, time, localtime
from sys import argv

try:
    argv[1]
except IndexError:
    argv = [0, 0]

print("PSET 3 - Crossword".center(os.get_terminal_size().columns, "="))
start_time = localtime()
print(
     f"Start Time: {start_time.tm_hour}h:{start_time.tm_min}m:{start_time.tm_sec}s")
runtime = 0.0
for i in range(3):
    for j in range(3):
        print(f'Structure{i} Words{j}'.center(
            os.get_terminal_size().columns, "_"))
        cmd = f'cmd /c "python generate.py data/structure{i}.txt data/words{j}.txt output.png'
        start = time()
        print("CMD:", cmd.replace("cmd /c", "").replace('"', ""))
        os.system(cmd)
        local_runtime = round(time() - start, 2)
        runtime += local_runtime
        print()
        print(f"Runtime: {local_runtime}s")
        if (i + j) == 4:
            break
        print(f"Sleeping {argv[1]}s")
        sleep(float(argv[1]))

print("Execution Complete".center(os.get_terminal_size().columns, "="))
end_time = localtime()
print(
    f"End Time: {end_time.tm_hour}h:{end_time.tm_min}m:{end_time.tm_sec}s")
end_time = ((end_time.tm_min*60)+end_time.tm_sec)

print(f"Total run time is {runtime}s")
