from SchoolClass import SchoolClass


class Node:
    def __init__(self, data: SchoolClass):
        self.data = data
        self.next = None
        self.prev = None


class Chain:
    def __init__(self, sch_class: SchoolClass) -> None:
        self.root = Node(sch_class)

    def add(self, sch_class: SchoolClass):
        self.root.next = Node(sch_class)
        self.root = self.root.next
