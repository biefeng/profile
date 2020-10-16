import jsonpickle


class Animal:

    def __init__(self, name, age):
        self._name = name
        self._age = age


a = Animal("1", 1)

print(jsonpickle.encode(a, unpicklable=False))
