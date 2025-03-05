def outer():
    yield 1
    yield 2
    yield 3

# 创建生成器对象
gen = outer()

# 迭代生成器
for value in gen:
    print(value)

#报错
# print(gen.__next__())
# print(gen.__next__())
# print(gen.__next__())
# print(gen.__next__())

def gen():
    yield 1
    yield 2
    yield 3
g = gen()
print(sum(g) + sum(g))