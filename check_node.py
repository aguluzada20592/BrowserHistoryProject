from node import Node

page = Node("https://google.com")

print("URL:", page.url)
print("Previous:", page.prev)
print("Next:", page.next)