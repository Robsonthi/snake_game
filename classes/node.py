class Node:
    def __init__(self, head, map, body, parent, action, value):
        self.head = head
        self.map = map
        self.body = body
        self.parent = parent
        self.action = action
        self.value = value
        self.level = 0 if parent is None else parent.level+1