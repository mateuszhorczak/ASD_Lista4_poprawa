import pickle


class Node:
    def __init__(self, person_surname, person_name, person_address, person_number):
        self.surname = person_surname
        self.name = person_name
        self.address = person_address
        self.number = person_number
        self.balance_status = 0
        self.parent = None
        self.right = None
        self.left = None


class AVLTree:
    def __init__(self):
        self.root = None

    def insertNode(self, person_surname, person_name, person_address, person_number):
        node = Node(person_surname, person_name, person_address, person_number)

        parent_node = None
        temp_node = self.getRoot()

        while temp_node is not None:
            parent_node = temp_node
            if node.surname > temp_node.surname or \
                    (node.surname == temp_node.surname and node.name > temp_node.name) or \
                    (node.surname == temp_node.surname and node.name == temp_node.name and
                     node.address > temp_node.address):
                temp_node = temp_node.right
            else:
                temp_node = temp_node.left
        node.parent = parent_node

        if parent_node is None:
            self.root = node
        elif node.surname > parent_node.surname or \
                (node.surname == parent_node.surname and node.name > parent_node.name) or \
                (node.surname == parent_node.surname and node.name == parent_node.name and
                 node.address > parent_node.address):
            parent_node.right = node
        else:
            parent_node.left = node

        self.checkBalanceStatus(node)

    def checkBalanceStatus(self, node):
        if node.balance_status > 1 or node.balance_status < -1:
            self.balanceTree(node)
            return

        if node.parent is not None:
            if node == node.parent.right:
                node.parent.balance_status += 1
            if node == node.parent.left:
                node.parent.balance_status -= 1
            if node.parent.balance_status != 0:
                self.checkBalanceStatus(node.parent)

    def balanceTree(self, node):
        if node.balance_status > 1:
            if node.right.balance_status > 0:  # Left Rotation
                self.leftRotate(node, 0)
            else:  # Left Right Rotation
                self.rightRotate(node.right, 1)
                self.leftRotate(node, 0)
        else:
            if node.left.balance_status < 0:  # Right Rotation
                self.rightRotate(node, 0)
            else:  # Right Left Rotation
                self.leftRotate(node.left, 1)
                self.rightRotate(node, 0)

    def getRoot(self):
        return self.root

    def rightRotate(self, node, double_rotate):
        temp_node = node.left
        node.left = temp_node.right

        if temp_node.right is not None:
            temp_node.right.parent = node

        temp_node.parent = node.parent
        if node.parent is None:
            self.root = temp_node
        elif node == node.parent.right:
            node.parent.right = temp_node
        else:
            node.parent.left = temp_node

        temp_node.right = node
        node.parent = temp_node
        
        if temp_node.parent is not None:
            if temp_node.balance_status == temp_node.parent.right.balance_status and \
                    node.left is None and double_rotate == 1:
                temp_node.parent.balance_status += 1
        
        node.balance_status -= (min(0, temp_node.balance_status) - 1)
        temp_node.balance_status += (max(0, node.balance_status) + 1)

    def leftRotate(self, node, double_rotate):
        temp_node = node.right
        node.right = temp_node.left

        if temp_node.left is not None:
            temp_node.left.parent = node

        temp_node.parent = node.parent
        if node.parent is None:
            self.root = temp_node
        elif node == node.parent.right:
            node.parent.right = temp_node
        else:
            node.parent.left = temp_node

        temp_node.left = node
        node.parent = temp_node
        
        if temp_node.parent is not None:
            if temp_node.balance_status == temp_node.parent.left.balance_status and \
                    node.right is None and double_rotate == 1:
                temp_node.parent.balance_status += 1
        
        node.balance_status -= (max(0, temp_node.balance_status) + 1)
        temp_node.balance_status += (min(0, node.balance_status) - 1)

    def deleteNode(self, surname, name, address):
        self.delete(self.root, surname, name, address)

    def delete(self, node, surname, name, address):
        if node is None:
            print("Nie ma takiego abonenta w ksiazce")
            return node

        if surname > node.surname or \
                (surname == node.surname and name > node.name) or \
                (surname == node.surname and name == node.name and address > node.address):
            self.delete(node.right, surname, name, address)
        if surname < node.surname or \
                (surname == node.surname and name < node.name) or \
                (surname == node.surname and name == node.name and address < node.address):
            self.delete(node.left, surname, name, address)

        if surname == node.surname and name == node.name and address == node.address:
            if node.right is None and node.left is None:  # wezel nie ma dzieci
                if node.parent is None:  # drzewo jednoelementowe
                    self.root = None
                    print("Usunieto ostatni element ksiazki")
                    return
                if node.parent.left == node:
                    node.parent.balance_status += 1
                    node.parent.left = None
                elif node.parent.right == node:
                    node.parent.balance_status -= 1
                    node.parent.right = None
                print("Usunieto osobe")

            elif node.right is None:  # wezel gdy ma tylko lewe dziecko
                temp_node = node
                node = node.left
                if temp_node.parent is None:  # temp_node jest rootem
                    temp_node.surname = node.surname
                    temp_node.name = node.name
                    temp_node.address = node.address
                    temp_node.balance_status = node.balance_status
                    node.parent.left = None

                    self.delete(node, node.surname, node.name, node.address)
                    return
                if temp_node.parent.right == temp_node:
                    temp_node.parent.right = node
                    node.parent = node.parent.parent
                else:
                    temp_node.parent.left = node
                    node.parent = node.parent.parent
                print("Usunieto osobe")

            elif node.left is None:  # wezel gdy ma tylko prawe dziecko
                temp_node = node
                node = node.right
                if temp_node.parent is None:  # temp_node jest rootem
                    temp_node.surname = node.surname
                    temp_node.name = node.name
                    temp_node.address = node.address
                    temp_node.balance_status = node.balance_status
                    node.parent.right = None
                    self.delete(node, node.surname, node.name, node.address)
                    return
                if temp_node.parent.right == temp_node:
                    temp_node.parent.right = node
                    node.parent = node.parent.parent
                else:
                    temp_node.parent.left = node
                    node.parent = node.parent.parent
                print("Usunieto osobe")

            else:  # wezel gdy ma prawe i lewe dziecko
                temp_node = getMinFromRight(node.right)
                node.surname = temp_node.surname
                node.name = temp_node.name
                node.address = temp_node.address
                node.balance_status = temp_node.balance_status

                self.delete(node.right, temp_node.surname, temp_node.name, temp_node.address)  # usuwa zbedny element

            while node.parent is not None:
                if node.parent.right == node and node.balance_status == 0:
                    node.parent.balance_status -= 1
                if node.parent.left == node and node.balance_status == 0:
                    node.parent.balance_status += 1
                node = node.parent
                if node.balance_status > 1 or node.balance_status < -1:
                    self.balanceTree(node)
                return

    def searchPerson(self, surname, name, address):
        return self.searchPersonHelper(self.root, surname, name, address)

    def searchPersonHelper(self, node, surname, name, address):
        if node is None:
            return None
        if surname == node.surname and name == node.name and address == node.address:
            return node
        if surname > node.surname or \
                (surname == node.surname and name > node.name) or \
                (surname == node.surname and name == node.name and address > node.address):
            return self.searchPersonHelper(node.right, surname, name, address)
        return self.searchPersonHelper(node.left, surname, name, address)

    def getPersons(self, node, list_of_persons):
        if node is None:
            return
        self.getPersons(node.left, list_of_persons)
        person = [node.surname, node.name, node.address, node.number]
        if person[0] != 0 and person[1] != 0 and person[2] != 0:
            list_of_persons.append(person)
        self.getPersons(node.right, list_of_persons)


def getMinFromRight(node):
    while node.left is not None:
        node = node.left
    return node


def getMaxFromLeft(node):
    while node.right is not None:
        node = node.right
    return node


def switch_choice(num):
    def add():
        print("1 - Dodawanie: Podaj w nowych liniach: Imie, Nazwisko, adres, numer(y) telefonu (jak wiecej niz jeden to"
              "po spacji)")
        name = str(input())
        surname = str(input())
        address = str(input())
        number = str(input())
        phone_book.insertNode(surname, name, address, number)
        print("Dodano abonenta")

    def delete():
        print("2 - Usuwanie: Podaj w nowych liniach: Imie, Nazwisko, adres")
        name = str(input())
        surname = str(input())
        address = str(input())
        phone_book.deleteNode(surname, name, address)

    def search():
        print("3 - Wyszukiwanie: Podaj w nowych liniach: Imie, Nazwisko, adres")
        name = str(input())
        surname = str(input())
        address = str(input())
        searched_node = phone_book.searchPerson(surname, name, address)
        print(searched_node.number) if searched_node is not None else print("Abonent nie istnieje")

    def save_data():
        print("4 - Zapis: Podaj nazwe pliku:")
        file_name = str(input())
        list_of_persons = []
        phone_book.getPersons(phone_book.getRoot(), list_of_persons)
        with open(f'{file_name}', 'wb') as file:
            pickle.dump(list_of_persons, file)
        print(f'Zapisano do pliku: {file_name}')

    def load_data():
        print('5 - Wczytywanie danych: Podaj nazwe pliku:')
        file_name = str(input())
        with open(f'{file_name}', 'rb') as file:
            persons = pickle.load(file)
        for person in persons:
            phone_book.insertNode(str(person[0]), str(person[1]), str(person[2]), str(person[3]))
        print(f'Wczytano dane z pliku: {file_name}')

    match num:
        case 1:
            add()
        case 2:
            delete()
        case 3:
            search()
        case 4:
            save_data()
        case 5:
            load_data()
        case 6:
            exit()
        case _:
            print("Zly przycisk")

    print("\n")


if __name__ == '__main__':
    phone_book = AVLTree()
    while True:
        print("Co chcesz zrobic?")
        print(" 1 - Wstawic nowego abonenta \n 2 - Usunac abonenta \n 3 - Wyszukac numer(y) abonenta \n "
              "4 - zapis danych do pliku \n 5 - wczytac dane z pliku \n 6 - wyjsc")
        switch_choice(int(input()))
