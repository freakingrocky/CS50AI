"""Demonstrate the project using all combimations."""
import os
from time import sleep, time, localtime
from sys import argv

try:
    argv[1]
except IndexError:
    argv = [0, '-i', 0]

if argv[1] == "-i":
    argv[1] = 1000000


print("_"*35, "PSET 4 - Shopping", "_"*35)
start_time = localtime()
print(
    f"Start Time: {start_time.tm_hour}h:{start_time.tm_min}m:{start_time.tm_sec}s")
runtime = 0.0
try:
    for i in range(argv[1]):
        print("_"*35, f"Iteration {i + 1}", "_"*35)
        cmd = f'cmd /c "python shopping.py shopping.csv'
        start = time()
        print("CMD:", cmd.replace("cmd /c", "").replace('"', ""), '\n')
        os.system(cmd)
        print("-"*20)
        rt = round(time() - start, 2)
        runtime += rt
        print(f"Runtime: {rt}s")
        if i == argv[1]:
            break
        print(f"Sleeping {argv[2]}s")
        sleep(float(argv[2]))
except:
    print("-"*os.get_terminal_size().columns)
    print("Stopped by user.")

print()
end_time = localtime()
print(
    f"End Time: {end_time.tm_hour}h:{end_time.tm_min}m:{end_time.tm_sec}s")

print(f"Total run time is {round(runtime, 2)}s")
