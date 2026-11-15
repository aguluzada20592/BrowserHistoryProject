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