import random as rd
import matplotlib.pyplot as plt


ones_position = []
for i in range(1000):
    salt = rd.randint(0,65356)
    second_salt = rd.randint(0,65356)
    positions = []
    for i in range(100):
        new_i = ((0x0000FFFF & (i+salt)) << 16) + ((0xFFFF0000 & (i+salt)) >> 16) ^ (second_salt)
        # print(new_i)
        positions.append((i,new_i))
    sorted_positions = sorted(positions, key=lambda x: x[1])
    print(sorted_positions)
    for x in range(len(sorted_positions)):
        if sorted_positions[x][0] == 1:
            ones_position.append(x)
print(ones_position)

plt.plot(ones_position)
plt.show()