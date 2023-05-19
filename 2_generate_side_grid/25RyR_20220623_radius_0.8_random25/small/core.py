from side_grid import main
import time

k = 0
num = 0
for i in range(60, -61, -30):
    for j in range(-60, 61, 30):
        num += main(j, i)
        print("boun[" + str(k) + "] = " + str(num))
        k += 1
        time.sleep(0.1)
