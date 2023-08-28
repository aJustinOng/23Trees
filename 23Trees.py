class Node:
    def __init__(self,value):
        self.value1 = value
        self.value2 = None
        self.left = None #left child
        self.mid = None #mid child
        self.right = None #right child
        self.parent = None #parent

    def is_leaf(self):
        #check if a node had children
        return not self.left and not self.mid and not self.right

    def is_full(self):
        #check if a node held 2 values
        return self.value2 is not None

    def get_child(self,value):
        #get child by a given value
        if self.value2: #if 3-node
            if value < self.value1:
                return self.left
            elif value < self.value2:
                return self.mid
            return self.right
        else: #if 2-node
            if value < self.value1:
                return self.left
            return self.right

    def brother(self):
        #return a brother of a node
        if self.parent: #only run when the node has a parent
            if not self.parent.is_full(): #2-node
                if self.parent.left is self:
                    return self.parent.right
                return self.parent.left
            else: #3-node
                if self.parent.mid is self:
                    if self.parent.right.is_full():
                        return self.parent.right
                    if self.parent.left.is_full():
                        return self.parent.left
                    return self.parent.right
                return self.parent.mid


class TwoThreeTree:
    def __init__(self):
        self.root = None

    def search(self,value):
        if not self.root:
            print('The tree is null!')
            return
        return  self.search_node(self.root,value)

    def search_node(self,root,value):
        if not root:
            return None #return None if node is not found
        if value == root.value1 or value == root.value2:
            return root #node is found
        return self.search_node(root.get_child(value),value) #search from the node's children

    def insert(self,value):
        print('Insert', value)
        if not self.root: #if the tree is null
            self.root = Node(value)
            return
        self.insert_node(self.root,value)

    def insert_node(self,root,value):
        while not root.is_leaf(): #insert only at leaf node
            root = root.get_child(value)
        if not root.is_full(): #if the node we insert is not full
            self.put_item(root,value)
        else: #if the node we insert is full
            self.put_item_full(root,value)

    def put_item(self,leaf,value):
        if value < leaf.value1:
            leaf.value2 = leaf.value1
            leaf.value1 = value
        else:
            leaf.value2 = value

    def put_item_full(self,leaf,value):
        #decide which value should be pushed upward
        pvalue, new_node = self.split(leaf,value)

        while leaf.parent: #if a parent exist, no new node is needed
            if not leaf.parent.is_full(): #if parent is 2-node
                self.put_item(leaf.parent,pvalue)
                if leaf.parent.left is leaf:
                    leaf.parent.mid = new_node
                else:
                    leaf.parent.mid = leaf; leaf.parent.right = new_node
                new_node.parent = leaf.parent
                break #leave while loop
            else: #if parent is 3-node
                pvalue_p, new_node_p = self.split(leaf.parent,pvalue) #parent needs to be split
                if leaf.parent.left is leaf: #case1: the split node is parent's left child
                    new_node_p.left = leaf.parent.mid; leaf.parent.mid.parent = new_node_p
                    new_node_p.right = leaf.parent.right; leaf.parent.right.parent = new_node_p
                    leaf.parent.right = new_node; new_node.parent = leaf.parent
                elif leaf.parent.mid is leaf: #case2: the split node is parent's mid child
                    new_node_p.left = new_node; new_node.parent = new_node_p
                    new_node_p.right = leaf.parent.right; leaf.parent.right.parent = new_node_p
                    leaf.parent.right = leaf.parent.mid
                else: #case3: the split node is parent's right child
                    leaf.parent.right = leaf.parent.mid; temp = leaf.parent.right
                    new_node_p.left = leaf; leaf.parent = new_node_p
                    new_node_p.right = new_node; new_node.parent = new_node_p
                    leaf = temp
                leaf.parent.mid = None #convert to 2-node
                leaf = leaf.parent; pvalue = pvalue_p; new_node = new_node_p #move leaf,pvalue,new_node upward
        else: #if no parent exists, a new node is needed
            new_root = Node(pvalue)
            new_root.left = leaf; new_root.right = new_node
            leaf.parent = new_root; new_node.parent = new_root
            self.root = new_root

    def split(self,leaf,value):
        new_node = Node(None)

        if value < leaf.value1: #value1 needs to be put upward
            pvalue = leaf.value1
            leaf.value1 = value
            new_node.value1 = leaf.value2
        elif value < leaf.value2: #value needs to be put upward
            pvalue = value
            new_node.value1 = leaf.value2
        else:
            pvalue = leaf.value2 #value2 needs to be put upward
            new_node.value1 = value
        leaf.value2 = None
        return  pvalue, new_node

    def remove(self,value):
        if not self.root:
            print("The tree is null!")
            return
        print('-----------------')
        print('Removing', value)
        node = self.search(value) #search the remove node
        if node is None: #if the node does not exist
            print('The value does not exist!')
            return
        if node.is_leaf(): #if the remove node is leaf
            self.remove_leaf(node, value)
        else: #if it is not a leaf
            if node.is_full() and node.value2 == value: #swap the predecessor value and remove value
                predecessor = self.get_predecessor(node.mid)
                if predecessor.is_full():
                    predecessor.value2, node.value2 = node.value2, predecessor.value2
                else:
                    predecessor.value1, node.value2 = node.value2, predecessor.value1
            else: #swap the predecessor value and remove value
                predecessor = self.get_predecessor(node.left)
                if predecessor.is_full():
                    predecessor.value2, node.value1 = node.value1, predecessor.value2
                else:
                    predecessor.value1, node.value1 = node.value1, predecessor.value1
            self.remove_leaf(predecessor,value) #remove the value

    def get_predecessor(self,root):
        if root.right:
            return self.get_predecessor(root.right)
        return root

    def remove_leaf(self,node,value):
        if node.is_full(): #if node is full
            self.remove_item(node, value) #remove value without adjustment
        else:
            brother = node.brother()
            while node.parent:
                if brother.is_full(): #case1
                    self.leaf_case1(node, brother)
                    break
                else:
                    if node.parent.is_full(): #case2
                        self.leaf_case2(node, brother)
                        break
                    else: #case3
                        node = self.merge(node, brother)
                        brother = node.brother()
            else:
                self.root = node.mid
                del node

    def remove_item(self,node,value):
        #remove a value from a full node
        if node.value1 == value:
            node.value1 = node.value2
        node.value2 = None

    def leaf_case1(self,node,brother):
        node.value1 = None #remove the value
        if node is node.parent.left: #if the node is in the left
            #put value1 of parent in node and move value1 in brother to parent
            node.value1 = node.parent.value1
            node.parent.value1 = brother.value1
            if brother.left: #if brother has child, move it to node's child
                node.left = node.mid
                node.right = brother.left
                brother.left.parent = node
                brother.left = brother.mid
            self.remove_item(brother,brother.value1)
        elif node is node.parent.right: #if the node is in the right
            if node.parent.is_full(): #if parent is full
                #put value2 of parent into node and value2 of brother in parent
                node.value1 = node.parent.value2
                node.parent.value2 = brother.value2
            else: #if parent is not full
                #put value1 of parent into node and value2 of brother in parent
                node.value1 = node.parent.value1
                node.parent.value1 = brother.value2
            if brother.right: #if brother has children, move it into node's child
                node.right = node.mid
                node.left = brother.right
                brother.right.parent = node
                brother.right = brother.mid
            self.remove_item(brother,brother.value2)
        else: #if the node is in the mid
            if brother is node.parent.right: #if brother is in the right
                #put value2 of parent into node and value1 of brother in parent
                node.value1 = node.parent.value2
                node.parent.value2 = brother.value1
                if brother.left: #if brother has children, move it into node's child
                    node.left = node.mid
                    node.right = brother.left
                    brother.left.parent = node
                    brother.left = brother.mid
                self.remove_item(brother,brother.value1)
            else: #if brother is in the left
                # put value1 of parent into node and value2 of brother in parent
                node.value1 = node.parent.value1
                node.parent.value1 = brother.value2
                if brother.right: #if brother has children, move it into node's child
                    node.right = node.mid
                    node.left = brother.right
                    brother.right.parent = node
                    brother.right = brother.mid
                self.remove_item(brother,brother.value2)
        #remove mid of brother and node
        brother.mid = None
        node.mid = None

    def leaf_case2(self,node,brother):
        node.value1 = None #remove the value
        if node is node.parent.left: #if node is in the left
            #put parent's value1 into brother
            self.put_item(brother, node.parent.value1)
            if node.mid: #if node's child exists, move it into brother's child
                brother.mid = brother.left
                brother.left = node.mid
                node.mid.parent = brother
            node.parent.left = brother #make brother the left node
            self.remove_item(node.parent, node.parent.value1)
        elif node is node.parent.right: #if node is in the right
            #put parent's value2 into brother
            self.put_item(brother, node.parent.value2)
            if node.mid: #if node's child exists, move it into brother's child
                brother.mid = brother.right
                brother.right = node.mid
                node.mid.parent = brother
            node.parent.right = brother #make brother the right node
            self.remove_item(node.parent, node.parent.value2)
        else: #if node is in the mid
            # put parent's value2 into brother
            self.put_item(brother, node.parent.value2)
            if node.mid: #if node's child exists, move it into brother's child
                brother.mid = brother.left
                brother.left = node.mid
                node.mid.parent = brother
            self.remove_item(node.parent, node.parent.value2)
        node.parent.mid = None
        del node #remove empty node

    def merge(self,node,brother):
        #put parent's value1 into brother
        self.put_item(brother,node.parent.value1)
        #if the node is in the left
        if node is node.parent.left:
            if node.mid:
                brother.mid = brother.left
                brother.left = node.mid
                node.mid.parent = brother
            node.parent.right = None
        else: #if the node is in the right
            if node.mid:
                brother.mid = brother.right
                brother.right = node.mid
                node.mid.parent = brother
            node.parent.left = None
        node.parent.mid = brother
        temp = node
        node = node.parent
        del temp
        return node

    def in_order(self,root):
        if not root.parent:
            print('-----In Order Traversal-----')
        if root.is_full():
            if root.left:
                self.in_order(root.left)
            print(root.value1, end=' ')
            if root.mid:
                self.in_order(root.mid)
            print(root.value2, end=' ')
            if root.right:
                self.in_order(root.right)
        else:
            if root.left:
                self.in_order(root.left)
            print(root.value1, end=' ')
            if root.right:
                self.in_order(root.right)
        if not root.parent:
            print('')

    def traversal(self):
        if not self.root:
            print('The tree is null!')
            return
        self.in_order(self.root)

    def printTop2Tiers(self):
        if not self.root:
            print('The tree is null!')
            return
        print('---------------2-3 Tree---------------')
        if self.root.is_full():
            print('[', self.root.value1, ',', self.root.value2, ']')
            if not self.root.left:
                return
            if self.root.left.is_full() and not self.root.mid.is_full() and not self.root.right.is_full():
                print('[',self.root.left.value1,',',self.root.left.value2,'][',self.root.mid.value1,'][',self.root.right.value1,']')
            elif not self.root.left.is_full() and self.root.mid.is_full() and not self.root.right.is_full():
                print('[',self.root.left.value1,'][',self.root.mid.value1,',',self.root.mid.value2,'][',self.root.right.value1,']')
            elif not self.root.left.is_full() and not self.root.mid.is_full() and self.root.right.is_full():
                print('[',self.root.left.value1,'][',self.root.mid.value1,'][',self.root.right.value1,',',self.root.right.value2,']')
            elif self.root.left.is_full() and self.root.mid.is_full() and not self.root.right.is_full():
                print('[',self.root.left.value1,',',self.root.left.value2,'][',self.root.mid.value1,',',self.root.mid.value2,'][',self.root.right.value1,']')
            elif self.root.left.is_full() and not self.root.mid.is_full() and self.root.right.is_full():
                print('[',self.root.left.value1,',',self.root.left.value2,'][',self.root.mid.value1,'][',self.root.right.value1,',',self.root.right.value2,']')
            elif not self.root.left.is_full() and self.root.mid.is_full() and self.root.right.is_full():
                print('[',self.root.left.value1,'][',self.root.mid.value1,',',self.root.mid.value2,'][',self.root.right.value1,',',self.root.right.value2,']')
            elif not self.root.left.is_full() and not self.root.mid.is_full() and not self.root.right.is_full():
                print('[',self.root.left.value1, '][', self.root.mid.value1,'][',self.root.right.value1,']')
            else:
                print('[',self.root.left.value1,',',self.root.left.value2,'][',self.root.mid.value1,',',self.root.mid.value2,'][',self.root.right.value1,',',self.root.right.value2,']')
        else:
            print('[', self.root.value1, ']')
            if not self.root.left:
                return
            if self.root.left.is_full() and not self.root.right.is_full():
                print('[',self.root.left.value1, ',', self.root.left.value2, '][', self.root.right.value1,']')
            elif not self.root.left.is_full() and self.root.right.is_full():
                print('[',self.root.left.value1, '][', self.root.right.value1, ',', self.root.right.value2,']')
            elif not self.root.left.is_full() and not self.root.right.is_full():
                print('[', self.root.left.value1, '][', self.root.right.value1,']')
            else:
                print('[',self.root.left.value1, ',', self.root.left.value2, '][', self.root.right.value1, ',', self.root.right.value2,']')

tree = TwoThreeTree()
for i in range(10):
    tree.insert(i)
    tree.printTop2Tiers()
#tree.traversal()
