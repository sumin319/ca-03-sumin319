class Stack:
    """Stack implementation as a list"""
    def __init__(self):
        """Create new stack"""
        self._items = []
        self._length = 0
    def is_empty(self):
        """Check if the stack is empty"""
        return self._length == 0
    def push(self, item):
        """Add an item to the stack"""
        self._items.append(item)
        self._length += 1
    def pop(self):
        """Remove an item from the stack"""
        self._length -= 1
        return self._items.pop()
    def peek(self):
        """Get the value of the top item in the stack"""
        return self._items[-1]
    def size(self):
        """Get the number of items in the stack"""
        return self._length

