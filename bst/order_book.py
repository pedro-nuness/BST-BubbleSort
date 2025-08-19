class Node:
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity
        self.left = None
        self.right = None

class OrderBookBST:
    def __init__(self):
        self.root = None

    def remove(self, price):
        self.root = self._remove(self.root, price)

    def _remove(self, node, price):
        if node is None:
            return node

        if price < node.price:
            node.left = self._remove(node.left, price)
        elif price > node.price:
            node.right = self._remove(node.right, price)
        else:  
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._min_value_node(node.right)
            node.price = temp.price
            node.quantity = temp.quantity
            node.right = self._remove(node.right, temp.price)
            
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def insert(self, price, quantity):
        self.root = self._insert(self.root, price, quantity)

    def _insert(self, node, price, quantity):
        if node is None:
            return Node(price, quantity)
        if price == node.price:
            node.quantity += quantity
        elif price < node.price:
            node.left = self._insert(node.left, price, quantity)
        else:
            node.right = self._insert(node.right, price, quantity)
        return node

    def inorder(self, node=None):
        if node is None:
            node = self.root
        if not node:
            return []
        result = []
        if node.left:
            result += self.inorder(node.left)
        result.append((node.price, node.quantity))
        if node.right:
            result += self.inorder(node.right)
        return result