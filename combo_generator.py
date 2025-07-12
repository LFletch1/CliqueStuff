
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

# Need to make this a class. It needs to maintain state. i.e. keep track of the indices. 
# After asking for a combo, we should be able to provide a function which specifies whether the previous combo was problematic. If it is
# skip as many combos as possible. 

class combo_generator:
    
    def __init__(self, combo_length, iterable):
        self.c = combo_length
        self.list = iterable
        self.indices = [i for i in range(combo_length)]
        self.combos_generated = 0

    def get_next_combo(self, valid_last_combo):

        if self.indices[0] <= (len(self.list) - self.c):
            # return
            if not valid_last_combo:
                return False
            else:
                self.combos_generated += 1
                combo_to_return = [self.list[idx] for idx in self.indices]

                p = len(self.indices) - 1
                m = 1
                while self.indices[p] + m == len(self.list):
                    p -= 1
                    m += 1
                self.indices[p] += 1
                for i in range(p+1, self.c):
                    self.indices[i] = self.indices[i-1] + 1

                return combo_to_return
            
        else:
            return False

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

def print_combo(indices, iterable):
    for i in indices:
        print(iterable[i], end=', ')
    print()

combo_length = 4
l = [i for i in range(10)]

cg = combo_generator(combo_length, l)

combo = cg.get_next_combo(True)
while combo:
    print(combo)
    combo = cg.get_next_combo(True)

print(cg.combos_generated)