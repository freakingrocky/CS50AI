"""Demonstrate the project using all combimations."""
import os
from time import sleep, time, localtime
from sys import argv

try:
    argv[1]
except IndexError:
    argv = [0, 0]


print("_"*35, "PSET 2 - Heredity", "_"*35)
start_time = localtime()
print(
    f"Start Time: {start_time.tm_hour}h:{start_time.tm_min}m:{start_time.tm_sec}s")
runtime = 0.0
for i in range(3):
    print("_"*35, f'Family{i}', "_"*35)
    cmd = f'cmd /c "python heredity.py data/family{i}.csv'
    start = time()
    print("CMD:", cmd.replace("cmd /c", "").replace('"', ""))
    os.system(cmd)
    print("-"*20)
    rt = round(time() - start, 2)
    runtime += rt
    print(f"Runtime: {rt}s")
    if i == 2:
        break
    print(f"Sleeping {argv[1]}s")
    sleep(float(argv[1]))

print("_"*135)
end_time = localtime()
print(
    f"End Time: {end_time.tm_hour}h:{end_time.tm_min}m:{end_time.tm_sec}s")

print(f"Total run time is {round(runtime, 2)}s")
