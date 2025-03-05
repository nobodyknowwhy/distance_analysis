import heapq
from collections import Counter

def topKFrequent(nums, k):
    # 统计频率
    count = Counter(nums)
    # 使用小根堆
    heap = []
    for key, freq in count.items():
        heapq.heappush(heap, (freq, key))
        if len(heap) > k:
            heapq.heappop(heap)
    # 提取结果
    return [item[1] for item in heap[::-1]]  # 逆序输出

print(topKFrequent([1,1,5,3,4,3,57,3,3,1,5,4,54,54,24,55], 3))