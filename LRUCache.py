class Entry:
    """Doubly-linked list entry class"""
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """Doubly-linked list class"""
    def __init__(self):
        self.tail = None
        self.head = None

    def addToHead(self, entry):
        """Add a new entry to the head of the list"""
        if not self.head:
            self.head = self.tail = entry
            entry.prev = entry.next = None
        else:
            entry.next = self.head
            self.head.prev = entry
            self.head = entry

    def removeTail(self):
        """Remove the tail entry of the list"""
        if self.head == self.tail:
            self.head, self.tail = None, None
        else:
            self.tail.prev.next = None
            self.tail = self.tail.prev

    def remove(self, entry):
        """Remove a entry from the list"""
        if self.head == self.tail:
            self.head, self.tail = None, None
        elif entry == self.head:
            entry.next.prev = None
            self.head = entry.next
        elif entry == self.tail:
            entry.prev.next = None
            self.tail = entry.prev
        else:
            entry.prev.next = entry.next
            entry.next.prev = entry.prev


class LRUCache(object):

    def __init__(self, capacity):

        self.cache_capacity = capacity
        self.used_size = 0
        self.cache = DoublyLinkedList()
        self.hash = {}

    def get(self, key):
        """Get data via key, return None if not found."""
        try:
            hit = self.hash[key]
            self.cache.remove(hit)
            self.cache.addToHead(hit)
            return hit.val
        except KeyError:
            return None

    def set(self, key, val):
        """Add or update cache item.
           If key presents, updates value, otherwise add a new entry
        """
        if key in self.hash:
            self.cache.removeTail(self.hash[key])
            self.cache.addToHead(self.hash[key])
            self.hash[key].val = value
        else:
            newEntry = Entry(key, val)
            self.cache.addToHead(newEntry)
            self.hash[key] = newEntry
            self.used_size += 1
            if self.cache_capacity < self.used_size:
                self.used_size -= 1
                self.hash.pop(self.cache.tail.key)
                self.cache.removeTail()

    def peek(self, key):
        """Lookup a cache item without reorganizing the cache"""
        try:
            return self.hash[key].val
        except KeyError:
            return None

    def contains(self, key):
        """Check if a certain key is present"""
        return key in self.hash

    def size(self):
        """Get the used cache size"""
        return self.used_size

    def capacity(self):
        """Get the cache capacity"""
        return self.cache_capacity

    def clear(self):
        """Clear up the cache"""
        for entry in self.hash.itervalues():
            self.cache.remove(entry)
        self.hash.clear()
        self.used_size = 0

    def removeItem(self, key):
        """Remove a cache item by key"""
        try:
            toDelete = self.hash.pop(key)
            self.cache.remove(toDelete)
            self.used_size -= 1
            return True
        except KeyError:
            return False
