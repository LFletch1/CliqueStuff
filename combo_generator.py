# def print_combo(indices, iterable):
#     for i in indices:
#         print(iterable[i], end=', ')
#     print()

# combo_length = 4
# indices = [i for i in range(combo_length)]

# nums = 10
# numbers = [i for i in range(nums)]

# number_of_combos = 0
# while indices[0] <= (len(numbers) - combo_length):
#     number_of_combos += 1
#     p = len(indices) - 1
#     m = 1
#     while indices[p] + m == len(numbers):
#         p -= 1
#         m += 1
#     indices[p] += 1
#     for i in range(p+1, combo_length):
#         indices[i] = indices[i-1] + 1

# print(number_of_combos)

from itertools import combinations

class combo_generator:
    
    def __init__(self, combo_length, iterable):
        self.c = combo_length
        self.list = iterable
        self.indices = [i for i in range(combo_length)]
        self.combos_generated = 0

    def get_next_combo(self, valid_last_combo, combo_idx1, combo_idx2):

        if self.combos_generated == 0: # Generate first combo
            self.combos_generated += 1
            return [self.list[i] for i in range(self.c)]

        if not valid_last_combo:
            # print("LAST COMBO IS INVALID, combo = ", self.indices)
            assert combo_idx1 < combo_idx2, "First index needs to be less than the second"
            p = combo_idx2
            while self.indices[p] == len(self.list) - self.c + p:
                p -= 1
            self.indices[p] += 1
            for i in range(p+1, self.c):
                self.indices[i] = self.indices[i-1] + 1
        else:
            # print("LAST COMBO IS VALID, valid combo = ", self.indices)
            p = len(self.indices) - 1
            while self.indices[p] + len(self.indices) - p == len(self.list):
                p -= 1
            self.indices[p] += 1
            for i in range(p+1, self.c):
                self.indices[i] = self.indices[i-1] + 1
        
        if self.indices[0] <= (len(self.list) - self.c):
            combo_to_return = [self.list[idx] for idx in self.indices]
            self.combos_generated += 1
            return combo_to_return
        else:
            return False

combo_length = 4
l = [i for i in range(10)]

cg = combo_generator(combo_length, l)

invalid_pairs = [(0,5), (1,9), (2,4), (3,7), (4,5), (5,6), (5,7), (6,9)]

invalid_combos = 0
combo = cg.get_next_combo(True, 0, 0)
while combo:
    # print("COMBO GENERATED: ", combo)
    combo_valid = True
    idx1 = 0
    idx2 = 0
    for i in range(len(combo)):
        for j in range(i, len(combo)):
            if (combo[i], combo[j]) in invalid_pairs:
                invalid_combos += 1
                idx1 = i
                idx2 = j
                combo_valid = False
                break 
        if not combo_valid:
            break

    combo = cg.get_next_combo(combo_valid, idx1, idx2)

print("Combos Generated: ", cg.combos_generated)
print("Invalid Combos: ", invalid_combos)
print("Valid Combos: ", cg.combos_generated - invalid_combos)

valid_combos = 0
for combo in combinations(l, combo_length):
    valid_combo = True
    for i in range(len(combo)):
        for j in range(i, len(combo)):
            if (combo[i], combo[j]) in invalid_pairs:
                valid_combo = False
                break 
        if not valid_combo:
            break
    if valid_combo:
        valid_combos += 1

print("Valid combos: ", valid_combos)

