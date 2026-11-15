from node import Node


class BrowserHistory:
    def __init__(self, homepage, max_capacity=50):
        self.head = Node(homepage)
        self.current = self.head
        self.tail = self.head
        self.size = 1
        self.max_capacity = max_capacity

    def visit(self, url):
        if self.current is None:
            new_node = Node(url)
            self.head = new_node
            self.tail = new_node
            self.current = new_node
            self.size = 1
            return

        node = self.current.next

        while node is not None:
            next_node = node.next
            node.prev = None
            node.next = None
            self.size -= 1
            node = next_node

        self.current.next = None
        self.tail = self.current

        new_node = Node(url)
        new_node.prev = self.current
        self.current.next = new_node

        self.current = new_node
        self.tail = new_node
        self.size += 1

    def back(self, steps):
        if self.current is None:
            return None

        for _ in range(max(0, steps)):
            if self.current.prev is None:
                break
            self.current = self.current.prev

        return self.current.url

    def forward(self, steps):
        if self.current is None:
            return None

        for _ in range(max(0, steps)):
            if self.current.next is None:
                break
            self.current = self.current.next

        return self.current.url

    def current_page(self):
        if self.current is None:
            return None

        return {
            "url": self.current.url,
            "position": self._current_position(),
            "total_pages": self.size
        }

    def _current_position(self):
        position = 1
        node = self.head

        while node is not None:
            if node is self.current:
                return position
            position += 1
            node = node.next

        return None

    def display_history(self):
        if self.head is None:
            print("Browser history is empty.")
            return

        print("\n--- Browser History ---")
        node = self.head

        while node is not None:
            marker = " [CURRENT]" if node is self.current else ""
            print(node.url + marker)
            node = node.next

        print("-----------------------")

    def export_history(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            node = self.head

            while node is not None:
                file.write(node.url + "\n")
                node = node.next

        print("History exported to:", filename)

    def import_history(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                urls = [line.strip() for line in file if line.strip()]

            if not urls:
                print("Import file is empty.")
                return

            self.head = Node(urls[0])
            self.tail = self.head
            self.current = self.head
            self.size = 1

            for url in urls[1:]:
                self.visit(url)

            print("History imported from:", filename)

        except FileNotFoundError:
            print("File not found:", filename)