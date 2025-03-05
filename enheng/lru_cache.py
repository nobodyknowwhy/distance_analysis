from functools import lru_cache

@lru_cache
def compute(lst):
    return sum(lst)

a = compute((1,2,3))  # TypeError: unhashable type: 'list'
print(compute.cache_info())
print(a)
a = compute((2,3,6))
print(a)
print(compute.cache_info())
compute.cache_clear()
print(compute.cache_info())