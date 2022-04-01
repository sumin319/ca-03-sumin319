class Queue:
    """Queue implementation as a list"""
    def __init__(self):
        """Create new queue"""
        self._items = []
        self._length = 0
    def is_empty(self):
        """Check if the queue is empty"""
        return self._length == 0
    def enqueue(self, item):
        """Add an item to the queue"""
        self._items.insert(0, item)
        self._length += 1
    def dequeue(self):
        """Remove an item from the queue"""
        self._length -= 1
        return self._items.pop()
    def size(self):
        """Get the number of items in the queue"""
        return self._length
