
from node import Node
from browser_history import BrowserHistory


class AdvancedBrowserHistory(BrowserHistory):

    def __init__(self, homepage, max_capacity=50):
        if max_capacity < 1:
            raise ValueError("Capacity must be at least 1")

        super().__init__(homepage, max_capacity)
        self.deleted_stack = []

    def _enforce_capacity(self):
        while self.size > self.max_capacity:
            oldest = self.head
            self.head = oldest.next

            if self.head is not None:
                self.head.prev = None
            else:
                self.tail = None

            if self.current is oldest:
                self.current = self.head

            oldest.prev = None
            oldest.next = None
            self.size -= 1

    def visit(self, url):
        super().visit(url)
        self._enforce_capacity()

    def delete_url(self, url):
        node = self.head
        position = 0

        while node is not None:
            if node.url == url:
                self.deleted_stack.append({
                    "url": node.url,
                    "position": position
                })

                previous = node.prev
                following = node.next

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
                        following if following is not None
                        else previous
                    )

                node.prev = None
                node.next = None
                self.size -= 1

                print("Deleted:", url)
                return True

            node = node.next
            position += 1

        print("URL not found:", url)
        return False

    def restore(self):
        if not self.deleted_stack:
            print("No deleted URLs to restore.")
            return False

        record = self.deleted_stack.pop()
        url = record["url"]
        position = record["position"]

        new_node = Node(url)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node

        elif position == 0:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        else:
            previous = self.head
            index = 1

            while previous.next is not None and index < position:
                previous = previous.next
                index += 1

            new_node.prev = previous
            new_node.next = previous.next

            if previous.next is not None:
                previous.next.prev = new_node
            else:
                self.tail = new_node

            previous.next = new_node

        self.size += 1
        self._enforce_capacity()

        print("Restored:", url)
        return True

    def delete_history(self):
        node = self.head

        while node is not None:
            next_node = node.next
            node.prev = None
            node.next = None
            node = next_node

        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

        self.deleted_stack.clear()

        print("All browser history has been deleted.")

    def import_history(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = [
                    line.strip()
                    for line in file
                    if line.strip()
                ]

            if not lines:
                print("Import file is empty.")
                return

            position = None

            if lines[0].startswith("CURRENT_POSITION:"):
                value = lines[0].split(":", 1)[1]

                if value == "None":
                    position = None
                else:
                    try:
                        position = int(value)
                    except ValueError:
                        print("Invalid current page position.")
                        return

                urls = lines[1:]
            else:
                urls = lines

            if not urls:
                if position is not None:
                    print("Invalid import file.")
                    return

                self.delete_history()
                print("History imported from:", filename)
                return

            if position is not None and not (1 <= position <= len(urls)):
                print("Invalid current page position.")
                return

            removed_count = max(0, len(urls) - self.max_capacity)
            urls = urls[-self.max_capacity:]

            self.head = Node(urls[0])
            self.tail = self.head
            self.current = self.head
            self.size = 1

            for url in urls[1:]:
                self.visit(url)

            if position is not None:
                adjusted_position = max(
                    1, position - removed_count
                )
                self.back(self.size - adjusted_position)

            self.deleted_stack.clear()

            print("History imported from:", filename)

        except OSError as error:
            print("Import failed:", error)
