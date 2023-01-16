class Node:
    def __init__(self, val):
        self.value = val
        self.balance_status = 0
        self.parent = None
        self.right = None
        self.left = None


class AVLTree:
    def __init__(self):
        self.root = None

    def insertNode(self, value):
        node = Node(value)
        node.parent = None
        node.left = None
        node.right = None

        parent_node = None
        temp_node = self.getRoot()

        while temp_node is not None:
            parent_node = temp_node
            if node.value > temp_node.value:
                temp_node = temp_node.right
            else:
                temp_node = temp_node.left
        node.parent = parent_node

        if parent_node is None:
            self.root = node
        elif node.value > parent_node.value:
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
            if node.right.balance_status > 0:  # Left Rotation TODO check
                self.leftRotate(node, 0)
            else:  # Left Right Rotation TODO check
                self.rightRotate(node.right, 1)
                # node.balance_status -= 1
                self.leftRotate(node, 0)
        else:
            if node.left.balance_status < 0:  # Right Rotation TODO check
                self.rightRotate(node, 0)
            else:  # Right Left Rotation TODO check
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
                    node.left is None and double_rotate == 1:  # TODO HAHA
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
                    node.right is None and double_rotate == 1:  # TODO HAHA
                temp_node.parent.balance_status -= 1

        node.balance_status -= (max(0, temp_node.balance_status) + 1)
        temp_node.balance_status += (min(0, node.balance_status) - 1)

    def deleteNode(self, value):
        self.delete(self.root, value)

    def delete(self, node, value):
        if node is None:
            print("Nie ma takiego abonenta w ksiazce")
            return node

        if value > node.value:
            self.delete(node.right, value)
        if value < node.value:
            self.delete(node.left, value)

        if value == node.value:
            if node.right is None and node.left is None:  # wezel nie ma dzieci
                if node.parent is None:  # drzewo jednoelementowe
                    self.root = None
                    print("Usunieto ostatni element ksiazki")
                    return
                if node.parent.left == node:
                    node.parent.balance_status += 1     # TODO check
                    node.parent.left = None
                elif node.parent.right == node:
                    node.parent.balance_status -= 1
                    node.parent.right = None
                print("Usunieto osobe")

            elif node.right is None:  # wezel gdy ma tylko lewe dziecko
                temp_node = node
                node = node.left
                # node.parent = temp_node.parent
                if temp_node.parent is None:  # temp_node jest rootem
                    temp_node.value = node.value
                    temp_node.balance_status = node.balance_status
                    node.parent.left = None

                    self.delete(node, node.value)
                    return
                if temp_node.parent.right == temp_node:
                    temp_node.parent.right = node
                    node.parent = node.parent.parent
                    # print("usunieto osobe")
                else:
                    temp_node.parent.left = node
                    node.parent = node.parent.parent
                    # print("Usunieto osobe")
                print("Usunieto osobe")

            elif node.left is None:  # wezel gdy ma tylko prawe dziecko
                temp_node = node
                node = node.right
                # node.parent = temp_node.parent
                if temp_node.parent is None:    # temp_node jest rootem
                    temp_node.value = node.value
                    temp_node.balance_status = node.balance_status
                    node.parent.right = None
                    self.delete(node, node.value)
                    return
                if temp_node.parent.right == temp_node:
                    temp_node.parent.right = node
                    node.parent = node.parent.parent
                else:
                    temp_node.parent.left = node
                    node.parent = node.parent.parent
                print("Usunieto osobe")

            else:  # wezel gdy ma prawe i lewe dziecko
                temp_node = self.getMinFromRight(node.right)
                node.value = temp_node.value
                node.balance_status = temp_node.balance_status

                self.delete(node.right, temp_node.value)  # usuwa zbedny element

            while node.parent is not None:
                if node.parent.right == node and node.balance_status == 0:   # TODO check
                    node.parent.balance_status -= 1
                if node.parent.left == node and node.balance_status == 0:    # TODO check
                    node.parent.balance_status += 1
                node = node.parent
                if node.balance_status > 1 or node.balance_status < -1:
                    self.balanceTree(node)
                print("orzeszki")
                return

    def getMinFromRight(self, node):
        while node.left is not None:
            node = node.left
        return node

    def getMaxFromLeft(self, node):
        while node.right is not None:
            node = node.right
        return node

    def searchValue(self, value):
        return self.searchValueHelper(self.root, value)

    def searchValueHelper(self, node, value):
        if node is None:
            print("Nie ma takiej osoby w ksiazce")
            return None
        if value == node.value:
            return node
        if value > node.value:
            return self.searchValueHelper(node.right, value)
        return self.searchValueHelper(node.left, value)


if __name__ == '__main__':
    # print("psst")
    tree = AVLTree()
    # tree.insertNode(10)
    tree.insertNode(12)
    tree.insertNode(20)
    tree.insertNode(5)
    tree.insertNode(2)
    tree.insertNode(7)
    tree.insertNode(22)
    tree.insertNode(19)
    tree.deleteNode(12)
    tree.insertNode(50)
    tree.insertNode(1)
    tree.insertNode(6)
    tree.insertNode(25)
    tree.insertNode(3)
    print("dupa")

    # tree.insertNode(20)
    # tree.insertNode(30)
    # tree.insertNode(50)
    # tree.insertNode(45)
    # tree.insertNode(40)
    # tree.insertNode(90)
    # tree.insertNode(70)
    # tree.insertNode(60)
    # print(tree.searchValue(90).value)
    # # print(tree.searchValue(6).value)
    # # print(tree.searchValue(7).value)
