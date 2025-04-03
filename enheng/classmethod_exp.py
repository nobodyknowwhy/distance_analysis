class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_birth_year(cls, name, birth_year):
        current_year = 2023
        age = current_year - birth_year
        return cls(name, age)  # 返回一个新的 Person 实例

# 使用工厂方法创建实例
p1 = Person("Alice", 30)
p2 = Person.from_birth_year("Bob", 1990)

print(p1.age)  # 输出：30
print(p2.age)  # 输出：33