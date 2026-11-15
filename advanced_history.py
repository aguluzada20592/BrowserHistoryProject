from node import Node
from browser_history import BrowserHistory
class AdvancedBrowserHistory(BrowserHistory):
    def __init__(self, homepage, max_capacity=50):
        if max_capacity < 1:
            raise ValueError("Capacity must be at least 1")
        super().__init__(homepage, max_capacity)
        self.deleted_stack = []
    def visit(self, url):
        super().visit(url)
        while self.size > self.max_capacity:
            oldest = self.head
            self.head = oldest.next
            if self.head is not None:
                self.head.prev = None
            oldest.next = None
            self.size -= 1
        if self.head is None:
            self.tail = None
            self.current = None
    def delete_url(self, url):
        node = self.head
        while node is not None:
            if node.url == url:
                previous = node.prev
                following = node.next
                self.deleted_stack.append({
                    "url": node.url,
                    "prev": previous,
                    "next": following
                })
                if previous is not None:
                    previous.next = following
                else:
                    self.head = following
                if following is not None:
                    following.prev = previous
                else:
                    self.tail = previous
                if self.current is node:
                    self.current = (
                        following if following is not None else previous
                    )
                node.prev = None
                node.next = None
                self.size -= 1
                print("Deleted:", url)
                return True
            node = node.next
        print("URL not found:", url)
        return False
    def restore(self):
        if not self.deleted_stack:
            print("No deleted URLs to restore.")
            return False
        record = self.deleted_stack.pop()
        url = record["url"]
        previous = record["prev"]
        new_node = Node(url)
        node = self.head
        previous_exists = False
        while node is not None:
            if node is previous:
                previous_exists = True
                break
            node = node.next
        if previous_exists:
            new_node.prev = previous
            new_node.next = previous.next
            if previous.next is not None:
                previous.next.prev = new_node
            else:
                self.tail = new_node
            previous.next = new_node
        else:
            new_node.next = self.head
            if self.head is not None:
                self.head.prev = new_node
            else:
                self.tail = new_node
            self.head = new_node
        if self.current is None:
            self.current = new_node
        self.size += 1
        while self.size > self.max_capacity:
            oldest = self.head
            self.head = oldest.next
            if self.head is not None:
                self.head.prev = None
            else:
                self.tail = None
                self.current = None
            oldest.next = None
            self.size -= 1
        print("Restored:", url)
        return True