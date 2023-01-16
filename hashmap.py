from llist import sllist


class HashMap:
    def __init__(self, size):
        if size < 0:
            print('Tablica nie moze miec ujemnej ilosci elementow !')
            exit()
        self.size = size
        self.hashmap = [None] * self.size

    def hashValue(self, value):
        if value is None:
            return None
        if isinstance(value, int):  # tylko int
            return value % self.size
        return None

    def putValue(self, value):
        hashed_value = self.hashValue(value)
        if self.hashmap[hashed_value] is None:  # jesli w komorce hashmapy nic nie ma
            self.hashmap[hashed_value] = sllist([value])
        else:
            self.hashmap[hashed_value].append(value)
        print(f'Dodano wartosc: {value} do tablicy')

    def getValue(self, value):
        hashed_value = self.hashValue(value)
        if self.hashmap[hashed_value] is None:
            print(f'Nie ma elementu {value} w tablicy')
            return None
        for item in self.hashmap[hashed_value]:
            if item == value:
                print(f'O to element: {item}')
                return item

    def removeValue(self, value):
        hashed_value = self.hashValue(value)
        if self.hashmap[hashed_value] is None:
            print(f'Nie ma elementu: {value} w tablicy')
            return
        temp = self.hashmap[hashed_value].first
        for item in self.hashmap[hashed_value]:
            if item == value:
                print(f'Usunieto element: {value}')
                self.hashmap[hashed_value].remove(temp)
                return
            temp = temp.next
        print(f'Nie ma elementu: {value} w tablicy')

    def clear(self):
        self.hashmap = [None] * self.size
        print('Wyczyszczono tablice')


if __name__ == '__main__':
    # Wartosci i operacje do testowania
    size_of_hash_map = 3
    hash_array = HashMap(size_of_hash_map)
    hash_array.getValue(0)
    hash_array.removeValue(0)
    hash_array.putValue(1)
    hash_array.putValue(2)
    hash_array.putValue(3)
    hash_array.putValue(4)
    hash_array.removeValue(4)
    hash_array.putValue(5)
    hash_array.putValue(6)
    hash_array.putValue(7)
    hash_array.putValue(8)
    hash_array.putValue(9)
    hash_array.putValue(10)
    hash_array.putValue(11)
    hash_array.removeValue(5)
    hash_array.removeValue(1)
    hash_array.removeValue(2)
    hash_array.removeValue(3)
    val = hash_array.getValue(10)
    print(val)
    hash_array.clear()
