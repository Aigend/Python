import sys
import time
import psutil

# get pid from args
if len(sys.argv) < 2:
    print("missing pid arg")
    sys.exit()

# get process
l = len(sys.argv)
for i in range(1, l):
	print(sys.argv[i])
print(type(sys.argv[1]))