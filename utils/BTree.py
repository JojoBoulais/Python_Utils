from sorting_utils import merge_sort
import math

class BNode():
    def __init__(self, parent_node, btree, elements=None, childs=None):
        self.parent_node = parent_node
        self.btree = btree
        self.elements = elements or []
        self.childs = childs or []

    def add_element(self, element, upward=False):

        # Recursing to proper leaf (Comparing elements)
        if self.childs and not upward:

            # Adding to the end child
            if element > self.elements[-1]:
                self.childs[-1].add_element(element)
                return self

            # Comparing all others
            for i, e in enumerate(self.elements[:-1]):
                if element < e:
                    self.childs[i].add_element(element)
                    break
            return self

        # Is a leaf or splitting-------------------------

        #Just Adding an element
        self.elements.append(element)
        merge_sort(self.elements)

        to_return = self

        # Max degree obtain (Splitting)
        if len(self.elements) == self.btree.get_max_degree():

            left_elements = self.elements[:len(self.elements) // 2]
            right_elements = self.elements[len(self.elements) // 2:]

            # Max Degree variation
            if self.btree.get_max_degree() % 2 == 0:
                new_top_element = left_elements.pop(-1)
                left_childs = self.childs[:len(self.childs) // 2]
                right_childs = self.childs[len(self.elements) // 2:]
            else:
                new_top_element = right_elements.pop(0)
                left_childs = self.childs[:len(self.childs) // 2 + 1]
                right_childs = self.childs[len(self.elements) // 2 + 1:]

            # Current Splitted Node is root
            if not self.parent_node:
                parent = BNode(None, self.btree)
                parent.elements = [new_top_element]
                self.btree.root = parent
            # Current Splitted Node is not root
            else:
                parent = self.parent_node
                parent = parent.add_element(new_top_element, upward=True)
                # If parent got splitted, get corresponding one
                if isinstance(parent, tuple):
                    parent = parent[0] if self in parent[0].childs else parent[1]

            # Creating new nodes and linking to parent
            new_left_node = BNode(parent, self.btree)
            new_left_node.elements = left_elements
            new_left_node.childs = left_childs

            new_right_node = BNode(parent, self.btree)
            new_right_node.elements = right_elements
            new_right_node.childs = right_childs

            # Deals with parent childs
            childs_elem_diff = len(parent.elements) + 1 - len(parent.childs)
            if childs_elem_diff > 0:
                for i in range(0, childs_elem_diff):
                    parent.childs.append(None)

            parent.childs[parent.elements.index(new_top_element)] = new_left_node
            parent.childs[parent.elements.index(new_top_element)+1] = new_right_node

            if upward:
                to_return = (new_left_node, new_right_node)

        return to_return

    def find(self, element):
        """
        Returns node containing element

        :param element: element to find
        :rtype: BNode
        """
        if element in self.elements:
            return self

        # Adding to the end child
        if element > self.elements[-1]:
            return self.childs[-1].find(element)

        # Comparing all others
        for i, e in enumerate(self.elements[:-1]):
            if element < e:
                return self.childs[i].find(element)

    def getCorrespondingElement(self, element):

        if element > self.elements[-1]:
            return self.elements[-1]

        for elem in self.elements[:-1]:
            if element < elem:
                return elem

    def elementSiblings(self, element):

        index = self.elements.index(element)

        return (self.childs[index], self.childs[index+1])

    def getRightSibling(self):

        # In case of root
        if not self.parent_node:
            return

        currIndex = self.parent_node.childs.index(self)

        # If no right sibling
        if len(self.parent_node.childs.childs) == currIndex+1:
            return

        return self.parent_node.childs.childs[currIndex+1]

    def getLeftSibling(self):
        # In case of root
        if not self.parent_node:
            return

        currIndex = self.parent_node.childs.index(self)

        # If no left sibling
        if currIndex == 0:
            return

        return self.parent_node.childs.childs[currIndex - 1]

    def __str__(self):

        return "[ " + " ".join([str(elem) for elem in self.elements]) + " ]\n"


class BTree():

    def __init__(self, max_degree):
        self.__max_degree = max_degree
        self.root = None

    def get_max_degree(self):
        return self.__max_degree

    def add_element(self, element):
        # Adding root
        if self.root == None:
            root = BNode(None, self)
            self.root = root
            root.add_element(element)
            return

        # Adding any other
        self.root.add_element(element)

    def remove_element(self, element):

        # Finding node with element to remove
        nodeWithElement = self.findNode(element)
        if not nodeWithElement:
            return

        nodeWithElement.elements.remove(element)

        # If we are respecting floor(maxdegree/2), we quit
        if not len(nodeWithElement.elements) < math.floor(self.get_max_degree() / 2):
            return

        # Otherwise we borrow or merge -------------

        left_sibling = nodeWithElement.getLeftSibling()
        right_sibling = nodeWithElement.getRightSibling()

        # If Siblings have enough element to share, we share
        using_sib = None
        for sib in [left_sibling, right_sibling]:
            if sib and len(sib.elements) > self.get_max_degree() // 2:
                using_sib = sib
                break

        corresponding_parent_elem = nodeWithElement.parent_node.getCorrespondingElement(element)
        corresponding_parent_elem_index = nodeWithElement.parent_node.elements.index(corresponding_parent_elem)

        # Emprunter
        if using_sib:
            if using_sib == left_sibling:
                last_sib_elem = using_sib.elements[-1]
            else:
                last_sib_elem = using_sib.elements[0]

            nodeWithElement.add_element(nodeWithElement.parent_node.pop(corresponding_parent_elem_index))
            nodeWithElement.parent_node.add_element(last_sib_elem) # Issue here, add_element work only for leafs

        # Sinon Merge
        else:

            mergingSibling = left_sibling if left_sibling else right_sibling

            merged_elements = nodeWithElement.elements + [corresponding_parent_elem] + mergingSibling.elements

            newNode = BNode(nodeWithElement.parent_node, self, elements=merged_elements)

            nodeWithElementIndex = nodeWithElement.parent_node.childs.index(nodeWithElement)
            nodeWithElement.parent_node.childs[nodeWithElementIndex] = newNode

            del nodeWithElement

            # Will remove on parent <3
            self.remove_element(corresponding_parent_elem)

    def findNode(self, element):
        """
        :param element: element to find
        :rtype: BNode
        """

        if not self.root:
            return

        return self.root.find(element)


    def getAllNodes(self):

        if not self.root:
            return list()

        nodes = [self.root]
        return parcoursLargeur(nodes, self.root.childs)

    def __str__(self):

        all_nodes = self.getAllNodes()

        if not all_nodes:
            return ""

        btree_str = "BTree {\n"

        for node in all_nodes:
            btree_str += str(node)

        return btree_str + "}"

def parcoursLargeur(accumulateur, childs):

    if not childs:
        return accumulateur

    accumulateur += childs

    new_childs = []
    for child in childs:
        new_childs.extend(child.childs)

    return parcoursLargeur(accumulateur, new_childs)


myBTree = BTree(4)

for i in range(0, 21):
    myBTree.add_element(i)

print(myBTree)