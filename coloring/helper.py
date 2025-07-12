
def prefix_sum(nums_list):
    new_list = [0] * len(nums_list)
    new_list[0] = nums_list[0]
    nums_list
    for i in range(1,len(nums_list)):
        new_list[i] = new_list[i-1] + nums_list[i]
    return new_list