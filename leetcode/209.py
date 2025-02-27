
target = 11
nums = [1,1,1]

n_index = 0
sum_nums_now = 0
len_nums_now = 100

start_index = 0
end_index = 0

if target > sum(nums):
    print(0)
    exit(0)

if target == sum(nums):
    print(len(nums))
    exit(0)

while True:
    for x in range(end_index, len(nums)):
        sum_nums_now += nums[x]
        if sum_nums_now >= target:
            len_nums = x - start_index + 1
            if len_nums < len_nums_now:
                len_nums_now = len_nums
            end_index = x
            break

    for y in range(start_index, end_index + 1):
        sum_nums_now -= nums[y]
        if sum_nums_now < target:
            if end_index == len(nums) - 1:
                len_nums = end_index - y + 1
                if len_nums < len_nums_now:
                    len_nums_now = len_nums
            else:
                start_index = y + 1
                len_nums = end_index - y + 1
                if len_nums < len_nums_now:
                    len_nums_now = len_nums
            break

    if end_index == len(nums) - 1:
        break

    end_index += 1


print(len_nums_now)
